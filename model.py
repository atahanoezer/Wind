import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
from catboost import CatBoostRegressor
from .utils import score_function
import matplotlib.pyplot as plt
from sklearn.metrics import  mean_squared_error,mean_absolute_error
from catboost import  EShapCalcType, EFeaturesSelectionAlgorithm
import optuna


class Model:
	def __init__(
		self,
		model_function: str = "cb",
		params: dict = {},
		prediction_type: str = "one_shot",
	) -> None:
		"""
		Initialize the Model object.

		Parameters
		----------
			model_function (str, optional): 
				Model function to use ("cb" for CatBoost or "lgb" for LightGBM). Defaults to "cb".
			
			params (dict, optional):
				 Parameters for the model function. Defaults to {}.

			prediction_type (str, optional):
				 Type of prediction ("one_shot" or "recursive"). Defaults to "one_shot".


		Attributes
		----------
			model_function : str
				Model function to use ("cb" for CatBoost or "lgb" for LightGBM)
			params : dict
				Parameters for the model function
			prediction_type : str
				Type of prediction ("one_shot" or "recursive")
			model : object
				Trained model object
		"""
		self.model_function = (
			CatBoostRegressor if model_function == "cb" else LGBMRegressor
		)
		self.params = params
		self.prediction_type = prediction_type

	def train(
		self,
		train_x: pd.DataFrame,
		train_y: pd.DataFrame,
		val_x: pd.DataFrame,
		val_y: pd.DataFrame,
		multioutput: bool = False,
		verbose: int = 500,
	) -> None:
		"""
		Train the model.

		Parameters
		----------
			train_x (pd.DataFrame):
				 Training input data.

			train_y (pd.DataFrame):
				 Training target data.

			val_x (pd.DataFrame):
				 Validation input data.

			val_y (pd.DataFrame):
				 Validation target data.

			multioutput (bool, optional):
				 Flag indicating if the model supports multioutput. Defaults to False.

			verbose (int, optional):
				 Verbosity level during training. Defaults to 500.

		Returns
		-------
			None
		"""
		if multioutput:
			self.model = MultiOutputRegressor(self.model_function())
			self.model.fit(train_x, train_y, verbose=verbose)
		else:
			self.model = self.model_function(**self.params)
			self.model.fit(train_x, train_y, eval_set=(val_x, val_y), verbose=verbose)

	def predict(self, X: pd.DataFrame, horizon: int = 1) -> np.ndarray:
		"""
		Make predictions using the trained model depending on prediction type.
		Recursive prediction only supports univariate data with previous steps as features.


		Parameters
		----------
			X (pd.DataFrame): 
				Input data for prediction.
			horizon (int, optional): 
				Number of steps to predict into the future. Defaults to 1.

		Returns
		-------
			np.ndarray: 
				Predicted values.
		"""
		if self.prediction_type == "one_shot":
			forecast = self.model.predict(X)
			return forecast
		elif self.prediction_type == "recursive":
			forecast = []
			recursive_x = X.copy()

			for _ in range(horizon):
				pred = self.model.predict(recursive_x)
				recursive_x[:, :-1] = recursive_x[:, 1:]
				recursive_x[:, -1] = pred

			forecast = np.array(pred)
			return forecast
		else:
			print("Prediction type not recognized")

	def model_summarizer(
		self,
		val_x: pd.DataFrame,
		val_y: pd.DataFrame,
		test_x: pd.DataFrame,
		test_y: pd.DataFrame,
		plots: bool = True,
		plot_steps: int = 2000,
		feat_importance: bool = True,
		feat_steps: int = 15,
		feat_names: list = None,
		horizon: int = 1,
	) -> tuple:
		"""
		Generate a summary of the model's performance.

		Parameters
		----------
			val_x (pd.DataFrame):
				 Validation input data.

			val_y (pd.DataFrame):
				 Validation target data.

			test_x (pd.DataFrame):
				 Test input data.

			test_y (pd.DataFrame):
				 Test target data.

			plots (bool, optional):
				 Flag indicating if plots should be generated. Defaults to True.

			plot_steps (int, optional):
				 Number of steps to include in the plots. Defaults to 2000.

			feat_importance (bool, optional):
				 Flag indicating if feature importance should be calculated and plotted. Defaults to True.

			feat_steps (int, optional):
				 Number of top features to display in the feature importance plot. Defaults to 15.

			feat_names (list, optional):
				 List of feature names. Defaults to None.

			horizon (int, optional):
				 Number of steps to predict into the future. Defaults to 1.

		Returns
		-------
			tuple: 
				Tuple containing scores (MAE, RMSE, R2) and feature importances (if enabled).
		"""
		val_pred, test_pred = self.predict(val_x, horizon), self.predict(
			test_x, horizon
		)

		val_pred, test_pred = val_pred.reshape(-1), test_pred.reshape(-1)

		val_mae, val_rmse, val_r2 = score_function(val_y, val_pred)
		test_mae, test_rmse, test_r2 = score_function(test_y, test_pred)

		scores = pd.DataFrame(
			np.array([[val_mae, val_rmse, val_r2], [test_mae, test_rmse, test_r2]])
		)
		scores.columns = ["MAE", "RMSE", "R2"]
		scores.index = ["Validation", "Test"]
		print(scores)

		if plots:
			_, axs = plt.subplots(2, 1, figsize=(10, 8))

			# Plot the validation predictions
			axs[0].plot(
				range(plot_steps),
				val_pred[:plot_steps],
				label="Predictions",
				color="red",
			)
			axs[0].plot(
				range(plot_steps), val_y[:plot_steps], label="True", color="black"
			)
			axs[0].set_title("Validation Predictions")
			axs[0].legend()

			# Plot the test predictions
			axs[1].plot(
				range(plot_steps),
				test_pred[:plot_steps],
				label="Predictions",
				color="red",
			)
			axs[1].plot(
				range(plot_steps), test_y[:plot_steps], label="True", color="black"
			)
			axs[1].set_title("Test Predictions")
			axs[1].legend()

			# Adjust the layout and display the plot
			plt.tight_layout()
			plt.show()
		importances = None
		if feat_importance:
			# Get feature importances
			if hasattr(self.model, "feature_importances_"):
				importances = self.model.feature_importances_
			elif hasattr(self.model, "get_feature_importance"):
				importances = self.model.get_feature_importance()
			else:
				print("Model does not have feature importance attribute")
			
			if importances is not None:
				# Sort indices from most to least important and get corresponding names
				indices = np.argsort(importances)[::-1]
				names = [feat_names[i] for i in indices]

				# Create plot
				plt.figure(figsize=(10, 8))

				# Create plot title
				plt.title("Feature Importance")

				# Add bars
				plt.bar(range(feat_steps), importances[indices][:feat_steps])

				# Add feature names as x-axis labels
				plt.xticks(range(feat_steps), names[:feat_steps], rotation=90)

				# Show plot
				plt.show()
		return scores, importances
	
	def hyp_op(
			self,
			val_x: pd.DataFrame,
			val_y: pd.DataFrame,
			train_x: pd.DataFrame,
			train_y: pd.DataFrame,
			horizon: int = 1,
			trial = 30,
			task_type = 'GPU'
		) -> tuple:
		"""
			Perform hyperparameter optimization for a machine learning model using Optuna.

			Parameters:
				val_x (pd.DataFrame): Validation dataset features.
				val_y (pd.DataFrame): Validation dataset labels.
				train_x (pd.DataFrame): Training dataset features.
				train_y (pd.DataFrame): Training dataset labels.
				horizon (int, optional): Prediction horizon for the model. Default is 1.
				trial (int, optional): Number of optimization trials. Default is 30.
				task_type (str, optional): Task type for CatBoost ('CPU' or 'GPU'). Default is 'GPU'.

			Returns:
				tuple: A tuple containing the best hyperparameters (dict) and the corresponding best RMSE (float).

			This function uses Optuna to perform hyperparameter optimization for a CatBoost machine learning model.
			It searches for the best hyperparameters within the specified parameter ranges and training settings.

			The optimization objective is to minimize the Root Mean Squared Error (RMSE) on the validation dataset.
			The best hyperparameters and their corresponding RMSE are returned as a tuple.

			Example:
				best_params, best_rmse = hyp_op(val_x, val_y, train_x, train_y, horizon=2, trial=50, task_type='GPU')
				print("Best Hyperparameters:", best_params)
				print("Best RMSE:", best_rmse)
		"""

		def objective(trial):
			params = {
				"iterations": 1000,
				"learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.1, log=True),
				"depth": trial.suggest_int("depth", 1, 10),
				# "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.05, 1.0), # requires task type CPU
				"min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
				'task_type': task_type,
				'thread_count':-1
			}

			self.model = self.model_function(**params)
			self.model.fit(train_x, train_y,eval_set=(val_x, val_y), silent=True)

			val_pred = self.predict(val_x, horizon)
			rmse = mean_absolute_error(val_y, val_pred.reshape(-1))

			return rmse
		study = optuna.create_study(direction='minimize')
		study.optimize(objective, n_trials=30)

		print('Best hyperparameters:', study.best_params)
		print('Best RMSE:', study.best_value)
		return study.best_params, study.best_value


	def feat_select(self,
      val_x: pd.DataFrame,
      val_y: pd.DataFrame,
      train_x: pd.DataFrame,
      train_y: pd.DataFrame,
      num_feats = 20,
      num_steps = 3,
	  plot = True
        ):
		"""
		Perform feature selection using CatBoost's select_features method.

		Parameters:
			val_x (pd.DataFrame): Validation dataset features.
			val_y (pd.DataFrame): Validation dataset labels.
			train_x (pd.DataFrame): Training dataset features.
			train_y (pd.DataFrame): Training dataset labels.
			num_feats (int, optional): Number of features to select. Default is 20.
			num_steps (int, optional): Number of feature selection steps. Default is 3.
			plot (bool, optional): Whether to plot feature selection results. Default is True.

		Returns:
			catboost.FeatureSelectionSummary: A summary of the feature selection process.

		This function uses CatBoost's select_features method to perform feature selection on the given datasets.
		It selects a specified number of features based on their importance and returns a summary of the process.

		Example:
			summary = feat_select(val_x, val_y, train_x, train_y, num_feats=15, num_steps=4, plot=True)
			print(summary)
    	"""
		self.model = self.model_function(**self.params)
		summary = self.model.select_features(
				X= train_x,
				y= train_y,
				eval_set=(val_x, val_y),
				features_for_select=list(range(train_x.shape[1])),
				num_features_to_select=num_feats,
				steps=num_steps,
				algorithm=EFeaturesSelectionAlgorithm.RecursiveByShapValues,
				shap_calc_type=EShapCalcType.Regular,
				train_final_model=True,
				logging_level='Silent',
				plot=plot
				)

		return summary
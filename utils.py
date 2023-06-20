import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


def model_summarizer(model, predictions, targets, plot_steps=100, exp_title='', feat=True,
                     feature_names=None):
    _, val_pred, test_pred = predictions.items()
    _, val_y, test_y = targets.items()

    score, mape, rmse, R2 = score_function(test_y[1], test_pred[1])
    print(f'Mix score: {score}, MAPE: {mape}, RMSE: {rmse}, R2: {R2}')

    plt.figure(figsize=(10, 10))
    index = np.arange(val_y[1].shape[0])
    plt.plot(index[:plot_steps], val_y[1][:plot_steps], label='Y')
    plt.plot(index[:plot_steps], val_pred[1][:plot_steps], label='Pred')
    plt.legend()
    plt.title(f'{exp_title} prediction Val')

    plt.figure(figsize=(10, 10))
    index = np.arange(test_y[1].shape[0])
    plt.plot(index[:plot_steps], test_y[1][:plot_steps], label='Y')
    plt.plot(index[:plot_steps], test_pred[1][:plot_steps], label='Pred')
    plt.legend()
    plt.title(f'{exp_title} prediction Test')
    # plt.plot(test_preds.yhat,label = ' Y_hat')

    if feat:
        feature_importance = model.get_feature_importance()

        # Create a bar plot of feature importance
        plt.figure(figsize=(10, 8))
        plt.bar(feature_names, feature_importance)
        plt.xticks(rotation=90)
        plt.xlabel('Features')
        plt.ylabel('Importance')
        plt.title(f'Feature Importance {exp_title}')
    plt.tight_layout()
    plt.show()


def score_function(true_values, predicted_values):
    """
    Calculate a score to evaluate the performance of a time series prediction model.

    Parameters:
    true_values (numpy.ndarray): Array of true values for the time series.
    predicted_values (numpy.ndarray): Array of predicted values for the time series.

    Returns:
    float: Score representing the performance of the prediction model.
    """
    # Calculate the mean absolute percentage error (MAPE)
    mae = mean_absolute_error(true_values, predicted_values)

    # Calculate the root mean squared error (RMSE)
    rmse = mean_squared_error(true_values, predicted_values, squared=False)

    r_2 = r2_score(true_values, predicted_values)

    return  mae, rmse, r_2




	# def create_dataset(self, delay: int, roll_time: int, rolling_features: list = []) -> pd.DataFrame:
	# 	"""
	# 	Creates the final dataset with lagged features, rolling window features, and additional features.

	# 	Parameters:
	# 			delay (int): The number of time steps to lag the target variable.
	# 			roll_time (int): The window size for the rolling window features.
	# 			rolling_features (list): A list of column names on which to apply the rolling window features.

	# 	Returns:
	# 			pd.DataFrame: The final dataset with all the engineered features.
	# 	"""
	# 	X = self.df.copy()
	# 	y = self.create_y(X, delay)
	# 	X = X.dropna(subset=['y'])
	# 	X = X.ffill()

	# 	for f in rolling_features:
	# 		self.apply_rolling_window(X, f, roll_time, np.mean)
	# 		self.apply_rolling_window(X, f, roll_time, np.std)
	# 		self.apply_rolling_window(X, f, roll_time, np.min)
	# 		self.apply_rolling_window(X, f, roll_time, np.max)
	# 		self.apply_rolling_window(X, f, roll_time, np.median)

	# 	if delay < 20:
	# 		self.add_last_t(X, 'active_power_total', step=2)

	# 	return X, y
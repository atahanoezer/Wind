import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
from catboost import CatBoostRegressor
from Wind.utils import score_function
import matplotlib.pyplot as plt


class Model:
    def __init__(
        self,
        model_function: str = "cb",
        params: dict = {},
        prediction_type: str = "one_shot",
    ) -> None:
        """
        Initialize the Model object.

        Args:
            model_function (str, optional): Model function to use ("cb" for CatBoost or "lgb" for LightGBM). Defaults to "cb".
            params (dict, optional): Parameters for the model function. Defaults to {}.
            prediction_type (str, optional): Type of prediction ("one_shot" or "recursive"). Defaults to "one_shot".
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

        Args:
            train_x (pd.DataFrame): Training input data.
            train_y (pd.DataFrame): Training target data.
            val_x (pd.DataFrame): Validation input data.
            val_y (pd.DataFrame): Validation target data.
            multioutput (bool, optional): Flag indicating if the model supports multioutput. Defaults to False.
            verbose (int, optional): Verbosity level during training. Defaults to 500.

        Returns:
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
        Make predictions using the trained model.

        Args:
            X (pd.DataFrame): Input data for prediction.
            horizon (int, optional): Number of steps to predict into the future. Defaults to 1.

        Returns:
            np.ndarray: Predicted values.
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

        Args:
            val_x (pd.DataFrame): Validation input data.
            val_y (pd.DataFrame): Validation target data
            test_x (pd.DataFrame): Test input data.
            test_y (pd.DataFrame): Test target data.
            plots (bool, optional): Flag indicating if plots should be generated. Defaults to True.
            plot_steps (int, optional): Number of steps to include in the plots. Defaults to 2000.
            feat_importance (bool, optional): Flag indicating if feature importance should be calculated and plotted. Defaults to True.
            feat_steps (int, optional): Number of top features to display in the feature importance plot. Defaults to 15.
            feat_names (list, optional): List of feature names. Defaults to None.
            horizon (int, optional): Number of steps to predict into the future. Defaults to 1.

        Returns:
            tuple: Tuple containing scores (MAE, RMSE, R2) and feature importances (if enabled).
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

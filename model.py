from typing import Any
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.multioutput import MultiOutputRegressor
from catboost import CatBoostRegressor
from utils import score_function
import matplotlib.pyplot as plt


class Model:
    def __init__(self, model_function="cb", params={}) -> None:
        self.model_function = (
            CatBoostRegressor if model_function == "cb" else LGBMRegressor
        )
        self.params = params

    def train(
        self,
        train_x: pd.DataFrame,
        train_y: pd.DataFrame,
        val_x: pd.DataFrame,
        val_y: pd.DataFrame,
        multioutput=False,
        verbose=500,
    ):
        """
        Trains the model.

        Parameters:
                        train_x (pd.DataFrame): The input DataFrame.
                        train_y (pd.DataFrame): The output DataFrame.

        Returns:
                        None
        """

        if multioutput: # TODO  CB does not support multioutput valitdation
            self.model = MultiOutputRegressor(
                self.model_function()
            )
            self.model.fit(train_x, train_y,verbose=500)
        else:
            self.model = self.model_function(**self.params)
            self.model.fit(train_x, train_y, eval_set=(val_x, val_y),verbose=500)

    def predict(self, test_x: pd.DataFrame, prediction_type="one_shot") -> np.ndarray:
        if prediction_type == "one_shot":
            forecast = self.model.predict(test_x)
            # check wheter forecast is 2d or 1d
            if len(forecast.shape) == 2:
                forecast = forecast[:, -1]
            return forecast
        elif prediction_type == "recursive":
            print("Not implemented yet")
        else:
            print("Prediction type not recognized")

    def model_summarizer(
        self,
        val_x: pd.DataFrame,
        val_y: pd.DataFrame,
        test_x: pd.DataFrame,
        test_y: pd.DataFrame,
        plots=True,
        plot_steps=2000,
        feat_importance=True,
        feat_steps=15,
    ):
        val_pred, test_pred = self.predict(val_x), self.predict(test_x)
        # give assertion error if predictions are not 1d
        assert (
            len(val_pred.shape) == 1 and len(test_pred.shape) == 1
        ), "Predictions are not 1d"
        # give assertion error if the shape of the prediction is not the same as the shape of the test set
        if len(test_y.shape) != 1: # returning to original shape
            test_y = test_y[:, -1]
        if len(val_y.shape) != 1: # returning to original shape
            val_y = val_y[:, -1]

        val_mae, val_rmse, val_r2 = score_function(val_y, val_pred)
        test_mae, test_rmse, test_r2 = score_function(test_y, test_pred)
        # create a 2 row  dataframe to store the results, first row is for validation, second row is for test
        scores = pd.DataFrame(
            np.array([[val_mae, val_rmse, val_r2], [test_mae, test_rmse, test_r2]])
        )
        scores.columns = ["MAE", "RMSE", "R2"]
        scores.index = ["Validation", "Test"]
        print(scores)

        if plots:
            fig, axs = plt.subplots(2, 1, figsize=(10, 8))

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
            axs[1].plot(range(plot_steps), test_y[:plot_steps], label="True", color="black")
            axs[1].set_title("Test Predictions")
            axs[1].legend()

            # Adjust the layout and display the plot
            plt.tight_layout()
            plt.show()
        # TODO make feat importance a DF
        # TODO importance for multioutput
        importances = None
        if feat_importance:
            # Get feature importances
            if hasattr(self.model, "feature_importances_"):
                importances = self.model.feature_importances_
            elif hasattr(self.model, "get_feature_importance"):
                importances = self.model.get_feature_importance()
            else:
                print("Model does not have feature importance attribute")
                


            # check if model is catboost or lightgbm

            # Sort indices from most to least important and get corresponding names
            if importances is not None :
                indices = np.argsort(importances)[::-1]
                names = [val_x.columns[i] for i in indices]

                # Create plot
                plt.figure(figsize=(10, 8))

                # Create plot title
                plt.title("Feature Importance")

                # Add bars
                plt.bar(range(val_x.shape[1]), importances[indices][:feat_steps])

                # Add feature names as x-axis labels
                plt.xticks(range(val_x.shape[1]), names[:feat_steps], rotation=90)

                # Show plot
                plt.show()
        return scores, importances

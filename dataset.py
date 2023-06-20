import pandas as pd
import numpy as np


class Dataset:
    """
    A class that represents a dataset and provides methods for data preprocessing and feature engineering.

    Parameters:
                    df (pd.DataFrame): The input DataFrame containing the dataset.

    Methods:
                    create_y(df: pd.DataFrame, delay: int) -> pd.DataFrame:
                                    Creates a lagged target variable DataFrame.

                    apply_rolling_window(df: pd.DataFrame, data: str, roll_time: int, window_function: callable):
                                    Applies a rolling window function to a specific column of the DataFrame.

                    add_last_t(df: pd.DataFrame, data: str, step: int = 2):
                                    Adds the last T steps of a specific column as new features to the DataFrame.

                    add_seasonal_feat(df: pd.DataFrame):
                                    Adds seasonal features based on time information to the DataFrame.

                    create_dataset(delay: int, roll_time: int, rolling_features: list = []) -> pd.DataFrame:
                                    Creates the final dataset with lagged features, rolling window features, and additional features.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def fill_nan(self, fields):  # TODO add delayed Nan handling
        for f in fields:  # fill na with previous value
            self.df[f] = self.df[f].ffill()
            self.df[f] = self.df[f].fillna(
                self.df[f].mean()
            )  # fill remaining na with mean

    def drop_nan(self, fields):
        self.df = self.df.drop(columns=fields)

    def sample(self, n: int):
        self.df = self.df.iloc[::n, :]  # sample every nth row

    def create_y(self, df: pd.DataFrame, delay: int) -> pd.DataFrame:
        """
        Create a lagged target variable DataFrame.

        Parameters:
                        df (pd.DataFrame): The input DataFrame.
                        delay (int): The number of time steps to lag the data.

        Returns:
                        pd.DataFrame: The DataFrame with the lagged target variable.
        """
        y = pd.DataFrame()
        y["y"] = df.shift(-delay)
        y.dropna(inplace=True)
        return y

    def apply_rolling_window(
        self, df: pd.DataFrame, data: str, roll_time: int, window_function: callable
    ):
        """
        Applies a rolling window function to a specific column of the DataFrame.

        Parameters:
                        df (pd.DataFrame): The input DataFrame.
                        data (str): The column name on which to apply the rolling window function.
                        roll_time (int): The window size for the rolling window function.
                        window_function (callable): The function to apply on the rolling window.

        Returns:
                        pd.DataFrame: The DataFrame with the applied rolling window function.
        """
        if not callable(window_function):
            raise ValueError("window_function must be a callable function")

        df[f"rolling_{window_function.__name__}_{data}"] = (
            df[data].rolling(window=roll_time).apply(window_function)
        )
        df.fillna(0, inplace=True)
        return df

    def add_last_t(self, df: pd.DataFrame, data: str, step: int = 2):
        """
        Adds the last T steps of a specific column as new features to the DataFrame.

        Parameters:
                        df (pd.DataFrame): The input DataFrame.
                        data (str): The column name for which to add the last T steps as new features.
                        step (int): The number of steps to consider.

        Returns:
                        None
        """
        for i in range(1, step + 1):
            df[f"{data}_last_{i}_step"] = df[data].shift(i)
            df[f"{data}_last_{i}_step"].fillna(0)

    def get_df(self):
        return self.df

    def add_seasonal_feat(self, df: pd.DataFrame):
        """
        Adds seasonal features based on time information to the DataFrame.

        Parameters:
                        df (pd.DataFrame): The input DataFrame.

        Returns:
                        None
        """
        df["hour_sin"] = np.sin(df.Time.dt.hour / 23 * 2 * np.pi)
        df["hour_cos"] = np.cos(df.Time.dt.hour / 23 * 2 * np.pi)
        df["week_sin"] = np.sin((df.Time.dt.week / 52) * 2 * np.pi)
        df["week_cos"] = np.cos((df.Time.dt.week / 52) * 2 * np.pi)

    def create_dataset(
        self, df, window_size, prediction_horizon, shuffle=False, test_split=0.2,val_split=0.2
    ):  # TODO vectorize
        # TODO add index to df
        def create_xy(df):
            X = []
            y = []
            for i in range(0, len(df)):
                if (
                    len(df[(i + window_size) : (i + window_size + prediction_horizon)])
                    < prediction_horizon
                ):
                    break
                X.append(df[i : (i + window_size)])
                y.append(df[(i + window_size) : (i + window_size + prediction_horizon)])
            X = np.array(X)
            y = np.array(y)
            return X, y

        train_split = len(df) - int(len(df) * test_split) - int(len(df) * val_split)
        val_split = len(df) - int(len(df) * test_split)
        train_df = df[:train_split]
        val_df = df[train_split - window_size :val_split]
        test_df = df[val_split - window_size :]

        train_x, train_y = create_xy(train_df)
        val_x, val_y = create_xy(val_df)
        test_x, test_y = create_xy(test_df)

        return train_x,val_x, test_x, train_y,val_y, test_y

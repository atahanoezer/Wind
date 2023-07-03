import pandas as pd
import numpy as np


class Dataset:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the Dataset object.

        Parameters
        ----------
            df (pd.DataFrame): 
                Input DataFrame containing the data.
        """
        self.df = df

    def fill_nan(self, fields: list):
        """
        Fill missing values (NaN) in the specified fields/columns of the DataFrame.

        Parameters
        ----------
            fields (list): 
                List of fields/columns to fill missing values.

        Returns
        -------
            None
        """
        for f in fields:
            self.df[f] = self.df[f].ffill()
            self.df[f] = self.df[f].fillna(self.df[f].mean())

    def drop_nan(self, fields: list):
        """
        Drop columns in the specified fields/columns of the DataFrame.

        Parameters
        ----------
            fields (list): 
                List of fields/columns to drop rows with NaN values.

        Returns
        -------
            None
        """
        self.df = self.df.drop(columns=fields)

    def sample(self, n: int):
        """
        Sample every nth row from the DataFrame.

        Parameters
        ----------
            n (int): 
                Sampling interval.

        Returns
        -------
            None
        """
        self.df = self.df.iloc[::n, :]

    def apply_rolling_window(
        self, df: pd.DataFrame, data: str, roll_time: int, window_function: callable
    ) :
        """
        Apply a rolling window function to the specified data column in the DataFrame.

        Parameters
        ----------
            df (pd.DataFrame): 
                DataFrame to which the rolling window function will be applied.

            data (str): 
                Column name containing the data to apply the rolling window function.

            roll_time (int): 
                Window size for the rolling window.

            window_function (callable): 
                Callable function to apply as the rolling window function.
        Returns
        -------
            None
        """
        if not callable(window_function):
            raise ValueError("window_function must be a callable function")

        df[f"rolling_{window_function.__name__}_{data}_{roll_time}"] = (
            df[data].rolling(window=roll_time).apply(window_function)
        )
        df.fillna(0, inplace=True)


    def add_last_t(self, df: pd.DataFrame, data: str, step: int = 2):
        """
        Add lagged versions of a column to the DataFrame.

        Parameters
        ----------
            df (pd.DataFrame): 
                DataFrame to which the lagged columns will be added.

            data (str): 
                Column name to create lagged versions of.

            step (int, optional): 
                Number of lagged steps to add. Defaults to 2.

        Returns
        -------
            None
        """
        for i in range(1, step + 1):
            df[f"{data}_last_{i}_step"] = df[data].shift(i)
            df[f"{data}_last_{i}_step"].fillna(0)

    def add_seasonal_feat(self, df: pd.DataFrame, time_col):
        """
        Add seasonal features based on a time column.

        Parameters
        ----------
            df (pd.DataFrame): 
                DataFrame to which the seasonal features will be added.

            time_col: 
                Time column to extract seasonal features from.

        Returns
        -------
            None
        """
        df["hour_sin"] = np.sin(time_col.hour / 23 * 2 * np.pi)
        df["hour_cos"] = np.cos(time_col.hour / 23 * 2 * np.pi)
        df["week_sin"] = np.sin((time_col.week / 52) * 2 * np.pi)
        df["week_cos"] = np.cos((time_col.week / 52) * 2 * np.pi)

    def create_dataset(
        self,
        df: pd.DataFrame,
        window_size: int,
        prediction_horizon: int,
        test_split: float = 0.2,
        val_split: float = 0.2,
        univariate: bool = False,
        target_col: str = "active_power_total",
    ) -> tuple:
        """
        Create a dataset for training and evaluation.

        Parameters
        ----------
            df (pd.DataFrame):
                 Input DataFrame containing the data.

            window_size (int):
                 Size of the input window.

            prediction_horizon (int):
                 Number of steps to predict into the future.

            test_split (float, optional): 
                Ratio of test data split. Defaults to 0.2.

            val_split (float, optional):
                 Ratio of validation data split. Defaults to 0.2.

            univariate (bool, optional): 
                Flag indicating if the data is univariate. Defaults to False.
                
            target_col (str, optional): 
                Name of the target column. Defaults to "active_power_total".

        Returns
        -------
            tuple: Tuple containing train,val and test data and labels, as well as feature names.
        """

        def create_xy(df: pd.DataFrame) -> tuple:  # TODO: Vectorize
            X = []
            y = []
            for i in range(0, len(df)):
                if (
                    len(df[(i + window_size) : (i + window_size + prediction_horizon)])
                    < prediction_horizon
                ):
                    break
                X.append(df[target_col][i : (i + window_size)])
                y.append(
                    df[target_col][
                        (i + window_size) : (i + window_size + prediction_horizon)
                    ]
                )
            X = np.array(X)

            if not univariate:
                X = np.concatenate(
                    (
                        X,
                        df.iloc[window_size-1 : len(X) + window_size-1, :]
                        .copy()
                        .drop(target_col, axis=1),# target col appears as the highest lag
                    ),
                    axis=1,
                )
            y = np.array(y)
            return X, y

        train_split = len(df) - int(len(df) * test_split) - int(len(df) * val_split)
        val_split = len(df) - int(len(df) * test_split)
        train_df = df[:train_split]
        val_df = df[train_split - window_size : val_split]
        test_df = df[val_split - window_size :]

        train_x, train_y = create_xy(train_df)
        val_x, val_y = create_xy(val_df)
        test_x, test_y = create_xy(test_df)

        names = [f"lag_{i}" for i in range(1, window_size + 1)]
        names.extend(list(df.copy().drop(target_col, axis=1).columns))

        return train_x, val_x, test_x, train_y, val_y, test_y, names

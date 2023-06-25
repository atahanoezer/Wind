from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


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

    # Calculate the R2 score
    r_2 = r2_score(true_values, predicted_values)

    return mae, rmse, r_2

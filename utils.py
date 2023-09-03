from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import numpy as np
from tabulate import tabulate

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

def experiment_results(names, results,title = 'Results'):
    """
    Display experiment results in a formatted table with optional title.

    Parameters:
        names (list): List of model names.
        results (list of dict): List of dictionaries containing metric results for each model.
        title (str, optional): Title to be displayed above the results table. Default is 'Results'.

    This function takes model names and their corresponding metric results and displays them in a formatted table.
    It includes options to display a title above the table and make the best values bold.
    If any metric value is 0, it is displayed as '-' in the table.

    Example:
        names = ["Model 1", "Model 2", "Model 3"]
        results = [
            {"MAE": 0.1, "RMSE": 0.2, "R2": 0.9},
            {"MAE": 0, "RMSE": 0.25, "R2": 0.85},
            {"MAE": 0.12, "RMSE": 0.22, "R2": 0.88},
        ]
        experiment_results(names, results, title='Experiment 1 Results')
    """
    metrics = ['MAE', 'RMSE', 'R2']

    header = ['Metric'] + metrics
    table_data = []

    # Add a title row
    title_row = [title] + [''] * len(metrics)
    table_data.append(title_row)

    best_mae_idx = np.argmin([r['MAE'] for r in results])
    best_rmse_idx = np.argmin([r['RMSE'] for r in results])
    best_r2_idx = np.argmax([r['R2'] for r in results])

    for i, n in enumerate(names):
        value = [n] + [np.round(results[i]['MAE'], 3)] + [np.round(results[i]['RMSE'], 3)] + [np.round(results[i]['R2'], 3)]
        # Replace 0 with "-"
        value = ['-' if val == 0 else val for val in value]
        if i in [best_mae_idx, best_rmse_idx, best_r2_idx]:
            # Make the best values bold using Markdown syntax
            value = ['**' + str(val) + '**' if idx > 0 else val for idx, val in enumerate(value)]
        table_data.append(value)

    table = tabulate(table_data, headers=header, tablefmt='pipe')
    print(table)
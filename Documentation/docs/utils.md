<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style>##Wind.utils.**score_function**

<p class="func-header">
    <i>def</i> Wind.utils.<b>score_function</b>(<i>true_values, predicted_values</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/Wind/utils.py#L5">[source]</a>
</p>

Calculate a score to evaluate the performance of a time series prediction model.

Parameters:
true_values (numpy.ndarray): Array of true values for the time series.
predicted_values (numpy.ndarray): Array of predicted values for the time series.

Returns:
float: Score representing the performance of the prediction model.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##Wind.utils.**experiment_results**

<p class="func-header">
    <i>def</i> Wind.utils.<b>experiment_results</b>(<i>names, results, title='Results'</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/Wind/utils.py#L27">[source]</a>
</p>

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

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>


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
</style>##dataset.**Dataset**

<p class="func-header">
    <i>class</i> dataset.<b>Dataset</b>(<i>df: pd.DataFrame</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L5">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>fill_nan</b>(<i>self, fields: list</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L15">[source]</a>
</p>

Fill missing values (NaN) in the specified fields/columns of the DataFrame.

Args:
fields (list): List of fields/columns to fill missing values.

Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>drop_nan</b>(<i>self, fields: list</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L29">[source]</a>
</p>

Drop rows containing NaN values in the specified fields/columns of the DataFrame.

Args:
fields (list): List of fields/columns to drop rows with NaN values.

Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>sample</b>(<i>self, n: int</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L41">[source]</a>
</p>

Sample every nth row from the DataFrame.

Args:
n (int): Sampling interval.

Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>apply_rolling_window</b>(<i>self, df: pd.DataFrame, data: str, roll_time: int, window_function: callable</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L53">[source]</a>
</p>

Apply a rolling window function to the specified data column in the DataFrame.

Args:
df (pd.DataFrame): DataFrame to which the rolling window function will be applied.
data (str): Column name containing the data to apply the rolling window function.
roll_time (int): Window size for the rolling window.
window_function (callable): Callable function to apply as the rolling window function.
Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>add_last_t</b>(<i>self, df: pd.DataFrame, data: str, step: int=2</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L76">[source]</a>
</p>

Add lagged versions of a column to the DataFrame.

Args:
df (pd.DataFrame): DataFrame to which the lagged columns will be added.
data (str): Column name to create lagged versions of.
step (int, optional): Number of lagged steps to add. Defaults to 2.

Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>add_seasonal_feat</b>(<i>self, df: pd.DataFrame, time_col</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L92">[source]</a>
</p>

Add seasonal features based on a time column.

Args:
df (pd.DataFrame): DataFrame to which the seasonal features will be added.
time_col: Time column to extract seasonal features from.

Returns:
None

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>create_dataset</b>(<i>self, df: pd.DataFrame, window_size: int, prediction_horizon: int, test_split: float=0.2, val_split: float=0.2, univariate: bool=False, target_col: str='active_power_total'</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L108">[source]</a>
</p>

Create a dataset for training and evaluation.

Args:
df (pd.DataFrame): Input DataFrame containing the data.
window_size (int): Size of the input window.
prediction_horizon (int): Number of steps to predict into the future.
test_split (float, optional): Ratio of test data split. Defaults to 0.2.
val_split (float, optional): Ratio of validation data split. Defaults to 0.2.
univariate (bool, optional): Flag indicating if the data is univariate. Defaults to False.
target_col (str, optional): Name of the target column. Defaults to "active_power_total".

Returns:
tuple: Tuple containing train,val and test data and labels, as well as feature names.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>


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
    <i></i> <b>fill_nan</b>(<i>self, fields: list</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L17">[source]</a>
</p>

Fill missing values (NaN) in the specified fields/columns of the DataFrame.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>fields (list) : <i></i></b>
<p class="attr">
    List of fields/columns to fill missing values.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>drop_nan</b>(<i>self, fields: list</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L34">[source]</a>
</p>

Drop rows containing NaN values in the specified fields/columns of the DataFrame.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>fields (list) : <i></i></b>
<p class="attr">
    List of fields/columns to drop rows with NaN values.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>sample</b>(<i>self, n: int</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L49">[source]</a>
</p>

Sample every nth row from the DataFrame.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>n (int) : <i></i></b>
<p class="attr">
    Sampling interval.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>apply_rolling_window</b>(<i>self, df: pd.DataFrame, data: str, roll_time: int, window_function: callable</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L64">[source]</a>
</p>

Apply a rolling window function to the specified data column in the DataFrame.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>df (pd.DataFrame) : <i></i></b>
<p class="attr">
    DataFrame to which the rolling window function will be applied.
</p>
<b>data (str) : <i></i></b>
<p class="attr">
    Column name containing the data to apply the rolling window function.
</p>
<b>roll_time (int) : <i></i></b>
<p class="attr">
    Window size for the rolling window.
</p>
<b>window_function (callable) : <i></i></b>
<p class="attr">
    Callable function to apply as the rolling window function.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>add_last_t</b>(<i>self, df: pd.DataFrame, data: str, step: int=2</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L96">[source]</a>
</p>

Add lagged versions of a column to the DataFrame.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>df (pd.DataFrame) : <i></i></b>
<p class="attr">
    DataFrame to which the lagged columns will be added.
</p>
<b>data (str) : <i></i></b>
<p class="attr">
    Column name to create lagged versions of.
</p>
<b>step (int, optional) : <i></i></b>
<p class="attr">
    Number of lagged steps to add. Defaults to 2.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>add_seasonal_feat</b>(<i>self, df: pd.DataFrame, time_col</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L119">[source]</a>
</p>

Add seasonal features based on a time column.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>df (pd.DataFrame) : <i></i></b>
<p class="attr">
    DataFrame to which the seasonal features will be added.
</p>
<b>time_col : <i></i></b>
<p class="attr">
    Time column to extract seasonal features from.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>None : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>create_dataset</b>(<i>self, df: pd.DataFrame, window_size: int, prediction_horizon: int, test_split: float=0.2, val_split: float=0.2, univariate: bool=False, target_col: str='active_power_total'</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/dataset.py#L140">[source]</a>
</p>

Create a dataset for training and evaluation.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>df (pd.DataFrame) : <i></i></b>
<p class="attr">
    Input DataFrame containing the data.
</p>
<b>window_size (int) : <i></i></b>
<p class="attr">
    Size of the input window.
</p>
<b>prediction_horizon (int) : <i></i></b>
<p class="attr">
    Number of steps to predict into the future.
</p>
<b>test_split (float, optional) : <i></i></b>
<p class="attr">
    Ratio of test data split. Defaults to 0.2.
</p>
<b>val_split (float, optional) : <i></i></b>
<p class="attr">
    Ratio of validation data split. Defaults to 0.2.
</p>
<b>univariate (bool, optional) : <i></i></b>
<p class="attr">
    Flag indicating if the data is univariate. Defaults to False.
</p>
<b>target_col (str, optional) : <i></i></b>
<p class="attr">
    Name of the target column. Defaults to "active_power_total".
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>tuple : <i>Tuple containing train,val and test data and labels, as well as feature names.</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>


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
</style>##model.**Model**

<p class="func-header">
    <i>class</i> model.<b>Model</b>(<i>model_function: str='cb', params: dict={}, prediction_type: str='one_shot'</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/model.py#L10">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>train</b>(<i>self, train_x: pd.DataFrame, train_y: pd.DataFrame, val_x: pd. DataFrame, val_y: pd.DataFrame, multioutput: bool=False, verbose: int=500 </i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/model.py#L56">[source]</a>
</p>

Train the model.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>train_x (pd.DataFrame) : <i></i></b>
<p class="attr">
    Training input data.
</p>
<b>train_y (pd.DataFrame) : <i></i></b>
<p class="attr">
    Training target data.
</p>
<b>val_x (pd.DataFrame) : <i></i></b>
<p class="attr">
    Validation input data.
</p>
<b>val_y (pd.DataFrame) : <i></i></b>
<p class="attr">
    Validation target data.
</p>
<b>multioutput (bool, optional) : <i></i></b>
<p class="attr">
    Flag indicating if the model supports multioutput. Defaults to False.
</p>
<b>verbose (int, optional) : <i></i></b>
<p class="attr">
    Verbosity level during training. Defaults to 500.
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
    <i></i> <b>predict</b>(<i>self, X: pd.DataFrame, horizon: int=1</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/model.py#L99">[source]</a>
</p>

Make predictions using the trained model depending on prediction type.
Recursive prediction only supports univariate data with previous steps as features.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>X (pd.DataFrame) : <i></i></b>
<p class="attr">
    Input data for prediction. horizon (int, optional): Number of steps to predict into the future. Defaults to 1.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>np.ndarray : <i></i></b>
<p class="attr">
    Predicted values.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>model_summarizer</b>(<i>self, val_x: pd.DataFrame, val_y: pd.DataFrame, test_x: pd.DataFrame, test_y: pd.DataFrame, plots: bool=True, plot_steps: int= 2000, feat_importance: bool=True, feat_steps: int=15, feat_names: list= None, horizon: int=1</i>) <a class="src-href" target="_blank" href="https://github.com/atahanoezer/Wind.git/model.py#L134">[source]</a>
</p>

Generate a summary of the model's performance.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>val_x (pd.DataFrame) : <i></i></b>
<p class="attr">
    Validation input data.
</p>
<b>val_y (pd.DataFrame) : <i></i></b>
<p class="attr">
    Validation target data.
</p>
<b>test_x (pd.DataFrame) : <i></i></b>
<p class="attr">
    Test input data.
</p>
<b>test_y (pd.DataFrame) : <i></i></b>
<p class="attr">
    Test target data.
</p>
<b>plots (bool, optional) : <i></i></b>
<p class="attr">
    Flag indicating if plots should be generated. Defaults to True.
</p>
<b>plot_steps (int, optional) : <i></i></b>
<p class="attr">
    Number of steps to include in the plots. Defaults to 2000.
</p>
<b>feat_importance (bool, optional) : <i></i></b>
<p class="attr">
    Flag indicating if feature importance should be calculated and plotted. Defaults to True.
</p>
<b>feat_steps (int, optional) : <i></i></b>
<p class="attr">
    Number of top features to display in the feature importance plot. Defaults to 15.
</p>
<b>feat_names (list, optional) : <i></i></b>
<p class="attr">
    List of feature names. Defaults to None.
</p>
<b>horizon (int, optional) : <i></i></b>
<p class="attr">
    Number of steps to predict into the future. Defaults to 1.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>tuple : <i></i></b>
<p class="attr">
    Tuple containing scores (MAE, RMSE, R2) and feature importances (if enabled).
</p></td>
</tr>
    </tbody>
</table>


# Wind Turbine Energy Prediction

This repository contains the materials of the term project Wind Turbine Energy Prediction of Renewable Energy Systems at the University of Tuebingen. 


## **Quick Start**
For a quick start, you can reproduce the results of the project by running the following Colab links below.




**Beberibe Colab**  --> <a href="https://colab.research.google.com/github/atahanoezer/Wind/blob/main/Notebooks/UEBB.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

**Kelmarsh Colab**  --> <a href="https://colab.research.google.com/github/atahanoezer/Wind/blob/main/Notebooks/Kelmarsh.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

**Code Documentation** --> <a href="https://atahanoezer.github.io/Wind/" target="_parent"><img src="https://img.shields.io/badge/Documentation-Click%20Here-blue"/></a>



----


## **Introduction**

This project focuses on generating accurate predictions for wind energy production from two distinct wind farms. The forecasts are required for three-time intervals: the next 10 minutes, the next hour, and the next day. To ensure high-quality results and meet the project's objectives, gradient-boosted trees are employed in conjunction with hyperparameter optimization. Additionally, feature engineering techniques and data imputation methods are utilized to enhance the accuracy of the predictions.

### **Project Structure**

The easiest way to reproduce the project is to follow the notebooks, however, one can also directly start developing using Dataset and Model classes. The Dataset class is designed for the efficient usage of memory without using replicate data frames and it also enables all kinds of feature engineering steps to be integrated into the project as simple as a function. On the developer side, this helps to prevent the side effects of mutable and reference objects. 

The Model class is just a wrapper for boosted decision trees enabling one-shot and recursive prediction without a big boilerplate code. Furthermore, all the predictions, score calculations, and visualizations are handled on the class side making the ML pipeline robust against developer mistakes. Finally, any further functionalities such as CV and hyperparam optimization can be easily integrated into the project with simple functions.


## **Datasets**

 Datasets are provided for two different wind farms. One of them is located in Beberibe, Brazil and the other one is located in Kelmarsh, UK. 
 
 The Brazilian data compilation comprises two sets of information gathered during a micrometeorological study conducted in two separate wind farms situated in a coastal region of northeastern Brazil [1]. The wind farms in question are named Pedra do Sal Wind Farm (UEPS) and Beberibe Wind Farm (UEBB). These farms are positioned along the northeast coast of Brazil, an area characterized by meteorological conditions heavily impacted by trade winds and sea breeze. Each dataset encompasses measurements collected continuously over the course of an entire year, specifically from August 2013 to July 2014. The dataset can be downloaded from [Beberibe Wind Farm](https://zenodo.org/record/1475197#.ZD6iMxXP2WC).



UK dataset encompasses information related to the Kelmarsh wind farm in the UK [2]. It includes a KMZ file for easy visualization in tools like Google Earth, as well as static data providing turbine details and coordinates. Additionally, it offers 10-minute SCADA and events data for the six Senvion MM92 turbines at Kelmarsh wind farm, organized by year from 2016 to mid-2021. The dataset is provided by Cubico Sustainable Investments Ltd under a CC-BY-4.0 open data license. The dataset can be downloaded from [UK Wind Farm](https://zenodo.org/record/5841834#.ZEajKXbP2BQ).




## **Exploratory Data Analysis**


Exploratory Data Analysis (EDA) plays a crucial role in understanding and extracting insights from datasets. One powerful tool for conducting EDA is the pandas profiling library[3]. It automates the process of generating comprehensive reports on the dataset, providing insights into its structure, statistical measures, and data quality. The reports include information on data types, missing values, correlations, distributions, outliers, and more. By using pandas profiling, analysts can efficiently identify patterns, anomalies, and data quality issues, facilitating informed decision-making in data preprocessing and modeling

EDA was performed on both datasets using the pandas profiling library. The generated reports can be found in the reports folder. Based on the reports, fields with a high number of missing values were removed, while the remaining missing values were either filled using a backward filling or mean imputation methods. Fortunately, the UK dataset providers have already prepared a set of useful columns for analysis out of the original 300 columns [4]. Nevertheless, a profile check was conducted, revealing minor issues that were addressed. Additionally, correlations between the features were examined, and features with high correlation are set to be discarded (TBD). The visualization below showcases the correlation for the UEBB dataset.

<!-- resize the image and center -->

<p align="center">
<img src="Reports/uebb_correlation.jpeg" alt="Correlation" width="550" height="400"">
</p>




## **Feature Engineering**

**TBD**

## **Modeling**


The modeling approach involves utilizing two gradient-boosted tree methods, namely Catboost and LightGBM. The Model class design allows for the flexibility to incorporate other tree-based methods if desired. Each model employs two prediction mechanisms: One-shot prediction and Recursive Prediction [5], enabling the generation of predictions for different time horizons. Hyperparameter optimization will be integrated into the current code by the second deadline of the course.

### **One Shot Prediction**

A One-shot prediction is a straightforward approach that directly predicts the target variable for a specific time step without calculating intermediate steps. In the context of wind turbine power output prediction, this methodology converts the problem into a supervised learning task. The target variable becomes the power output of the wind turbine, while the features consist of the previous power outputs of the turbine. By leveraging this method, we can predict the power output for a future time interval, such as the next 10 minutes, without needing to calculate power outputs for shorter intervals in between. This is accomplished by utilizing the past 10 minutes of data. The advantage of this approach is that it allows us to leverage previous data without being restricted by causality limitations, making it an excellent candidate for accurately predicting wind turbine power output.

### **Recursive Prediction**


A recursive prediction is a sophisticated approach that involves predicting the target variable for a specific time step by calculating intermediate steps. In the case of wind turbine power output prediction, the target variable is the power output of the turbine, while the features include the previous power outputs. However, recursive prediction differs from a one-shot prediction by requiring the calculation of power outputs for multiple time steps leading up to the desired prediction. This becomes more challenging when dealing with multivariate data because it requires the calculation of the other features for intermediate steps which means additional regressors for each feature. Consequently, the recursive prediction may not be suitable when the data heavily relies on non-target features. However, for wind turbine power output prediction, the use of univariate target data with lagged features has proven to be effective and efficient. 


### **Hyperparameter Optimization**

TBD


## **Results**

The wind turbine power output prediction models were evaluated using two datasets: UEBB and Kelmarsh with three prediction horizons such as next 10 min, the next hour, and the next day. The evaluation metrics used to assess the performance of the models were Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and R-squared (R2). The baseline results are provided by the lecture and no model information exists. Other than the baseline two modeling schemes such as one shot and recursive prediction were used to generate the results. 

 -----
  
### **UEBB Dataset**

| Metric                 | MAE        | RMSE      | R2        |
|:-----------------------|:-----------|:----------|:----------|
| Next Step Prediction   |            |            |          |
| Baseline               | 91.554     | 145.603    | -        |
| One Shot               | 34.105     | 52.417     | 0.938    |
| One Shot Feat          | 34.164     | 52.723     | 0.937    |
| One Shot Feat + Hyp-op | **33.428** | **51.545** | **0.94** ||
|---------------------	|---------	|---------	|----------	|
| Next Hour Prediction   |            |            |           |
| Baseline               | 183.286    | 263.749    | -         |
| One Shot               | 77.657     | 110.062    | 0.726     |
| One Shot Feat          | 76.401     | 107.943    | 0.737     |
| One Shot Feat + Hyp-op | 76.886     | 107.769    | 0.737     |
| Recursive              | **49.412** | **71.511** | **0.884** |
|---------------------	|---------	|---------	|----------	|
| Next Day Prediction    |             |             |           |
| Baseline               | 510.71      | 623.023     | -         |
| One Shot               | 149.102     | 186.475     | 0.209     |
| One Shot Feat          | 156.049     | 191.793     | 0.164     |
| One Shot Feat + Hyp-op | 153.75      | 189.205     | 0.186     |
| Recursive              | **107.729** | **142.285** | **0.543** |

The Next Step One Shot prediction obtains a similar result to the baseline, the table does not include the validation results but if you check the validation results from the notebook, there is a significant decrease in the performance. This is most likely caused by the size of the validation data of UEBB which is quite small and covers a very seasonal period of time. This problem will be addressed in the next deadline with robust cross-validation.

The Next Hour One Shot prediction has a similar MAE to the baseline, but it achieves a lower RMSE and MAE, indicating an improvement in prediction accuracy. The R2 value of 0.733 suggests that the model explains a substantial portion of the variance in the data. The Next Hour Recursive prediction outperforms both the baseline and the one-shot prediction in terms of MAE and RMSE, indicating a reduction in prediction errors. 

The Next Day Recursive prediction outperforms the other methods significantly, indicating improved prediction accuracy for longer time horizons. However, the R2 value of 0.495 suggests that the model's explanatory power is limited compared to short-horizon predictions.

 -----
  
### **Kelmarsh Dataset**

| Metric                 | MAE        | RMSE        | R2        |
|:-----------------------|:-----------|:------------|:----------|
| Next Step Prediction   |            |             |           |
| Baseline               | 91.554     | 145.603     | -         |
| One Shot               | 90.258     | 140.081     | 0.956     |
| One Shot Feat          | **89.849** | **139.897** | **0.956** |
| One Shot Feat + Hyp-op | 93.945     | 143.624     | 0.954     |
|---------------------	|---------	|---------	|----------	|
| Next Hour Prediction   |             |             |           |
| Baseline               | 183.286     | 263.749     | -         |
| One Shot               | 174.836     | 251.791     | 0.859     |
| One Shot Feat          | 174.404     | 251.4       | 0.859     |
| One Shot Feat + Hyp-op | 174.953     | 251.308     | 0.859     |
| Recursive              | **104.926** | **156.903** | **0.945** |
|---------------------	|---------	|---------	|----------	|
| Next Day Prediction    |             |             |           |
| Baseline               | 510.71      | 623.023     | -         |
| One Shot               | 521.039     | 627.725     | 0.124     |
| One Shot Feat          | 503.041     | 613.067     | 0.165     |
| One Shot Feat + Hyp-op | 496.411     | 606.829     | 0.182     |
| Recursive              | **163.795** | **247.326** | **0.864** |




The Next Step One Shot prediction falls back behind the baseline in terms of MAE and RMSE. A validation shortage is also observed in this dataset. This problem will be handled during the next iteration. Yet, current predictions are still good and this makes it possible to use recursive models for long horizons.

Both One shot and Recursive prediction outperforms the baseline in terms of MAE and RMSE scores. Furthermore, their R2 values suggest a good explanatory power of the models. Yet, the Recursive prediction achieves significantly lower MAE, RMSE, and R2 compared to the One Shot prediction, indicating a better representation of the longer steps.

As observed before, both one-shot and recursive predictions outperform the baseline in terms of MAE and RMSE scores. However, one-shot prediction is not quite capable of capturing daily patterns, as indicated by the R2 value of 0.306. In contrast, the recursive prediction is quite good at capturing daily patterns such that it surpasses even the hourly one-shot predictions in terms of MAE and RMSE scores. 


-----

### **Transfer Learning**

| Metric                              | MAE        | RMSE       | R2       |
|:------------------------------------|:-----------|:-----------|:---------|
| Next step Hyp-op                    | **33.428** | **51.545** | **0.94** |
| Next step Transfer Hyp-op           | 33.633     | 51.96      | 0.939    |
|---------------------	|---------	|---------	|----------	|
| Next hour Hyp-op                    | 76.886     | 107.769    | 0.737    |
| Next hour Transfer Hyp-op           | 75.559     | 106.965    | 0.741    |
| Next hour Recursive                 | **49.412**     | **71.511**     | **0.884**    |
| Next hour Recursive Transfer Hyp-op | 50.6       | 72.057     | 0.883    |
|---------------------	|---------	|---------	|----------	|
| Next day Hyp-op                     | 153.75     | 189.205    | 0.186    |
| Next day Transfer Hyp-op            | 153.96     | 188.241    | 0.194    |
| Next day Recursive                  | 107.729    | 142.285    | 0.543    |
| Next day Recursive Transfer Hyp-op  | **102.999**    | **136.213**    | **0.582**    |

-----
### **Summary**

In summary, the forecast models, especially the recursive predictions, generally outperform the baselines in terms of MAE and RMSE, indicating a better generalization than the baseline for both of the datasets. One observation is that one-shot predictions can not really outperform baselines in both datasets. I believe this is related to having a smaller validation set than the test set and the effects of this appear in the UEBB dataset more heavily. In addition, obtained results do not include the effect of hyperparameter optimization. I believe that the results can be further improved by using  hyperparameter optimization with good cross-validation.

## **References**

[1] [https://zenodo.org/record/1475197#.ZD6iMxXP2WC]( URL) 

[2] [https://zenodo.org/record/5841834#.ZEajKXbP2BQC]( URL) 

[3] [https://ydata-profiling.ydata.ai/docs/master/]( URL) 

[4] [https://github.com/charlie9578/CubicoOpenData/blob/main/Kelmarsh.ipynb]( URL) 

[5] [https://phdinds-aim.github.io/time_series_handbook/08_WinningestMethods/lightgbm_m5_forecasting.html]( URL) 


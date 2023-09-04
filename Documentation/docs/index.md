# Wind Turbine Energy Prediction

This repository contains the materials of the term project Wind Turbine Energy Prediction of Renewable Energy Systems at the University of Tuebingen. 


## **Quick Start**
For a quick start, you can reproduce the results of the project by running the following Colab links below.




**Beberibe Colab**  --> <a href="https://colab.research.google.com/github/atahanoezer/Wind/blob/main/Notebooks/UEBB.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

**Kelmarsh Colab**  --> <a href="https://colab.research.google.com/github/atahanoezer/Wind/blob/main/Notebooks/Kelmarsh.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

## **Introduction**

This project focuses on generating accurate predictions for wind energy production from two distinct wind farms. The forecasts are required for three-time intervals: the next 10 minutes, the next hour, and the next day. To ensure high-quality results and meet the project's objectives, gradient-boosted trees are employed in conjunction with hyperparameter optimization. Additionally, feature engineering techniques and data imputation methods are utilized to enhance the accuracy of the predictions.


## **Datasets**

 Datasets are provided for two different wind farms. One of them is located in Beberibe, Brazil and the other one is located in Kelmarsh, UK. 
 
 The Brazilian data compilation comprises two sets of information gathered during a micrometeorological study conducted in two separate wind farms situated in a coastal region of northeastern Brazil [1]. The wind farms in question are named Pedra do Sal Wind Farm (UEPS) and Beberibe Wind Farm (UEBB). These farms are positioned along the northeast coast of Brazil, an area characterized by meteorological conditions heavily impacted by trade winds and sea breeze. Each dataset encompasses measurements collected continuously over the course of an entire year, specifically from August 2013 to July 2014. The dataset can be downloaded from [Beberibe Wind Farm](https://zenodo.org/record/1475197#.ZD6iMxXP2WC).



UK dataset encompasses information related to the Kelmarsh wind farm in the UK [2]. It includes a KMZ file for easy visualization in tools like Google Earth, as well as static data providing turbine details and coordinates. Additionally, it offers 10-minute SCADA and events data for the six Senvion MM92 turbines at Kelmarsh wind farm, organized by year from 2016 to mid-2021. The dataset is provided by Cubico Sustainable Investments Ltd under a CC-BY-4.0 open data license. The dataset can be downloaded from [UK Wind Farm](https://zenodo.org/record/5841834#.ZEajKXbP2BQ).
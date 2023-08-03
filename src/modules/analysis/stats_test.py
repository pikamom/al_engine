import logging
import os
from datetime import datetime, timedelta
from typing import Dict
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import requests
from scipy import stats
import numpy as np
from matplotlib.pyplot import figure
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import adfuller
from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class StatsTest(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in cleaned dataframe")
        clean_df=pd.read_csv("data/processed/cleaned_data.csv")
        merged_scaled=pd.read_csv("data/processed/scaled_cleaned_data.csv").set_index("DATE") # change name later on
   

        logger.info("Use t-test to test the coefficients' significance")
        corr_matrix = merged_scaled.corr()

        n = len(corr_matrix["AL_PRICE"])
        degrees_of_freedom = n - 2 
        alpha = 0.05
        logger.info(f"{n} number of [AL_PRICE] present, dof = {degrees_of_freedom}, sig level = {alpha}")


        variable_names = corr_matrix["AL_PRICE"].index
        logger.info(f"Variables present in [corr_matirx] are [{variable_names}]")

        logger.debug("Perform the t-test for each correlation coefficient")
        for i, correlation in enumerate(corr_matrix["AL_PRICE"]):
            logger.debug("Convert the correlation to a z-score using Fisher's r-to-z transformation")
            logger.info("This is required to make the correlation values approximately normally distributed")
            z_score = np.arctanh(correlation)
            
            logger.debug("Calculate the standard error for the z-score")
            standard_error = 1 / np.sqrt(n - 3)
            
            logger.debug("Calculate the t-statistic")
            t_stat = z_score / standard_error
            
            logger.debug("Calculate the p-value")
            p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), degrees_of_freedom))
            
            logger.debug("Check if the correlation is significant")
            if p_value < alpha:
                print(f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} and is significant.")
            else:
                print(f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} but is not.")


        
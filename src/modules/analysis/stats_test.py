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
        al_correlation_values=corr_matrix["AL_PRICE"]
        logger.info(f"Variables present in [corr_matirx] are {list(variable_names)}")

        logger.debug("Perform the t-test for each correlation coefficient")
        list_p_values=[]
        list_decisions=[]
        for i, correlation in enumerate(al_correlation_values):
            logger.debug("Convert the correlation to a z-score using Fisher's r-to-z transformation")
            z_score = np.arctanh(correlation)
            
            logger.debug("Calculate the standard error for the z-score")
            standard_error = 1 / np.sqrt(n - 3)
            
            logger.debug("Calculate the t-statistic")
            t_stat = z_score / standard_error
            
            logger.debug("Calculate the p-value")
            p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), degrees_of_freedom))
            list_p_values.append(p_value)
            
            logger.debug("Check if the correlation is significant")
            if p_value < alpha:
                logger.info(f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} and is significant.")
                list_decisions.append("significant")
            else:
                logger.info(f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} but is not significant")
                list_decisions.append("insignificant")

        logger.info(f"Making a t-test dataframe for results")
        t_test_results=pd.DataFrame({"Variable_Name": variable_names, "Correlation":al_correlation_values,"P_Value":list_p_values,f"Test_Result_Alpha_{alpha}": list_decisions})
        Saver.save_csv(t_test_results, "t_test", "results")

        
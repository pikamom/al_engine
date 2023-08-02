import logging
import os
from datetime import datetime, timedelta
from typing import Dict

import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import requests
from matplotlib.pyplot import figure

from sklearn.preprocessing import MinMaxScaler

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class Scaling(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in cleaned dataframe")
        raw_df=pd.read_csv("data/processed/cleaned_data.csv")

        merged_11 = raw_df
        logger.info("Starting min-max scaling process")
        scaler = MinMaxScaler()

        logger.debug("Fit and transform the explainary variables dataframe with the scaler")
        merged_copy=merged_11.copy()
        merged_copy=merged_copy.set_index('DATE')
        merged_scaled = pd.DataFrame(scaler.fit_transform(merged_copy), columns=merged_copy.columns)
        merged_scaled['DATE']=merged_11['DATE']

        logger.debug("Dropping rows with missing values as a result of RSI calculation")
        merged_scaled=merged_scaled.dropna(subset=["RSI"])

        Saver.save_csv(merged_scaled, "scaled_cleaned_data", "processed")
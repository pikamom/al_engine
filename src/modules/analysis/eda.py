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


class EDA(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in cleaned dataframe")
        raw_df=pd.read_csv("data/processed/cleaned_data.csv")

        logger.info("Starting min-max scaling process")
        scaler = MinMaxScaler()

        logger.debug("Fit and transform the explainary variables dataframe with the scaler")
        copy_raw_df=raw_df.copy()
        copy_raw_df=copy_raw_df.set_index('DATE')
        scaled_df = pd.DataFrame(scaler.fit_transform(copy_raw_df), columns=copy_raw_df.columns)
        scaled_df['DATE']=raw_df['DATE']

        logger.debug("Dropping rows with missing values as a result of RSI calculation")
        scaled_df=scaled_df.dropna(subset=["RSI"])

        Saver.save_csv(scaled_df, "scaled_cleaned_data", "processed")
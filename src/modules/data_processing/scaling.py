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
        clean_df=pd.read_csv("data/processed/cleaned_data.csv")

        print(clean_df)

        logger.info("Starting min-max scaling process")
        scaler = MinMaxScaler()

        logger.debug("Fit and transform the explainary variables dataframe with the scaler")
        copy_clean_df=clean_df.copy()
        copy_clean_df=copy_clean_df.set_index('DATE')
        scaled_df = pd.DataFrame(scaler.fit_transform(copy_clean_df), columns=copy_clean_df.columns)
        scaled_df['DATE']=clean_df['DATE']

        print(scaled_df)

        Saver.save_csv(scaled_df, "scaled_cleaned_data", "processed")
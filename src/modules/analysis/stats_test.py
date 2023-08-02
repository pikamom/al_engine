import logging
import os
from datetime import datetime, timedelta
from typing import Dict
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import requests
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
   


        
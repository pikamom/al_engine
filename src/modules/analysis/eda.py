import logging
import os
from datetime import datetime, timedelta
from typing import Dict

import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import requests
from matplotlib.pyplot import figure
import plotly.express as px
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
        clean_df=pd.read_csv("data/processed/cleaned_data.csv")
        merged_scaled=pd.read_csv("data/processed/scaled_cleaned_data.csv")

        logger.info("Giving a line plot on all features")
        fig = px.line(merged_scaled.drop('DATE',axis=1), facet_col="variable", facet_col_wrap=3,
                    width=1000, height=1200, facet_row_spacing=0.02)  
        Saver.save_plots("line_plot")
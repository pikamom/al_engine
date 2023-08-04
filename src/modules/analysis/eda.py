import logging
import os
from datetime import datetime, timedelta
from typing import Dict
import seaborn as sns
import matplotlib.pyplot as plt
import plotly
import missingno as msno
import pandas as pd
import requests
from matplotlib.pyplot import figure
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.stattools import adfuller
from src.modules.base import Module
from src.utils.saver import Saver
from src.utils.settings import SETTINGS

logger = logging.getLogger("al_engine")


class EDA(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in cleaned dataframe")
        clean_df=pd.read_csv("data/processed/cleaned_data.csv")
        merged_scaled=pd.read_csv("data/processed/scaled_cleaned_data.csv").set_index("DATE") # change name later on

        logger.info("Giving a line plot on all features")
        logger.warn("Need to fix the plot saving")
        fig = px.line(merged_scaled, facet_col="variable", facet_col_wrap=3,
                    width=1000, height=1200, facet_row_spacing=0.02)
        plotly.offline.plot(fig, filename=f'{SETTINGS.run_meta_data.run_folder_path}/plots/line_plot.html')
        plt.clf()

        logger.info("Giving a correlation plot on all features")
        corr_matrix = merged_scaled.corr()
        fig, ax = plt.subplots(figsize=(8,8))
        ax_heatmap = sns.heatmap(
            corr_matrix, 
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 170, n=200),
            square=True
        )
        ax_heatmap.set_xticklabels(
            ax_heatmap.get_xticklabels(),
            rotation=90,
            horizontalalignment='right'
        )
        Saver.save_plots("correlation_plot")
        plt.clf()

        logger.info("Outputing actual correlation to logging")
        corr_info=corr_matrix["AL_PRICE"].sort_values(ascending=False)
        logger.info(f"""Correlation info: [
                    {corr_info}
                    ]""")


        
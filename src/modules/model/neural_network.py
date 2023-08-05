import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.linear_model import Lasso, LassoCV, LinearRegression, Ridge, RidgeCV
from sklearn.model_selection import TimeSeriesSplit

from src.modules.base import Module
from src.utils.model_measurement import calculate_performance_metrics
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class NeuralNetworkModel(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in training datasets from unshifted data")
        clean_scaled_data = pd.read_csv("data/processed_scaled_clean_data.csv")

        X_train, y_train, X_test, y_test = self._get_data(
            self.settings["model"]["network_model"]["cut_off_trading_day"],
            self.settings["model"]["network_model"]["prediction_num_days"],
            clean_scaled_data,
        )

    def _get_data(self, cut_off_trading_day, prediction_num_days, data):
        logger.info("Dropping the date columns")
        data_no_date = data.drop("DATE", axis=1)

        logger.info("Obtaining the training dataframe and testing dataframe")
        training_df = data_no_date.head(cut_off_trading_day)
        testing_df = data_no_date.iloc[
            cut_off_trading_day : cut_off_trading_day + prediction_num_days
        ]

        logger.info("Creating predictors and target variables dataset")
        X_train = training_df.drop(["AL_PRICE"], axis=1).set_index("DATE")
        y_train = training_df["AL_PRICE"]
        X_test = testing_df.drop(["AL_PRICE"], axis=1).set_index("DATE")
        y_test = testing_df["AL_PRICE"]

        logger.info("Converting to tensors, except for y_test")
        X_train = tf.convert_to_tensor(X_train.to_numpy())
        y_train = tf.convert_to_tensor(y_train.to_numpy())
        X_test = tf.convert_to_tensor(X_test.to_numpy())

        return X_train, y_train, X_test, y_test

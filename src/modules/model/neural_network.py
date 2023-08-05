import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import LSTM, Dense
from keras.models import Sequential
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

        logger.debug("Getting the training and testing data")
        X_train, y_train, X_test, y_test = self._get_data(
            self.settings["model"]["network_model"]["cut_off_trading_day"],
            self.settings["model"]["network_model"]["prediction_num_days"],
            clean_scaled_data,
        )

        logger.debug("Running the LSTM model for difference structure")
        for model_type in [1, 2, 3]:
            logger.debug(f"Getting the model architecture part [{model_type}]")
            model = self._get_lstm_model(model_type)

            logger.debug("Training Model")
            model.compile(optimizer="adam", loss="mse")
            model.fit(
                X_train,
                y_train,
                epochs=self.settings["model"]["network_model"]["epoches"],
                batch_size=self.settings["model"]["network_model"]["batch_size"],
                verbose=0,
            )

    def _get_lstm_model(slef, type):
        if type == 1:
            model = Sequential()
            model.add(LSTM(64))
            model.add(Dense(4))
            model.add(Dense(1))
        elif type == 2:
            model = Sequential()
            model.add(LSTM(64))
            model.add(Dense(16))
            model.add(Dense(4))
            model.add(Dense(1))
        elif type == 3:
            model = Sequential()
            model.add(LSTM(64))
            model.add(Dense(32))
            model.add(Dense(16))
            model.add(Dense(8))
            model.add(Dense(4))
            model.add(Dense(1))
        else:
            raise NotImplementedError
        return model

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

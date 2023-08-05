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

        logger.debug("Running the LSTM model for difference structure")
        lstm_y_pred_test = []
        for model_type in [1, 2, 3]:
            for num_interval, incremental_trading_day in enumerate(
                np.arange(
                    0,
                    631,
                    self.settings["model"]["network_model"]["prediction_num_days"],
                )
            ):
                logger.info("Get the cut of trading day")
                cut_off_trading_day = (
                    self.settings["model"]["network_model"]["start_cut_off_trading_day"]
                    + incremental_trading_day
                )
                logger.debug(
                    f"For number of interval = [{num_interval}], the trading day cut off is [{cut_off_trading_day}]"
                )

                logger.debug("Getting the training and testing data")
                X_train, y_train, X_test, y_test = self._get_data(
                    cut_off_trading_day,
                    self.settings["model"]["network_model"]["prediction_num_days"],
                    clean_scaled_data,
                )
                logger.info(f"Use LSTM model type {model_type} for al price prediction")
                results_in_time_interval = self._run_lstm_model(
                    model_type, X_train, y_train, X_test, y_test
                )

                logger.info(
                    "Appending model prediction results with in the time interval to prediction results list"
                )
                lstm_y_pred_test.append(results_in_time_interval)

            logger.info("Making prediction plots")
            plt.plot(
                np.arange(len(lstm_y_pred_test)),
                lstm_y_pred_test,
                label=f"model_structure_type_{model_type}",
            )
            plt.plot(np.arange(len(y_test)), y_test, label="actual")
            plt.legend()
            plt.title(f"LSTM Out-of-Sample Forecasts For Structure Type {model_type}")
            Saver.save_plots(f"lstm_type_{model_type}_test_prediction_out_of_sample")
            plt.clf()

            logger.info("Give model performance metrics")
            lstm_performance_test = calculate_performance_metrics(
                y_test, lstm_y_pred_test
            )

            logger.info("Convert results to dataframe and save it")
            test_results = pd.DataFrame.from_dict(
                lstm_performance_test, orient="index"
            ).reset_index()
            test_results.columns = ["item", "value"]
            Saver.save_csv(
                test_results, f"lstm_type_{model_type}_test_results", "modelling"
            )

    def _run_lstm_model(self, model_type, X_train, y_train, X_test, y_test):
        logger.debug(f"Getting the model architecture part [{model_type}]")
        model = self._get_lstm_model(model_type)

        logger.info("Training Model")
        model.compile(optimizer="adam", loss="mse")
        model.fit(
            X_train,
            y_train,
            epochs=self.settings["model"]["network_model"]["epoches"],
            batch_size=self.settings["model"]["network_model"]["batch_size"],
            verbose=0,
        )

        logger.info("Making predictions using the trained model and output results")
        lstm_predictions_test = model.predict(X_test)
        results_in_time_interval = [i[0] for i in lstm_predictions_test]

        return results_in_time_interval

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

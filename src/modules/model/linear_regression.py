import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.modules.base import Module
from src.utils.model_measurement import calculate_performance_metrics
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class LinearRegModel(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in training datasets from shifted data")
        training_df_shifted = pd.read_csv("data/modelling/training_shifted.csv")
        testing_df_shifted = pd.read_csv("data/modelling/testing_shifted.csv")

        logger.info("Creating predictors and target variables dataset")
        X_train = training_df_shifted.drop(["SHIFTED_PRICE"], axis=1).set_index("DATE")
        y_train = training_df_shifted["SHIFTED_PRICE"]
        X_test = testing_df_shifted.drop(["SHIFTED_PRICE"], axis=1).set_index("DATE")
        y_test = testing_df_shifted["SHIFTED_PRICE"]

        logger.info("Fitting the linear regression model")
        linear = LinearRegression()
        linear.fit(X_train, y_train)

        logger.info("Giving predictions from a linear model")
        pred_linear_test = linear.predict(X_test)
        pred_linear_train = linear.predict(X_train)

        logger.info("Calculating performances metrics")
        linear_train_performance = calculate_performance_metrics(y_train, pred_linear_train)
        linear_test_performance = calculate_performance_metrics(y_test, pred_linear_test)

        logger.info("Putting results into dataframe")
        train_results = pd.DataFrame.from_dict(
            linear_train_performance, orient="index"
        ).reset_index()
        test_results = pd.DataFrame.from_dict(linear_test_performance, orient="index").reset_index()
        train_results.columns = ["item", "value"]
        test_results.columns = ["item", "value"]

        Saver.save_csv(train_results, "linear_regression_train_results", "modelling")
        Saver.save_csv(test_results, "linear_regression_test_results", "modelling")

        logger.info(
            f"Scaled Dataset: Linear Regression: In-Sample Error: [{linear_train_performance}]"
        )
        logger.info(f"Out-of-Sample Error: [{linear_test_performance}]")

        logger.info("Plotting prediction and results")
        plt.plot(np.arange(len(pred_linear_test)), pred_linear_test, label="Prediction")
        plt.plot(np.arange(len(y_test)), y_test, label="actual")
        plt.legend()
        plt.title("Linear Regression Out-of-Sample Forecast")
        Saver.save_plots("model/linear_regression")
        plt.clf()

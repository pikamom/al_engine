import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import arange
from sklearn.linear_model import Lasso, LassoCV, LinearRegression, Ridge, RidgeCV
from sklearn.model_selection import TimeSeriesSplit

from src.modules.base import Module
from src.utils.model_measurement import calculate_performance_metrics
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class LinearModel(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.debug("Starting Linear Regression Model Building...")
        self._linear_regression()
        logger.debug("Linear regression model finished successfully")

        logger.debug("Starting Lasso Regression Model Building...")
        self._lasso_regression()
        logger.debug("Lasso regression model finished successfully")

    def _lasso_regression(self):
        logger.info("Get training and testing data")
        X_train, y_train, X_test, y_test = self._get_data()

        logger.info("Finding the best alpha values via grid search")

        alphas = 10 ** np.linspace(-5, 2, 100)
        logger.debug(f"Define the range of alpha values to test is {alphas}")
        logger.info("Splitting the data into 5 folds for validation and grid search")
        tscv = TimeSeriesSplit(n_splits=5)

        logger.info("Fit the lassco CV")
        lasso_cv = LassoCV(alphas=alphas, cv=tscv)
        lasso_cv.fit(X_train, y_train)

        best_alpha = lasso_cv.alpha_
        logger.debug(
            f"The best alpha values for lasso found via cross validation is: [{best_alpha}]"
        )

        logger.info("Re-fit the model with the best alpha value")
        lasso = Lasso(alpha=best_alpha)
        lasso.fit(X_train, y_train)

        pred_lasso = lasso.predict(X_test)
        pred_lasso_train = lasso.predict(X_train)

        logger.info("Calculate performance metrics and Putting results into dataframe")
        lasso_performance_test = calculate_performance_metrics(y_test, pred_lasso)
        lasso_performance_train = calculate_performance_metrics(y_test, pred_lasso)

        train_results = pd.DataFrame.from_dict(
            lasso_performance_train, orient="index"
        ).reset_index()
        test_results = pd.DataFrame.from_dict(
            lasso_performance_test, orient="index"
        ).reset_index()

        train_results.columns = ["item", "value"]
        test_results.columns = ["item", "value"]

        Saver.save_csv(test_results, "lasso_regression_test_results", "modelling")
        Saver.save_csv(train_results, "lasso_regression_train_results", "modelling")

        logger.info("Plotting prediction and results")
        plt.plot(np.arange(len(pred_lasso)), pred_lasso, label="Prediction")
        plt.plot(np.arange(len(y_test)), y_test, label="actual")
        plt.legend()
        plt.title("Lasso Regression Out-of-Sample Forecast")
        Saver.save_plots("lasso_regression_prediction_out_of_sample")
        plt.clf()

        plt.plot(np.arange(len(pred_lasso_train)), pred_lasso_train, label="Prediction")
        plt.plot(np.arange(len(y_train)), y_train, label="actual")
        plt.legend()
        plt.title("Lasso Regression In-Sample Prediction")
        Saver.save_plots("lasso_regression_prediction_in_sample")
        plt.clf()

    def _linear_regression(self):
        logger.info("Get training and testing data")
        X_train, y_train, X_test, y_test = self._get_data()

        logger.info("Fitting the linear regression model")
        linear = LinearRegression()
        linear.fit(X_train, y_train)

        logger.info("Giving predictions from a linear model")
        pred_linear_test = linear.predict(X_test)
        pred_linear_train = linear.predict(X_train)

        logger.info("Calculating performances metrics")
        linear_train_performance = calculate_performance_metrics(
            y_train, pred_linear_train
        )
        linear_test_performance = calculate_performance_metrics(
            y_test, pred_linear_test
        )

        logger.info("Putting results into dataframe")
        train_results = pd.DataFrame.from_dict(
            linear_train_performance, orient="index"
        ).reset_index()
        test_results = pd.DataFrame.from_dict(
            linear_test_performance, orient="index"
        ).reset_index()
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
        Saver.save_plots("linear_regression_prediction_out_of_sample")
        plt.clf()

        plt.plot(
            np.arange(len(pred_linear_train)), pred_linear_train, label="Prediction"
        )
        plt.plot(np.arange(len(y_train)), y_train, label="actual")
        plt.legend()
        plt.title("Linear Regression In-Sample Prediction")
        Saver.save_plots("linear_regression_prediction_in_sample")
        plt.clf()

    def _get_data(self):
        logger.info("Reading in training datasets from shifted data")
        training_df_shifted = pd.read_csv("data/modelling/training_shifted.csv")
        testing_df_shifted = pd.read_csv("data/modelling/testing_shifted.csv")

        logger.info("Creating predictors and target variables dataset")
        X_train = training_df_shifted.drop(["SHIFTED_PRICE"], axis=1).set_index("DATE")
        y_train = training_df_shifted["SHIFTED_PRICE"]
        X_test = testing_df_shifted.drop(["SHIFTED_PRICE"], axis=1).set_index("DATE")
        y_test = testing_df_shifted["SHIFTED_PRICE"]
        return X_train, y_train, X_test, y_test

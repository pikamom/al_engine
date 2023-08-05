import logging
import os

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class StatsTest(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Conducting t-test")
        self._t_test()
        logger.info("T-test completed successfully")

        logger.info("Conducting Granger Causality Test")
        self._granger_causality_test()
        logger.info("Granger Causality Test completed successfully")

        logger.info("Conducting ADF Test for stationarity")
        self._adf_test()
        logger.info("ADF Test completed successfully")

    def _t_test(self):
        logger.info("Reading in cleaned dataframe")
        scaled_cleaned_data = pd.read_csv(
            "data/processed/scaled_cleaned_data.csv"
        ).set_index("DATE")

        logger.info("Use t-test to test the coefficients' significance")
        corr_matrix = scaled_cleaned_data.corr()

        n = len(corr_matrix["AL_PRICE"])
        degrees_of_freedom = n - 2
        alpha = 0.05
        logger.info(
            f"{n} number of [AL_PRICE] present, dof = {degrees_of_freedom}, sig level = {alpha}"
        )

        variable_names = corr_matrix["AL_PRICE"].index
        al_correlation_values = corr_matrix["AL_PRICE"]
        logger.info(f"Variables present in [corr_matirx] are {list(variable_names)}")

        logger.debug("Perform the t-test for each correlation coefficient")
        list_p_values = []
        list_decisions = []
        for i, correlation in enumerate(al_correlation_values):
            logger.debug(
                "Convert the correlation to a z-score using Fisher's r-to-z transformation"
            )
            z_score = np.arctanh(correlation)

            logger.debug("Calculate the standard error for the z-score")
            standard_error = 1 / np.sqrt(n - 3)

            logger.debug("Calculate the t-statistic")
            t_stat = z_score / standard_error

            logger.debug("Calculate the p-value")
            p_value = 2 * (1 - stats.t.cdf(np.abs(t_stat), degrees_of_freedom))
            list_p_values.append(p_value)

            logger.debug("Check if the correlation is significant")
            if p_value < alpha:
                logger.info(
                    f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} and is significant."  # noqa
                )
                list_decisions.append("significant")
            else:
                logger.info(
                    f"Correlation between 'AL_PRICE' and '{variable_names[i]}' is {round(correlation,2)} but is not significant"  # noqa
                )
                list_decisions.append("insignificant")

        logger.info("Making a t-test dataframe for results")
        t_test_results = pd.DataFrame(
            {
                "Variable_Name": variable_names,
                "Correlation": al_correlation_values,
                "P_Value": list_p_values,
                f"Test_Result_Alpha_{alpha}": list_decisions,
            }
        )
        Saver.save_csv(t_test_results, "t_test", "results")

    def _granger_causality_test(self):
        differenced_scaled_cleaned_data = pd.read_csv(
            "data/processed/differenced_scaled_cleaned_data.csv"
        ).set_index("DATE")

        logger.info("Determine the maximum number of lags to consider")
        max_lag = min(len(differenced_scaled_cleaned_data["AL_PRICE"]) - 1, 20)

        best_lags = {}
        for var in differenced_scaled_cleaned_data.columns:
            if var == "AL_PRICE":
                continue
            logger.debug(f"Conducting test for variable {var}")

            best_lag = None
            best_p_value = float("inf")
            for lag in range(1, max_lag + 1):
                logger.debug(
                    f"Running Granger Causality test for al price with variable [{var}] and lag [{lag}]"  # noqa
                )
                results = grangercausalitytests(
                    differenced_scaled_cleaned_data[["AL_PRICE", var]], maxlag=lag
                )
                p_value = results[lag][0]["ssr_ftest"][1]

                logger.debug(
                    f"P-value is [{p_value}] and the best p value is [{best_p_value}]"
                )
                if p_value > best_p_value:
                    break

                logger.info("Update the best lag and p-value")
                best_lag = lag
                best_p_value = p_value

            logger.debug(
                f"Best lags / p-value for variable [{var}] is {(best_lag, best_p_value)}"
            )
            best_lags[var] = (best_lag, best_p_value)

        granger_causality_results = pd.DataFrame(best_lags).T.reset_index()
        granger_causality_results.columns = [
            "variable_name",
            "best_lag",
            "best_p_value",
        ]
        Saver.save_csv(
            granger_causality_results,
            "granger_causality_test_on_diff_scaled_data",
            "results",
        )

    def _adf_test(self):
        scaled_cleaned_data = pd.read_csv(
            "data/processed/scaled_cleaned_data.csv"
        ).set_index("DATE")

        p_values_list = []
        for column in scaled_cleaned_data.columns:
            logger.debug(f"Conducting ADF test for col [{column}]")
            result = adfuller(scaled_cleaned_data[column].values)

            p_value = round(result[1], 3)
            p_values_list.append(p_value)

            logger.info(f"p-value for ADF test on [{column}] is [{p_value}]")

        logger.info("Creating ADF test results dataframe")
        adf_test_results = pd.DataFrame(
            {"col_name": scaled_cleaned_data.columns, "adf_p_value": p_values_list}
        )
        Saver.save_csv(adf_test_results, "adf_test", "results")

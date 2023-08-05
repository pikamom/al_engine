import logging
import os

import pandas as pd

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class Differencing(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.info("Reading in cleaned and scaled dataframe")
        scaled_cleaned_data = pd.read_csv("data/processed/cleaned_data.csv")

        logger.info("Define columns to differencing on")
        columns_to_difference = [
            "AL_PRICE",
            "OIL_PRICE",
            "CU_PRICE",
            "SCFI_INDEX_NEW",
            "CCFI_INDEX_NEW",
            "COAL",
            "US_DOLLAR",
            "AUS_DOLLAR",
            "LONDON_AL_PRICE",
            "ACC_OPEN",
            "ACC_CLOSE",
        ]
        logger.debug(f"Selected  columns for differencing are: {columns_to_difference}")

        logger.debug(
            "Take 1st Order Differncing on chosen columns and append back other columns"
        )
        differenced_scaled_cleaned_data = (
            scaled_cleaned_data[columns_to_difference].copy().diff().dropna()
        )
        differenced_scaled_cleaned_data = differenced_scaled_cleaned_data.merge(
            scaled_cleaned_data[
                [
                    "AL_VOLATILITY",
                    "ACC_CHANGE_WITHIN_A_DAY",
                    "ACC_CHANGE_ACROSS_DAYS",
                    "ACC_VOLUME",
                    "DATE",
                ]
            ],
            left_index=True,
            right_index=True,
        )

        Saver.save_csv(
            differenced_scaled_cleaned_data,
            "differenced_scaled_cleaned_data",
            "processed",
        )

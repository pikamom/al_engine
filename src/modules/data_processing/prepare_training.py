import logging
import os

import pandas as pd

from src.modules.base import Module
from src.utils.saver import Saver

logger = logging.getLogger("al_engine")


class PrepareTraining(Module):
    def __init__(self) -> None:
        module_name = os.path.basename(__file__).replace(".py", "")
        super().__init__(module_name)

    def run(self):
        logger.debug("Reading in cleaned scaled dataframe")
        scaled_cleaned_data = pd.read_csv("data/processed/scaled_cleaned_data.csv")

        logger.info("Creating training dataframe for non-shifted al price")
        training_unshifted, testing_unshifted = self._split_train_test_data(
            scaled_cleaned_data
        )

        logger.debug(
            f'Creating shifted price dataframe with shift = [{self.settings["model"]["data"]["shift"]}]'
        )
        shifted_df = scaled_cleaned_data.copy()
        shifted_df["SHIFTED_PRICE"] = scaled_cleaned_data["AL_PRICE"].shift(
            self.settings["model"]["data"]["shift"]
        )
        shifted_df = shifted_df.dropna().reset_index(drop=True)
        training_shifted, testing_shifted = self._split_train_test_data(shifted_df)

        logger.info("Saving all created modelling data files")
        Saver.save_csv(training_unshifted, "training_unshifted", "modelling")
        Saver.save_csv(testing_unshifted, "testing_unshifted", "modelling")
        Saver.save_csv(training_shifted, "training_shifted", "modelling")
        Saver.save_csv(testing_shifted, "testing_shifted", "modelling")

    def _split_train_test_data(self, data):
        logger.debug(
            f'Taking training dataframe to be trading days before [{self.settings["model"]["data"]["training_end_date"]}]'
        )
        training_df = data[
            data["DATE"] < self.settings["model"]["data"]["training_end_date"]
        ]
        testing_df = data[
            data["DATE"] >= self.settings["model"]["data"]["training_end_date"]
        ]
        return training_df, testing_df

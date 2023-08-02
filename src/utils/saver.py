import logging

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.settings import SETTINGS

logger = logging.getLogger("al_engine")


class Saver:
    def __init__(self) -> None:
        pass

    @staticmethod
    def save_csv(df_to_save: pd.DataFrame, filename: str, type: str = "raw"):
        if filename[-4:] != ".csv":
            logger.debug(
                "The filename does not contain .csv as file extension, adding .csv..."
            )
            filename = filename + ".csv"

        logger.debug(
            f"Saving file with file name [{filename}] at location [data/{type}/{filename}]..."
        )
        df_to_save.to_csv(f"data/{type}/{filename}", index=False)
        logger.info("Save successful!")

    @staticmethod
    def save_plots(filename: str, extension: str = ".png"):
        if filename[-4:] != extension:
            logger.debug(
                f"The filename does not contain specified extension, adding {extension}..."
            )
            filename = filename + extension

        logger.debug(
            f'Saving file with file name [{filename}] at location [{SETTINGS["run_meta_data"]["run_folder_path"]}/plots]...'
        )
        plt.savefig(
            f'{SETTINGS["run_meta_data"]["run_folder_path"]}/plots/{filename}', dpi=300
        )
        logger.info("Save successful!")

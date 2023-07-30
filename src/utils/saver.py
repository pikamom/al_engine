import pandas as pd
import logging

logger=logging.getLogger()


class Saver:
    def __init__(self) -> None:
        pass

    @staticmethod
    def save_csv(df_to_save: pd.DataFrame, filename: str):

        if filename[-4:] != ".csv":
            logger.debug("The filename does not contain .csv as file extension, adding .csv...")
            filename=filename+".csv"
        
        logger.debug(f"Saving file with file name [{filename}] at location [src/data/{filename}]...")
        df_to_save.to_csv(f"src/data/{filename}")
        logger.info("Save successful!")
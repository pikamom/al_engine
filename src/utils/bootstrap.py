import logging
import os
import textwrap
import uuid
from datetime import datetime
from typing import Union

from src.utils.logger import LoggerSetup
from src.utils.settings import SETTINGS

logger = logging.getLogger("al_engine")


def Boostrap() -> None:
    # run meta data
    run_id, time_now, run_folder_path, log_file = create_run_meta_data()

    # make folders
    os.makedirs(run_folder_path)
    os.makedirs(f"{run_folder_path}/logs")
    os.makedirs(f"{run_folder_path}/plots")

    # set up logger
    LoggerSetup(log_file=log_file)

    logger_message = f"""

    ###########################
    Boostrap task in progress...
    run id: {run_id}
    run start time: {time_now}
    run folder created at: {run_folder_path}
    ###########################
    """

    # log the run meta data
    logger_message = textwrap.dedent(logger_message)
    logger.debug(logger_message)


def create_run_meta_data() -> Union[str, str, str, str]:
    run_id = uuid.uuid4()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_date = datetime.now().strftime("%Y%m%d")
    run_folder_path = f"runs/{today_date}/{run_id}"
    log_file = f"{run_folder_path}/logs/run.log"

    run_meta_data = {
        "run_id": run_id,
        "start_time": time_now,
        "today_date": today_date,
        "run_folder_path": run_folder_path,
        "log_file": log_file,
    }

    SETTINGS["run_meta_data"] = run_meta_data

    return run_id, time_now, run_folder_path, log_file

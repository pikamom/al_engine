from src.utils.logger import LoggerSetup
from datetime import datetime
import os
import uuid
import logging
import textwrap

logger=logging.getLogger()

def Boostrap():

    # run meta data
    run_id=uuid.uuid4()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_date=datetime.now().strftime("%Y%m%d")
    run_folder_path=f"runs/{today_date}/{run_id}"
    log_file=f"{run_folder_path}/logs/run.log"
    
    # make a run folder + logs folder within the run folder
    os.makedirs(f"runs/{today_date}/{run_id}")
    os.makedirs(f"runs/{today_date}/{run_id}/logs")

    # set up logger
    LoggerSetup(log_file=log_file)

    logger_message=f"""

    ###########################
    Boostrap task in progress...
    run id: {run_id}
    run time: {time_now}
    run folder created at: {run_folder_path}
    log file stored in: {log_file}
    ###########################
    """

    # log the run meta data
    logger_message = textwrap.dedent(logger_message)
    logger.debug(logger_message)




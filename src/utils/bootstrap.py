from src.utils.logger import LoggerSetup
from datetime import datetime
import os
import uuid
import logging
import textwrap

logger=logging.getLogger()
LoggerSetup()

def Boostrap():
    # run meta data
    run_id=uuid.uuid4()
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_date=datetime.now().strftime("%Y%m%d")

    logger_message=f"""
    ###########################
    Boostrap task in progress...
    run id: {run_id}
    run time: {time_now}
    run folder created at: runs/{today_date}/{run_id}
    ###########################
    """

    # log the run meta data
    logger_message = textwrap.dedent(logger_message)
    logger.debug(logger_message)

    # make a run folder
    logger.info(f"Creating the run folder at [runs/{today_date}/{run_id}]")
    os.makedirs(f"runs/{today_date}/{run_id}")
    
    logger.debug("Boostrap task completed successfully!")




import importlib
import importlib.util
import logging
import textwrap
from datetime import datetime

import click
import yaml

from src.utils.settings import SETTINGS

logger = logging.getLogger("al_engine")


class Orchestrator:
    @click.command()
    @click.argument("orc", type=str)
    def run_orchestartion(orc):
        logger.info("Loading in config files from src/config.yaml...")
        with open("src/config.yaml", "r") as file:
            settings = yaml.safe_load(file)

        logger.info("Reading orchestration file path")
        paths_to_orchestrate = f'{settings["orchestration"]["folder_path"]}/{orc}.py'
        logger.debug(f"Using [{paths_to_orchestrate}] file to obtain a list of modules")

        logger.debug("Loading the [list_modules] variable from orchestration file...")
        module_spec = importlib.util.spec_from_file_location(orc, paths_to_orchestrate)
        orchestrator_file = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(orchestrator_file)

        logger.info("Loading is successful!")
        list_modules_name = [
            module.__name__ for module in orchestrator_file.list_modules
        ]
        logger.debug(
            f"The list of modules that will be executed are {list_modules_name}"
        )

        logger.info("Starting all modules execution...")
        for module in orchestrator_file.list_modules:
            logger.info(f"Queueing modules execution for module [{module}]...")
            module()._run()

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger_message = f"""

        ###########################
        All modules' execution completed and are successful!
        run id: {SETTINGS["run_meta_data"]["run_id"]}
        run start time: {SETTINGS["run_meta_data"]["start_time"]}
        run finish time: {time_now}
        ###########################
        """

        # log the run meta data
        logger_message = textwrap.dedent(logger_message)
        logger.debug(logger_message)

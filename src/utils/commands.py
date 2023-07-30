import importlib
import importlib.util
import yaml
import click
import logging

logger = logging.getLogger()


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
        logger.debug("All modules execution complete and is successful!")

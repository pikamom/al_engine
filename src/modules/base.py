import logging
from abc import abstractmethod, ABC
import textwrap
import yaml

logger = logging.getLogger()


class Module(ABC):
    def __init__(self, module_name) -> None:
        self.module_name = module_name
        with open("src/config.yaml","r") as file:
            self.settings=yaml.safe_load(file)

    @abstractmethod
    def run(self) -> None:
        pass

    def _run(self):
        logger_message=f"""
        ###########################
        Starting modules [{self.module_name}]...
        ###########################
        """
        logger_message = textwrap.dedent(logger_message)
        logger.debug(logger_message)

        self.run()

        logger_message=f"""
        ###########################
        Modules [{self.module_name}] completed successfully!
        ###########################
        """
        logger_message = textwrap.dedent(logger_message)
        logger.debug(logger_message)

        pass

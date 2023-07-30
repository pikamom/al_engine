import logging
import textwrap
from abc import ABC, abstractmethod

from src.utils.settings import SETTINGS

logger = logging.getLogger("al_engine")


class Module(ABC):
    def __init__(self, module_name) -> None:
        self.module_name = module_name
        self.settings = SETTINGS

    @abstractmethod
    def run(self) -> None:
        pass

    def _run(self):
        logger_message = f"""
        
        ######################################################
        Starting modules [{self.module_name}]...
        ######################################################
        """
        logger_message = textwrap.dedent(logger_message)
        logger.debug(logger_message)

        self.run()

        logger_message = f"""

        ######################################################
        Modules [{self.module_name}] completed successfully!
        ######################################################
        """
        logger_message = textwrap.dedent(logger_message)
        logger.debug(logger_message)

        pass

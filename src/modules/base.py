import logging
from abc import abstractmethod, ABC
import os

import src.utils.logger

logger = logging.getLogger()


class Module(ABC):
    def __init__(self,module_name) -> None:
        self.module_name=module_name
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    def _run(self):
        logger.info(f"Start of module {self.module_name}...")

        self.run()

        logger.info(f"End of module {self.module_name}...")

        pass

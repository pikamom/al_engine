import logging
from abc import abstractmethod, ABC
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

        # log the run meta data
        logger.debug(logger_message)

        self.run()

        logger.info(f"End of module {self.module_name}...")

        pass

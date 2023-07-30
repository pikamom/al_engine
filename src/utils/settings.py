import yaml

class LoadSetting:

    def __init__(self) -> None:
        pass

    @staticmethod
    def loadconfig():
        with open("src/config.yaml","r") as file:
            settings=yaml.safe_load(file)
        return settings
        
SETTINGS=LoadSetting.loadconfig()
from abc import abstractmethod


class Orchestrate:
    def __init__(self, list_modules: list):
        self.list_modules = list_modules

    @abstractmethod
    def run(self):
        pass

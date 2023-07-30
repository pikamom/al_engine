from abc import abstractmethod
import click

class Orchestrate:
    def __init__(self, list_modules: list):
        self.list_modules = list_modules

    @click.command()
    @click.argument('module_name',type=str)
    @abstractmethod
    def run(self, module_name):
        print(module_name)
        pass

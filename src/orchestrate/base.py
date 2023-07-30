from abc import abstractmethod
import yaml
import click

class Orchestrate:

    @click.command()
    @click.argument('orchestration_name',type=str)
    def run_orchestartion(orchestration_name):
        list_modules=


    
from abc import abstractmethod
import click

class Orchestrate:
    # def __init__(self, list_modules: list):
    #     self.list_modules = list_modules
    @abstractmethod
    def run(self, module_name):
        print(module_name)
        pass

    @click.command()
    @click.argument('module_name',type=str)
    def run_orchestartion(self, module_name):
        self.run()

    
class TTT:

    @click.command()
    @click.argument('module_name',type=str)
    def run_orchestartion(module_name):
        print(module_name)

TTT.run_orchestartion()
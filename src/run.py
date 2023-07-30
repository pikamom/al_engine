from src.utils.bootstrap import Boostrap
from src.utils.commands import Orchestrator


if __name__=="__main__":
    Boostrap()
    Orchestrator().run_orchestartion()
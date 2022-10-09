from abc import ABC, abstractmethod
from chronicles.chronicle_settings import ChronicleSettings


class AbstractBot(ABC):
    def __init__(self, chronicle_settings: ChronicleSettings):
        self.__chronicle_settings = chronicle_settings

    def go(self):
        self.some_abs_method()
        print("go go go")

    @abstractmethod
    def some_abs_method(self):
        pass

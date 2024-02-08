from abc import ABC, abstractmethod
from ..models.graph import Graph


class Visualizer(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def display(self, graph: Graph):
        pass
from abc import ABC, abstractmethod
from ..models.graph import Graph


class DataSource(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def provide(self, **kwargs) -> Graph:
        pass

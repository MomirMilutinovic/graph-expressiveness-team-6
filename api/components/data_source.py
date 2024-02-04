from abc import ABC, abstractmethod
from ..models.graph import Graph


class DataSource(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def provide(self) -> Graph:
        pass

    @abstractmethod
    def get_configuration_parameters(self) -> dict[str, str]:
        pass

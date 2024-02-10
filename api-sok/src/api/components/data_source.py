from abc import ABC, abstractmethod
from ..models.graph import Graph


class DataSource(ABC):
    """Abstract class representing the API of the DataSource plugins.
    In order to create a DataSource plugin you have to implement this class with all its methods and follow the instructions on how to create a plugin toml file in the readme of the repository: https://github.com/MomirMilutinovic/graph-expressiveness-team-6
    """

    @abstractmethod
    def get_name(self) -> str:
        """Fetches the display name of the plugin.

        Returns:
            str: Plugin display name
        """
        pass

    @abstractmethod
    def provide(self, **kwargs) -> Graph:
        """Provides the Graph representing the data source.

        Args:
            **kwargs: DataSource configuration arguments (dependent on the implementation)

        Returns:
            Graph: A Graph representing the DataSource data
        """
        pass

    @abstractmethod
    def get_configuration_parameters(self) -> dict[str, str]:
        """Fetches a dictionary of DataSource's configuration parameters, with each dictionary item being (key: param_name, value: type).

        Returns:
            dict[str, str]: A Dictionary representing the configuration parameters with each item being (key: param_name, value: type)
        """
        pass

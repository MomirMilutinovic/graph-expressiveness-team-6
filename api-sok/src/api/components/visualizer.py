from abc import ABC, abstractmethod
from ..models.graph import Graph


class Visualizer(ABC):
    """Abstract class representing the API of the Visualizer plugins.
    In order to create a Visualizer plugin you have to implement this class with all its methods and follow the instructions on how to create a plugin toml file in the readme of the repository: https://github.com/MomirMilutinovic/graph-expressiveness-team-6
    """

    @abstractmethod
    def get_name(self) -> str:
        """Fetches the display name of the plugin.

        Returns:
            str: Plugin display name
        """
        pass

    @abstractmethod
    def display(self, graph: Graph) -> str:
        """Provides an HTML representation of the Graph that is ready to be presented to the end user.

        Args:
            Graph: Graph that is to be displayed

        Returns:
            str: HTML representation of the graph
        """
        pass

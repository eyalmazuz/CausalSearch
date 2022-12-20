from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional

from networkx.classes.digraph import DiGraph
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

class Search(ABC):
    
    def __init__(self,
                 network: BayesianNetwork,
                 criterion: Optional[Callable[[DiGraph], bool]]=None,
                 goal_test: Optional[Callable[[DiGraph], bool]]=None,
                 scoring_function: Optional[Callable[[Any], float]]=None):
        self.network = network
        self.criterion = criterion
        self.goal_test = goal_test
        self.scoring_function = scoring_function

    @abstractmethod
    def find(self) -> DiGraph:
        raise NotImplemented

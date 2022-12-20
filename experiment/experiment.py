from typing import Any, Callable, List, Optional

import pandas as pd
from pgmpy.models.BayesianNetwork import BayesianNetwork # type: ignore

def run_experiment(network: BayesianNetwork, search_method: Any,
                   criterion: Optional[Callable[[DiGraph], bool]]=None,
                   goal_test: Optional[Callable[[DiGraph], bool]]=None,
                   scoring_function: Optional[Callable[[str, List[str]], float]]=None,
                   ):
    
    sm = search_method(network, scoring_function)

    best_graph = sm.find()

    log_results(best_grap, network['model'], scoring_function)
    

def main():
    pass

if __name__ == "__main__":
    main()

import logging 

import azure.functions as func
import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    """

    Parameters
    ----------
    context: DurableOrchestrationContext
        This context has the past history
        and the durable orchestration API's to chain a set of functions
    Returns
    -------
    final_result: str
        Returns the final result after the chain completes

    """
    pass
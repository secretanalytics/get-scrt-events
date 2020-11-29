import logging 

import azure.functions as func
import azure.durable_functions as df

async def orchestrator_function(context: df.DurableOrchestrationContext):
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
    reachable = True
    while reachable:
        try:
            await context.call_activity("NodeStatus")
            await context.call_activity("NodeNetInfo")
        except Exception as e:
            reachable = False

main = df.Orchestrator.create(orchestrator_function)
    
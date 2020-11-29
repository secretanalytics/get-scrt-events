import logging

import azure.functions as func
import azure.durable_functions as df

from shared_code import Node


async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    instance_id = await client.start_new(req.route_params["functionName"], None, None)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)
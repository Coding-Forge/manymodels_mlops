import azureml.core
from azureml.core import Workspace, Datastore
import pandas as pd
import os
from azureml.core import Webservice

from ml_service.utils.env_variables import Env

def main():

    # set up workspace
    # ws=Workspace.from_config()
    # Get the variables defined in config file .env
    e=Env()

    ws = Workspace.get(
        name=e.workspace_name,
        subscription_id=os.environ.get("SUBSCRIPTION_ID"),
        resource_group=e.resource_group,
    )

    for webservice in Webservice.list(ws):
        print('name:', webservice.name)
        if "manymodels" in webservice.name:
            Webservice(ws, name = webservice.name).delete()


if __name__ == "__main__":
    main()

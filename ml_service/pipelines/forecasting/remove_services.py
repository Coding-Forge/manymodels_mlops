import azureml.core
from azureml.core import Workspace, Datastore
import argparse
import pandas as pd
import os
from azureml.core import Webservice

from ml_service.utils.env_variables import Env

def main():

    parser = argparse.ArgumentParser("register")
    parser.add_argument(
        "--subscription_id",
        type=str,
        help="subscription id for the person or service principal"
    )
    parser.add_argument(
        "--resource_group",
        help=("what resource group does the workspace belong to")
    )
    args = parser.parse_args()    

    # set up workspace
    # ws=Workspace.from_config()
    # Get the variables defined in config file .env
    e=Env()

    ws = Workspace.get(
        name=e.workspace_name,
        subscription_id=args.subscription_id,
        resource_group=args.resource_group
    )

    for webservice in Webservice.list(ws):
        print('name:', webservice.name)
        if "manymodels" in webservice.name:
            Webservice(ws, name = webservice.name).delete()


if __name__ == "__main__":
    main()

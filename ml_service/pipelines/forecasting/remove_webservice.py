import azureml.core
from azureml.core import Workspace, Datastore
import argparse
import pandas as pd
import os
from azureml.core import Webservice

# from ml_service.utils.env_variables import Env

def main():

    print('running here')

    ws = Workspace.get(
        name='coding-forge-ml-ws',
        subscription_id=os.getenv("SUBSCRIPTION_ID"),
        resource_group='coding-forge-rg'
    )

    for webservice in Webservice.list(ws):
        print('name:', webservice.name)
        if "manymodels" in webservice.name:
            Webservice(ws, name = webservice.name).delete()


if __name__ == "__main__":
    main()

from pkg_resources import resource_isdir
from azureml.core import Workspace, Dataset

ws = Workspace.get(
    name="",
    subscription_id="",
    resource_group=""
)

datastore_name=""
# Connect to default datastore
from azureml.core import Datastore

datastore = Datastore.get(ws, datastore_name)

ds = Dataset.get_by_name(ws, name="")

download_paths = ds.download()
# download_paths

import pandas as pd

sample_data = pd.read_csv(download_paths[0])
sample_data.head(10)

sample_data.to_csv("filename.csv", index=False, header=True)
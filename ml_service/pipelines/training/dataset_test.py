# %%
from azureml.core import Workspace, Datastore, Dataset, workspace
import os

ws = Workspace.get(
    name="coding-forge-ml-ws",
    subscription_id=os.getenv("SUBSCRIPTION_ID"),
    resource_group="coding-forge-rg"
)

# %%

datastore_name = 'somethingnew'

# get existing workspace
    
# retrieve an existing datastore in the workspace by name
datastore = Datastore.get(ws, datastore_name)

# create a TabularDataset from 3 file paths in datastore
data_paths = [(datastore, 'oj_sales_data_train')]

from datetime import datetime
import time
# ds_train = ds_train.filter(ds_train)

tm = datetime.strptime("2021-11-01 00:00:00","%Y-%m-%d %H:%M:%S")

df_trainer = Dataset.Tabular.from_delimited_files(path=data_paths) \
                            .with_timestamp_columns(timestamp="Date_Time") \
                            .time_before(tm) \
                            .to_pandas_dataframe()

df_tester = Dataset.Tabular.from_delimited_files(path=data_paths) \
                           .with_timestamp_columns(timestamp="Date_Time") \
                           .time_after(tm, include_boundary=True) \
                           .to_pandas_dataframe()

# %%

ds = Dataset.Tabular.register_pandas_dataframe(Dataset.Tabular.from_delimited_files(path=data_paths) \
                    .with_timestamp_columns(timestamp="Date_Time") \
                    .time_after(tm, include_boundary=True) \
                    .to_pandas_dataframe(), datastore, "goofy", "testing this out", show_progress=True) 


# %%

display(df_trainer.tail())
display(df_tester.tail())

# %%

df_train = ds_train
df_test = ds_test
display(df_test.take(3).to_pandas_dataframe().head())


# %%

df_train = ds_train.to_pandas_dataframe()
df_test = ds_test.to_pandas_dataframe()

# %%
df_test.head()

# %%
#df = df_train['Date_Time'].apply(lambda x: x.date() <  datetime.strptime("2021-11-01","%Y-%m-%d").date())
df = df_train[df_train['Date_Time'].apply(lambda x: x.date() < datetime.strptime("2021-11-01","%Y-%m-%d").date())]

# %%

df.head()

# %%

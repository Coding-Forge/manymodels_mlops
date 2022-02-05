import argparse
import pandas as pd
from azureml.core import Run, Datastore, Dataset
from datetime import datetime
import time


run = Run.get_context()
ws = run.experiment.workspace

parser = argparse.ArgumentParser()
parser.add_argument("--split_date", type=str,  help="date you want the files split into training and testing")
parser.add_argument("--folder_name", type=str, help="name of the folder where the tabular data exists")
args = parser.parse_args()

folder_name = args.folder_name
split_date = args.split_date

# should pass this in as a variable 
datastore_name = 'somethingnew'

# retrieve an existing datastore in the workspace by name
datastore = Datastore.get(ws, datastore_name)

# create a TabularDataset from file paths in datastore
data_paths = [(datastore, folder_name)]

# create a timestamp to be used for splitting dataset
tm = datetime.strptime(split_date,"%Y-%m-%d %H:%M:%S")

df_trainer = Dataset.Tabular.from_delimited_files(path=data_paths) \
                            .with_timestamp_columns(timestamp="Date_Time") \
                            .time_before(tm) \
                            .to_pandas_dataframe()

if not (args.training_data is None):
    path=args.training_data + "/training.parquet"
    write_df = pd.DataFrame.to_parquet(path)
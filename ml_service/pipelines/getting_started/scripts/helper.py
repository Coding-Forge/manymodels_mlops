# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import pandas as pd
import shutil


def recurse_path(target_path, root=""):
        """"
        This function recursively prints all contents of a pathlib.Path object
        """
        #print_indented(target_path.name, level)
        for file in target_path.iterdir():
            if file.is_dir():
                recurse_path(file, file)
            else:
                if "azureml" in str(root):
                    continue
                if str(file.name).endswith(".csv"):
                    shutil.copyfile(root / file.name, os.path.join(os.getcwd(), "oj_sales_data",file.name))

def walk_path(directory):
    for root, dirs, files in os.walk(directory):
        path = root.split(os.sep)
        print(path)

        for dir in dirs:
            print(f"what is the directory {dir}")

        print((len(path) - 1) * '-b-', os.path.basename(root))
        for file in files:
            print(file)
            print(len(path) * '---', file)

def split_data(data_path, time_column_name, split_date):

    train_data_path = os.path.join(data_path, "upload_train_data")
    inference_data_path = os.path.join(data_path, "upload_inference_data")
    os.makedirs(train_data_path, exist_ok=True)
    os.makedirs(inference_data_path, exist_ok=True)
    print("here1")

    files_list = [os.path.join(path, f) for path, _, files in os.walk(data_path) for f in files
                  if path not in (train_data_path, inference_data_path)]

    print(f"the length of file_list is {len(files_list)}")
    print("here2a")

    for file in files_list:
        file_name = os.path.basename(file)
        print(file_name)
        file_extension = os.path.splitext(file_name)[1].lower()
        df = read_file(file, file_extension)

        print("opa1")
        before_split_date = df[time_column_name] < split_date

        print("opa2")
        train_df, inference_df = df[before_split_date], df[~before_split_date]

        write_file(train_df, os.path.join(train_data_path, file_name), file_extension)
        write_file(inference_df, os.path.join(inference_data_path, file_name), file_extension)
    print("here3")
    return train_data_path, inference_data_path


def read_file(path, extension):
    if extension == ".parquet":
        return pd.read_parquet(path)
    else:
        return pd.read_csv(path)


def write_file(data, path, extension):
    if extension == ".parquet":
        data.to_parquet(path)
    else:
        data.to_csv(path, index=None, header=True)

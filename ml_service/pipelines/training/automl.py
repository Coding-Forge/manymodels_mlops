#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft Corporation. All rights reserved.

# Licensed under the MIT License.

# ![Impressions](https://PixelServer20190423114238.azurewebsites.net/api/impressions/MachineLearningNotebooks/how-to-use-azureml/automated-machine-learning/manymodels/02_Training/02_Training_Pipeline.png)

# # Training Pipeline - Automated ML
# _**Training many models using Automated Machine Learning**_
# 
# ---
# 
# This notebook demonstrates how to train and register 11,973 models using Automated Machine Learning. We will utilize the AutoMLPipelineBuilder to parallelize the process of training 11,973 models. For this notebook we are using an orange juice sales dataset to predict the orange juice quantity for each brand and each store. For more information about the data refer to the Data Preparation Notebook.
# 
# <span style="color:red"><b>NOTE: There are limits on how many runs we can do in parallel per workspace, and we currently recommend to set the parallelism to maximum of 20 runs per experiment per workspace. If users want to have more parallelism and increase this limit they might encounter Too Many Requests errors (HTTP 429). </b></span>

# <span style="color:red"><b> Please ensure you have the latest version of the SDK to ensure AutoML dependencies are consistent.</b></span>

# In[1]:


# !pip install --upgrade azureml-sdk


# In[2]:


# !pip install --upgrade azureml-train-automl


# Install the azureml-contrib-automl-pipeline-steps package that is needed for many models.

# In[3]:


# !pip install azureml-contrib-automl-pipeline-steps


# ### Prerequisites

# At this point, you should have already:
# 
# 1. Created your AML Workspace using the [00_Setup_AML_Workspace notebook](../../00_Setup_AML_Workspace.ipynb)
# 2. Run [01_Data_Preparation.ipynb](../../01_Data_Preparation.ipynb) to create the dataset

# ## 1.0 Set up workspace, datastore, experiment

# In[4]:


import sys
import os
print(os.getcwd())
# sys.path.append("../../")
print(os.getcwd())


# In[5]:


import azureml.core
from azureml.core import Workspace, Datastore
import pandas as pd
import os
from ml_service.utils.env_variables import Env
from ml_service.utils.aml_workspace import Connect

e=Env()

# set up workspace
ws = Connect().authenticate()

# Take a look at Workspace
ws.get_details()

# set up datastores
dstore = Datastore.get(ws, e.datastore_name)

output = {}
output['SDK version'] = azureml.core.VERSION
output['Subscription ID'] = ws.subscription_id
output['Workspace'] = ws.name
output['Resource Group'] = ws.resource_group
output['Location'] = ws.location
output['Default datastore name'] = dstore.name
pd.set_option('display.max_colwidth', -1)
outputDf = pd.DataFrame(data = output, index = [''])


# In[6]:


# !pip install python-dotenv


# In[7]:


# ### Choose an experiment

# In[8]:


from azureml.core import Experiment

experiment = Experiment(ws, e.experiment_name)
print('Experiment name: ' + experiment.name)


# ## 2.0 Call the registered filedataset

# We use 11,973 datasets and AutoMLPipelineBuilder to build 11,973 time-series to predict the quantity of each store brand.

# Each dataset represents a brand's 2 years orange juice sales data that contains 7 columns and 122 rows. 

# You will need to register the datasets in the Workspace first. The Data Preparation notebook demonstrates how to register two datasets to the workspace. 
# 
# The registered 'oj_data_small' file dataset contains the first 10 csv files and 'oj_data' contains all 11,973 csv files. You can choose to pass either filedatasets_10_models_input or filedatasets_all_models_inputs in the AutoMLPipelineBuilder.
# 
# We recommend to **start with filedatasets_10_models** and make sure everything runs successfully, then scale up to filedatasets_all_models.

# In[9]:


from azureml.core.dataset import Dataset

filedst_10_models = Dataset.get_by_name(ws, name=e.dataset_name)
filedst_10_models_input = filedst_10_models.as_named_input('train_10_models')


# In[10]:


type(filedst_10_models)
filedst_10_models.take(50)


# ## 3.0 Build the training pipeline
# Now that the dataset, WorkSpace, and datastore are set up, we can put together a pipeline for training. 

# ### Choose a compute target

# Currently AutoMLPipelineBuilder only supports AMLCompute. You can change to a different compute cluster if one fails.
# 
# This is the compute target we will pass into our AutoMLPipelineBuilder.

# In[11]:


from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget

# Choose a name for your cluster.
amlcompute_cluster_name = e.compute_name

found = False
# Check if this compute target already exists in the workspace.
cts = ws.compute_targets
if amlcompute_cluster_name in cts and cts[amlcompute_cluster_name].type == 'AmlCompute':
    found = True
    print('Found existing compute target.')
    compute = cts[amlcompute_cluster_name]
    
if not found:
    print('Creating a new compute target...')
    provisioning_config = AmlCompute.provisioning_configuration(vm_size=e.vm_size,
                                                           min_nodes=e.min_nodes,
                                                           max_nodes=e.max_nodes)
    # Create the cluster.
    compute = ComputeTarget.create(ws, amlcompute_cluster_name, provisioning_config)
    
print('Checking cluster status...')
# Can poll for a minimum number of nodes and for a specific timeout.
# If no min_node_count is provided, it will use the scale settings for the cluster.
compute.wait_for_completion(show_output = True, min_node_count = None, timeout_in_minutes = 20)
    
# For a more detailed view of current AmlCompute status, use get_status().


# ## Train
# 
# This dictionary defines the [AutoML settings](https://docs.microsoft.com/en-us/python/api/azureml-train-automl-client/azureml.train.automl.automlconfig.automlconfig?view=azure-ml-py#parameters), for this forecasting task we add the name of the time column and the maximum forecast horizon.
# 
# |Property|Description|
# |-|-|
# |**task**|forecasting|
# |**primary_metric**|This is the metric that you want to optimize.<br> Forecasting supports the following primary metrics <br><i>spearman_correlation</i><br><i>normalized_root_mean_squared_error</i><br><i>r2_score</i><br><i>normalized_mean_absolute_error</i>|
# |**blocked_models**|Models in blocked_models won't be used by AutoML. All supported models can be found at [here](https://docs.microsoft.com/en-us/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.forecasting?view=azure-ml-py).|
# |**iterations**|Number of models to train. This is optional but provides customer with greater control.|
# |**iteration_timeout_minutes**|Maximum amount of time in minutes that the model can train. This is optional and depends on the dataset. We ask customer to explore a bit to get approximate times for training the dataset. For OJ dataset we set it 20 minutes|
# |**experiment_timeout_hours**|Maximum amount of time in hours that the experiment can take before it terminates.|
# |**label_column_name**|The name of the label column.|
# |**n_cross_validations**|Number of cross validation splits. Rolling Origin Validation is used to split time-series in a temporally consistent way.|
# |**enable_early_stopping**|Flag to enable early termination if the score is not improving in the short term.|
# |**time_column_name**|The name of your time column.|
# |**max_horizon**|The number of periods out you would like to predict past your training data. Periods are inferred from your data.|
# |**grain_column_names**|The column names used to uniquely identify timeseries in data that has multiple rows with the same timestamp.|
# |**partition_column_names**|The names of columns used to group your models. For timeseries, the groups must not split up individual time-series. That is, each group must contain one or more whole time-series.|
# |**track_child_runs**|Flag to disable tracking of child runs. Only best run (metrics and model) is tracked if the flag is set to False.|
# |**pipeline_fetch_max_batch_size**|Determines how many pipelines (training algorithms) to fetch at a time for training, this helps reduce throttling when training at large scale.|

# In[12]:


import logging

partition_column_names = ['Store', 'Brand']

automl_settings = {
    "task" : 'forecasting',
    "primary_metric" : 'normalized_root_mean_squared_error',
    "iteration_timeout_minutes" : 10, # This needs to be changed based on the dataset. We ask customer to explore how long training is taking before settings this value
    "iterations" : 15,
    "experiment_timeout_hours" : 1,
    "label_column_name" : 'Quantity',
    "n_cross_validations" : 3,
    # "verbosity" : logging.INFO, 
    # "debug_log": 'automl_oj_sales_debug.txt',
    "time_column_name": 'WeekStarting',
    "max_horizon" : 20,
    "track_child_runs": False,
    "partition_column_names": partition_column_names,
    "grain_column_names": ['Store', 'Brand'],
    "pipeline_fetch_max_batch_size": 15
}


# ### Build many model training steps

# AutoMLPipelineBuilder is used to build the many models train step. You will need to determine the number of workers and nodes appropriate for your use case. The process_count_per_node is based off the number of cores of the compute VM. The node_count will determine the number of master nodes to use, increasing the node count will speed up the training process.
# 
# * <b>experiment</b>: Current experiment.
# 
# * <b>automl_settings</b>: AutoML settings dictionary.
# 
# * <b>train_data</b>: Train dataset.
# 
# * <b>compute_target</b>: Compute target for training.
# 
# * <b>partition_column_names</b>: Partition column names.
# 
# * <b>node_count</b>: The number of compute nodes to be used for running the user script. We recommend to start with 3 and increase the node_count if the training time is taking too long.
# 
# * <b>process_count_per_node</b>: The number of processes per node.
# 
# * <b>run_invocation_timeout</b>: The run() method invocation timeout in seconds. The timeout should be set to maximum training time of one AutoML run(with some buffer), by default it's 60 seconds.
# 
# * <b>output_datastore</b>: Output datastore to output the training results.
# 
# * <b>train_env(Optional)</b>: Optionally can provide train environment definition to use for training.
# 
# <span style="color:red"><b>NOTE: There are limits on how many runs we can do in parallel per workspace, and we currently recommend to set the parallelism to maximum of 320 runs per experiment per workspace. If users want to have more parallelism and increase this limit they might encounter Too Many Requests errors (HTTP 429). </b></span>
# 

# In[16]:


# In[14]:


from azureml.core import Environment

env = Environment.get(ws, "AzureML-AutoML", label="Latest")
env.environment_variables = {'AZUREML_OUTPUT_UPLOAD_TIMEOUT_SEC':'7200'}


# In[17]:


from azureml.contrib.automl.pipeline.steps import AutoMLPipelineBuilder

train_steps = AutoMLPipelineBuilder.get_many_models_train_steps(experiment=experiment,
                                                                automl_settings=automl_settings,
                                                                train_data=filedst_10_models_input,
                                                                compute_target=compute,
                                                                partition_column_names=partition_column_names,
                                                                node_count=2,
                                                                process_count_per_node=8,
                                                                run_invocation_timeout=3700,
                                                                output_datastore=dstore)


# ## 4.0 Run the training pipeline

# ### Submit the pipeline to run

# Next we submit our pipeline to run. The whole training pipeline takes about 1h 11m using a STANDARD_D16S_V3 VM with our current AutoMLPipelineBuilder setting.

# In[18]:


from azureml.pipeline.core import Pipeline
#from azureml.widgets import RunDetails

pipeline = Pipeline(workspace=ws, steps=train_steps)
run = experiment.submit(pipeline, tags={"BuildId": os.environ.get("BUILDID"), "ComputeName": e.vm_size})

#RunDetails(run).show()


# You can run the folowing command if you'd like to monitor the training process in jupyter notebook. It will stream logs live while training. 
# 
# **Note**: This command may not work for Notebook VM, however it should work on your local laptop.

# In[19]:


run.wait_for_completion(show_output=True)


# Succesfully trained, registered Automated ML models. 

# ## 5.0 Review outputs of the training pipeline

# The training pipeline will train and register models to the Workspace. You can review trained models in the Azure Machine Learning Studio under 'Models'.
# If there are any issues with training, you can go to 'many-models-training' run under the pipeline run and explore logs under 'Logs'.
# You can look at the stdout and stderr output under logs/user/worker/<ip> for more details
# 

# ## 6.0 Get list of AutoML runs along with registered model names and tags

# The following code snippet will iterate through all the automl runs for the experiment and list the details.
# 
# **Framework** - AutoML, **Dataset** - input data set, **Run** - AutoML run id, **Status** - AutoML run status,  **Model** - Registered model name, **Tags** - Tags for model, **StartTime** - Start time, **EndTime** - End time, **ErrorType** - ErrorType, **ErrorCode** - ErrorCode, **ErrorMessage** - Error Message

# In[ ]:


from scripts.helper import get_training_output
import os

training_results_name = "training_results"
training_output_name = "many_models_training_output"

training_file = get_training_output(run, training_results_name, training_output_name)
all_columns = ["Framework", "Dataset", "Run", "Status", "Model", "Tags", "StartTime", "EndTime" , "ErrorType", "ErrorCode", "ErrorMessage" ]
df = pd.read_csv(training_file, delimiter=" ", header=None, names=all_columns)
training_csv_file = "training.csv"
df.to_csv(training_csv_file)
print("Training output has", df.shape[0], "rows. Please open", os.path.abspath(training_csv_file), "to browse through all the output.")


# ## 7.0 Publish and schedule the pipeline (Optional)

# ### 7.1 Publish the pipeline
# 
# Once you have a pipeline you're happy with, you can publish a pipeline so you can call it programmatically later on. See this [tutorial](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-your-first-pipeline#publish-a-pipeline) for additional information on publishing and calling pipelines.

# In[ ]:


published_pipeline = pipeline.publish(name = 'automl_train_many_models',
                                  description = 'train many models',
                                  version = '1',
                                  continue_on_step_failure = False)


# ### 7.2 Schedule the pipeline
# You can also [schedule the pipeline](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-schedule-pipelines) to run on a time-based or change-based schedule. This could be used to automatically retrain models every month or based on another trigger such as data drift.

# In[ ]:


# from azureml.pipeline.core import Schedule, ScheduleRecurrence
    
# training_pipeline_id = published_pipeline.id

# recurrence = ScheduleRecurrence(frequency="Month", interval=1, start_time="2020-01-01T09:00:00")
# recurring_schedule = Schedule.create(ws, name="automl_training_recurring_schedule", 
#                             description="Schedule Training Pipeline to run on the first day of every month",
#                             pipeline_id=training_pipeline_id, 
#                             experiment_name=experiment.name, 
#                             recurrence=recurrence)


# ## 8.0 Bookkeeping of workspace (Optional)

# ### 8.1 Cancel any runs that are running
# 
# To cancel any runs that are still running in a given experiment.

# In[ ]:


# from scripts.helper import cancel_runs_in_experiment
# failed_experiment =  'Please modify this and enter the experiment name'
# # Please note that the following script cancels all the currently running runs in the experiment
# cancel_runs_in_experiment(ws, failed_experiment)


# %%

from re import VERBOSE
from azure.devops.connection import Connection
from azure.devops.v6_0 import pipelines
from azure.devops.v6_0.build import BuildClient
from azure.devops.v6_0.pipelines import PipelinesClient

# %%

from msrest.authentication import BasicAuthentication
import pprint

# Fill in with your personal access token and org URL
personal_access_token = 'runj4dvh56yhbt2afhwzdeon6cjaav7qnockwlzivucjqhnf5zoa'
organization_url = 'https://dev.azure.com/codingforge'

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()
build_client = BuildClient(base_url=organization_url, creds=credentials)
pipelines_client = PipelinesClient(base_url=organization_url, creds=credentials)

# %%
from azure.devops.v6_0.pipelines.models import CreatePipelineParameters

pipeline_parameters = CreatePipelineParameters(folder="coding-forge",name="test")
parameters = {"projectname":"Forecast","myStringName":"this is my string"}
pipeline_parameters.from_dict(parameters)
pipelines_client.run_pipeline(run_parameters=pipeline_parameters, project="ManyModelsOps", pipeline_id=9, pipeline_version=1)

# %%

# Get the first page of projects
get_projects_response = core_client.get_projects()
index = 0
while get_projects_response is not None:
    for project in get_projects_response.value:
        pprint.pprint("[" + str(index) + "] " + project.name)
        index += 1
    if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
        # Get the next page of projects
        get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
    else:
        # All projects have been retrieved
        get_projects_response = None

# %%

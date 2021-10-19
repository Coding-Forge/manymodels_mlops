# %%

from re import VERBOSE
from azure.devops.connection import Connection
from azure.devops.v6_0 import pipelines
from azure.devops.v6_0.pipelines import PipelinesClient

# %%

#azure_devops_python_print_urls


import logging
logging.basicConfig(level=logging.DEBUG)

from msrest.authentication import BasicAuthentication
import pprint
import os

# Fill in with your personal access token and org URL
# using environment variables to prevent uploading secrets
# into the code repository
personal_access_token = os.getenv("PAT")
organization_url = os.getenv("ORGANIZATION_URL")

# %%

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)

# %%
# Get a client (the "core" client provides access to projects, teams, etc)
pipelines_client = PipelinesClient(base_url=organization_url, creds=credentials)

# %%
from azure.devops.v6_0.pipelines.models import RunPipelineParameters

logging.exception("changing parameters")

#pipeline_parameters = CreatePipelineParameters(folder="coding-forge",name="test")
parameters = {"projectname":"FB-Prophet","myStringName":"Did this really work or did this not work"}
pipeline_parameters = RunPipelineParameters(template_parameters=parameters)
pipelines_client.run_pipeline(run_parameters=pipeline_parameters, project="ManyModelsOps", pipeline_id=9)

# %%

# %%

from re import VERBOSE
from azure.devops.connection import Connection
from azure.devops.v6_0 import pipelines
from azure.devops.v6_0.build import BuildClient
from azure.devops.v6_0.pipelines import PipelinesClient

# %%

from msrest.authentication import BasicAuthentication
import pprint
import os

# Fill in with your personal access token and org URL
<<<<<<< HEAD:devops_api/get_organization_projects.py
personal_access_token = os.getenv("PAT")
organization_url = os.getenv("ORGANIZATION_URL")

# %%
=======
personal_access_token = ''
organization_url = ''
>>>>>>> master:devops_api/pipeline_build.py

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)
core_client = connection.clients.get_core_client()

# %%
# Get a client (the "core" client provides access to projects, teams, etc)

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

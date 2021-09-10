from azureml.core import Workspace
from .env_variables import Env
import os

e=Env()

class Connect:
    #def __init__(self):

    def authenticate(self, subcription_id) -> Workspace:
        return Workspace.get(
            name=e.workspace_name,
            subscription_id=subscription_id,
            resource_group=e.resource_group
       )
    
    def authenticate_with_sp():
        return None
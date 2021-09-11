from azureml.core import Workspace
from .env_variables import Env
import os

e=Env()

class Connect:
    def authenticate(self) -> Workspace:
        return Workspace.get(
            name=e.workspace_name,
            subscription_id=e.subscription_id,
            resource_group=e.resource_group
       )
    
    def authenticate_with_sp():
        pass
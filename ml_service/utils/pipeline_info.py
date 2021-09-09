
from azureml.core import Experiment, Workspace
import os
from .env_variables import Env

class Info:
    
    def __init__(self, workspace, experiment, build_id):
        self._workspace = workspace
        self._experiment = experiment
        self._build_id = build_id

    e = Env()
    

    # get an iterable of all the experiment runs by experiment name

    def get_run_id(self):
        experiment = self._experiment
        ws = self._workspace
        build_id = self._build_id
        
        experiments = Experiment.list(ws,experiment_name=experiment)

        counter=0
        # iterate over the runs in the experiment and extract only the run based on the build id 
        # of Az DevOps
        for runs in experiments:
            run = runs.get_runs(tags={"BuildId": build_id})

            # get the associated run id and also check if it loops
            # more than once. If it does then more than one pipeline
            # in the experiment has the same build id
            # This has to be done this way because once a generator is 
            # accessed you can pull any more information from it
            for item in run:
                run_id = item.id
                counter+=1

        if(counter > 1):
            published_pipeline = None
            raise Exception(f"Multiple active pipelines have the associated build {build_id}.")  # NOQA: E501
        elif(counter == 0):
            published_pipeline = None
            raise KeyError(f"Unable to find a published pipeline for this build {build_id}")  # NOQA: E501
        else:
            print("The associated run id is", run_id)
            return run_id
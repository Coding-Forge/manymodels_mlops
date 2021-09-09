# %%
from azureml.core import Experiment, Workspace
import argparse
import os

def count(iter):
    try:
        return len(iter)
    except TypeError:
        return sum(1 for _ in iter)

ws = Workspace.from_config()

# get an iterable of all the experiment runs by experiment name
experiments = Experiment.list(ws,experiment_name="manymodels-training-pipeline")
build_id = os.environ.get("BUILDID")

print(build_id)

# iterate over the runs in the experiment and extract only the run based on the build id 
# of Az DevOps
for runs in experiments:
    run = runs.get_runs(tags={"BuildId": build_id})
    for item in run:
        print(item.id)
# %%

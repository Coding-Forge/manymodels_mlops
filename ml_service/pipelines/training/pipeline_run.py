
from azureml.core import Experiment, Workspace
import argparse
import os
from ml_service.utils.env_variables import Env

def main():

    parser = argparse.ArgumentParser("register")
    parser.add_argument(
        "--output_pipeline_id_file",
        type=str,
        default="pipeline_id.txt",
        help="Name of a file to write pipeline ID to"
    )
    args = parser.parse_args()

    e = Env()

    ws = Workspace.get(
        name=e.workspace_name,
        subscription_id=os.environ.get("SUBSCRIPTION_ID"),
        resource_group=e.resource_group
    )

    # get an iterable of all the experiment runs by experiment name
    experiments = Experiment.list(ws,experiment_name=e.experiment_name)
    build_id = os.environ.get("BUILDID")

    print(build_id)
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
        # Save the Pipeline ID for other AzDO jobs after script is complete
        if args.output_pipeline_id_file is not None:
            with open(args.output_pipeline_id_file, "w") as out_file:
                out_file.write(run_id)


if __name__ == "__main__":
    main()

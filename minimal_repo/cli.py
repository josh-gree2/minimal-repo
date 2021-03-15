import docker
import logging
import os
import json

from prefect.engine.results import LocalResult
from prefect.run_configs import DockerRun

from minimal_repo import all_flows

LOCAL_CONTAINER_TAG = "local"
IMAGE_NAME = "prefect_base"
DEV_PROJECT = "dev"

def log_stdout_stream(stream):
    # pylint: disable=missing-function-docstring
    for line in stream:
        try:
            line = line.decode("utf8")
            obj = json.loads(line)
            logging.info(obj["stream"])
        except:  # pylint: disable=bare-except
            pass


client = docker.from_env().api
stream = client.build(path=".", tag=f"{IMAGE_NAME}:{LOCAL_CONTAINER_TAG}")

log_stdout_stream(stream)

for flow_name, flow in all_flows.items():
    flow.run_config = DockerRun(
        image=f"{IMAGE_NAME}:{LOCAL_CONTAINER_TAG}",
        env={"PREFECT__FLOWS__CHECKPOINTING": "true"},
    )
    flow.result = LocalResult(dir="~/results")
    flow.register(project_name=DEV_PROJECT, labels=[os.environ["SHARED_LABEL"]])

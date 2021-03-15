"""
A sample flow def
"""
from prefect import Flow
from prefect.storage import Module
from prefect.executors import LocalDaskExecutor

from minimal_repo.flow_1.tasks import foo


with Flow("test_flow") as flow:

    r1 = foo()
    r2 = foo()

flow.storage = Module(__name__)
flow.executor = LocalDaskExecutor()
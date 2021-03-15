from time import sleep

from prefect import task

@task
def foo():
    return 23
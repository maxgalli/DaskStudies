from time import sleep

"""
Module with different tasks with different levels of complexity
to perform with Dask
"""

def dummy_function(num):
    sleep(5)
    return num**2

def sleep_more(num):
    sleep(40)
    return num + 1

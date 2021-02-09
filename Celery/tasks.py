from celery import Celery
#import argparse


'''
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parallelize simple function using Celery")

    parser.add_argument(
            "--host",
            default="localhost",
            type=str,
            help="Hostname for the machine where the Redis server is running")

    parser.add_argument(
            "--port",
            default="6379",
            type=str,
            help="Port from where the Redis server accepts connections")


args = parse_arguments()
hostname = args.host
port = args.port
full_address = "redis://{}:{}".format(hostname, port)


app = Celery("tasks", broker=full_address, backend=full_address)
'''

app = Celery("tasks", broker="redis://192.33.123.23:6379", backend="redis://192.33.123.23:6379")

@app.task
def add(x, y):
    return x + y

from celery import Celery

app = Celery("tasks_with_config")
app.config_from_object("celeryconfig")

@app.task
def mul(x, y):
    return x * y

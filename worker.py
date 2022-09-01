# manage.py

import redis
from rq import Connection, Worker

def run_worker():
    redis_url = "redis://127.0.0.1:6379/0"  #app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker("default")
        worker.work()


if __name__ == "__main__":
    run_worker()
    

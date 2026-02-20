import redis 
from rq import SimpleWorker, Queue
import yaml

CONFIG = yaml.safe_load(open('config.yaml'))

conn = redis.Redis(host=CONFIG["redis"]["domain"], port=CONFIG["redis"]["port"], db=0)

if __name__ == '__main__':
    with conn:
        worker = SimpleWorker([Queue(CONFIG["redis"]["queue_name"], connection=conn)])
        worker.work()
from fastapi import FastAPI, Depends
import redis
import yaml
import uvicorn
import logging
from typing import Annotated
import rq
from tasks import random_task

# Configure the root logger
logging.basicConfig(
    level=logging.INFO, # Set the minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()] # Output logs to the console (stdout/stderr)
)

# Get a logger for your application module
logger = logging.getLogger(__name__)

#containse redis configs
config = yaml.safe_load(open('config.yaml'))

#Dependency to get a Redis connection
async def get_redis():
    logger.info("Connecting to Redis...")
    try:
        r = redis.Redis(host=config["redis"]["domain"], port=config["redis"]["port"], db=0)
        r.ping()
        logger.info("Connected to Redis successfully.")
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise Exception("Could not connect to Redis") from e
    return r

# Get the queue name from the config
QUEUE_NAME = config["redis"]["queue_name"] 

# Initialize the FastAPI application
app = FastAPI()

#Startup event to check Redis connection and log the startup process
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the FastAPI application...")

    try:
        await get_redis()
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        exit(0)

# Health check endpoint to verify that the application is running
@app.get("/health")
async def health():
    return {"status": "ok"}

# Endpoint to add a task to the Redis queue
@app.post("/add_task")
async def add_task(task_count: Annotated[int, "count of tasks"] = 0, redis: Annotated[redis.Redis | None, Depends(get_redis)] = None):
    try:
        r = rq.Queue(QUEUE_NAME, connection=redis)
        for _ in range(task_count):
            job = r.enqueue(random_task)
            logger.info(f"Added task: {job.id}")
        return {"message": f"{task_count} tasks added successfully."}
    except Exception as e:
        logger.error(f"Failed to add task: {e}")
        return {"error": "Failed to add task"}

@app.get("/len_queue")
async def len_queue(redis: Annotated[redis.Redis, Depends(get_redis)]):
    try:
        r = rq.Queue(QUEUE_NAME, connection=redis)
        length = r.count
        logger.info(f"Queue length: {length}")
        return {"queue_length": length}
    except Exception as e:
        logger.error(f"Failed to get queue length: {e}")
        return {"error": "Failed to get queue length"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
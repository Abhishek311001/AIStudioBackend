from fastapi import APIRouter, Depends
from typing import Annotated
import redis
import rq
from tasks import random_task
from dependencies import get_redis_conn, QUEUE_NAME

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
async def add_task(
    task_count: Annotated[int, "count of tasks"] = 1,
    r: redis.Redis = Depends(get_redis_conn),
):
    queue = rq.Queue(QUEUE_NAME, connection=r)
    jobs = []
    for _ in range(task_count):
        job = queue.enqueue(random_task)
        jobs.append(job.id)
    return {"message": f"{task_count} tasks added.", "job_ids": jobs}


@router.get("/queue_length")
async def queue_length(r: redis.Redis = Depends(get_redis_conn)):
    queue = rq.Queue(QUEUE_NAME, connection=r)
    return {"queue_length": queue.count}

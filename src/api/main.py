import logging
import uvicorn
from fastapi import FastAPI
from dependencies import get_redis_conn, get_db
from routes import health, tasks, tenants, roles, users

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Backend API")

app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(tenants.router)
app.include_router(roles.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

    try:
        await get_redis_conn()
        logger.info("Redis connected.")
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        exit(1)

    try:
        db = next(get_db())
        db.close()
        logger.info("PostgreSQL connected.")
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")
        exit(1)

    logger.info("Startup complete.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

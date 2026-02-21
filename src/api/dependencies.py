import os
import yaml
import redis
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

config = yaml.safe_load(open("config.yaml"))

# Redis
REDIS_HOST = config["redis"]["domain"]
REDIS_PORT = config["redis"]["port"]
QUEUE_NAME = config["redis"]["queue_name"]

# PostgreSQL via SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    pg = config["postgres"]
    DATABASE_URL = f"postgresql://{pg['user']}:{pg['password']}@{pg['domain']}:{pg['port']}/{pg['dbname']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis_conn():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r.ping()
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise Exception("Could not connect to Redis") from e
    return r

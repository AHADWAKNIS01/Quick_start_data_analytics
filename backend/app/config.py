import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    couchbase_connstr: str = os.getenv("COUCHBASE_CONNSTR", "couchbase://localhost")
    couchbase_user: str = os.getenv("COUCHBASE_USER", "Administrator")
    couchbase_password: str = os.getenv("COUCHBASE_PASSWORD", "password")
    couchbase_bucket: str = os.getenv("COUCHBASE_BUCKET", "quickcart")

settings = Settings()

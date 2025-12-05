import os
import uuid
from datetime import datetime

def generate_job_id() -> str:
    return str(uuid.uuid4())

def get_timestamp() -> str:
    return datetime.now().isoformat()

def ensure_upload_dir(base_dir: str) -> str:
    upload_dir = os.path.join(base_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir

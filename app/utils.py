import hashlib
import json
import os
from datetime import datetime

PROCESSED_FILES_JSON = "data/metadata/processed_files.json"
AUDIT_LOG_DIR = "outputs/audit_logs"

def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def load_processed_files():
    if not os.path.exists(PROCESSED_FILES_JSON):
        return {}
    with open(PROCESSED_FILES_JSON, "r") as f:
        return json.load(f)

def save_processed_files(processed):
    with open(PROCESSED_FILES_JSON, "w") as f:
        json.dump(processed, f, indent=2)

def log_audit(action, filename, details=""):
    os.makedirs(AUDIT_LOG_DIR, exist_ok=True)
    log_file = os.path.join(AUDIT_LOG_DIR, f"audit_{datetime.now().strftime('%Y%m%d')}.csv")
    timestamp = datetime.now().isoformat()
    with open(log_file, "a") as f:
        f.write(f"{timestamp},{action},{filename},{details}\n")

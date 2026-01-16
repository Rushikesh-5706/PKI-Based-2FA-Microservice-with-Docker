import os
import time
from datetime import datetime, timezone
from app.totp_utils import generate_code

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

def log_2fa():
    try:
        if not os.path.exists(SEED_PATH):
            return
        with open(SEED_PATH, "r") as f:
            seed = f.read().strip()
        code, _ = generate_code(seed)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a") as f:
            f.write(f"{timestamp} - 2FA Code: {code}\n")
    except Exception:
        pass

if __name__ == "__main__":
    log_2fa()

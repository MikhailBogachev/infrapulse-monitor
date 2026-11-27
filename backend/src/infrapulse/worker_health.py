import sys
from pathlib import Path

from infrapulse.config import contains_live_process

if __name__ == "__main__":
    ready = Path("/tmp/infrapulse-worker.ready").is_file()
    sys.exit(0 if ready and contains_live_process(Path("/tmp/infrapulse-worker.pid")) else 1)

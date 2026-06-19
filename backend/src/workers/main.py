import logging
import os
import signal
import time

from src.config.settings import get_settings
from src.logging.config import configure_logging

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

_shutdown_requested = False


def _request_shutdown(signum: int, _frame: object) -> None:
    global _shutdown_requested
    _shutdown_requested = True
    logger.info("worker shutdown requested", extra={"request_id": "worker", "signal": signum})


def run_worker() -> None:
    """Run the initial worker loop.

    Long-running processing will later poll and lock pending rows from the PostgreSQL
    jobs table. No external broker is used in the MVP.
    """

    poll_interval_seconds = int(os.getenv("WORKER_POLL_INTERVAL_SECONDS", "5"))
    logger.info("worker started", extra={"request_id": "worker"})

    while not _shutdown_requested:
        logger.debug("worker idle; jobs table polling not implemented yet", extra={"request_id": "worker"})
        time.sleep(poll_interval_seconds)

    logger.info("worker stopped", extra={"request_id": "worker"})


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, _request_shutdown)
    signal.signal(signal.SIGINT, _request_shutdown)
    run_worker()

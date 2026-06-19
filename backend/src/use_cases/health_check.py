from dataclasses import dataclass
import logging

from src.adapters.mongo_adapter import MongoAdapter
from src.database.postgres import check_postgres_connection

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HealthCheckResult:
    status: str
    postgres: str
    mongodb: str


class HealthCheckUseCase:
    """Coordinates infrastructure health checks without business logic in controllers."""

    def execute(self) -> HealthCheckResult:
        postgres_status = "ok" if self._check_postgres() else "unavailable"
        mongodb_status = "ok" if self._check_mongodb() else "unavailable"
        status = "ok" if postgres_status == "ok" and mongodb_status == "ok" else "degraded"
        return HealthCheckResult(status=status, postgres=postgres_status, mongodb=mongodb_status)

    def _check_postgres(self) -> bool:
        try:
            return check_postgres_connection()
        except Exception as exc:  # health endpoint should report degraded, not expose internals
            logger.warning("postgres health check failed", extra={"request_id": "health"}, exc_info=exc)
            return False

    def _check_mongodb(self) -> bool:
        adapter = MongoAdapter()
        try:
            return adapter.ping()
        except Exception as exc:  # MongoDB is not source of truth; report unavailable
            logger.warning("mongodb health check failed", extra={"request_id": "health"}, exc_info=exc)
            return False
        finally:
            adapter.close()

from fastapi import APIRouter, status

from src.schemas.health import HealthResponse
from src.use_cases.health_check import HealthCheckUseCase

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health() -> HealthResponse:
    result = HealthCheckUseCase().execute()
    return HealthResponse(status=result.status, postgres=result.postgres, mongodb=result.mongodb)

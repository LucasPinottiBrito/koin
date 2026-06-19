from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    postgres: str
    mongodb: str

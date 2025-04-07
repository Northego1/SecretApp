from uuid import UUID

from pydantic import BaseModel, Field


class SecretPostResponse(BaseModel):
    secret_key: UUID


class SecretGetReposnse(BaseModel):
    secret: str


class SecretNotFoundResponse(BaseModel):
    detail: str = Field(examples=["Secret not found"])

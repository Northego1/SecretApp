from uuid import UUID

from pydantic import BaseModel, Field


class SecretPostResponse(BaseModel):
    secret_key: UUID


class SecretGetReponse(BaseModel):
    secret: str = Field(examples=["Some secret data"])


class SecretNotFoundResponse(BaseModel):
    detail: str = Field(examples=[
        "Secret with id: UUID(123e4567-e89b-12d3-a456426614174000) not found",
    ])

class SecretAlreadyReadResponse(BaseModel):
    detail: str = Field(examples=[
        "Secret with id: UUID(123e4567-e89b-12d3-a456426614174000) has already been read",
    ])

class SecretExpiredResponse(BaseModel):
    detail: str = Field(examples=[
        "Secret with id: UUID(123e4567-e89b-12d3-a456426614174000) has expired",
    ])

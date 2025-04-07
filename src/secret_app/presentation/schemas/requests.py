from pydantic import BaseModel, Field


class SecretDeleteRequest(BaseModel):
    passphrase: str | None = Field(default=None, examples=["Some passphrase | None", None])


class SecretPostRequest(SecretDeleteRequest):
    secret: str = Field(examples=["Some secret text"])
    ttl_seconds: int = Field(ge=1, examples=[180])





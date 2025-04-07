from pydantic import BaseModel, Field


class SecretPostRequest(BaseModel):
    secret: str = Field(examples=["Some secret text"])
    passphrase: str | None = Field(default=None, examples=["Some passphrase"])
    ttl_seconds: int = Field(ge=1, examples=[180])

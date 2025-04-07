from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.v1 import protocol as proto
from core.container import Container
from secret_app.presentation.schemas import requests, responses

router = APIRouter(
    prefix="/secret",
    responses={
        404: {
            "description": "Secret not found",
            "model": responses.SecretNotFoundResponse,
        },
    },
)


@router.post("/", status_code=201, summary="Create a new secret")
@inject
async def create_secret(
    requested_data: requests.SecretPostRequest,
    create_secret_cl: proto.CreateSecretControllerProtocol = Depends(Provide[
        Container.presentation_container.create_secret_cl # type: ignore
    ]),
) -> responses.SecretPostResponse:
    """
    Creates a new secret.

    This endpoint allows the user to create and securely store a new secret.
    """
    return await create_secret_cl.create_secret(requested_data)


@router.get("/{secret_key}", status_code=200, summary="Retrieve a secret")
@inject
async def get_secret(
    secret_key: str,
    get_secret_cl: proto.GetSecretControllerProtocol = Depends(Provide[
        Container.presentation_container.get_secret_cl # type: ignore
    ]),
) -> responses.SecretGetReposnse:
    """
    Retrieves a secret by its key.

    Args:
        secret_key (str): The unique key of the secret to retrieve.

    Returns:
        The secret associated with the provided key.
    """
    ...


@router.delete("/{secret_key}", status_code=204, summary="Delete a secret")
@inject
async def delete_secret(secret_key: str) -> None:
    """
    Deletes a secret by its key.

    Args:
        secret_key (str): The unique key of the secret to delete.

    Returns:
        A confirmation that the secret has been deleted.
    """
    ...

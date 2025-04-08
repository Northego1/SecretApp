from core.exceptions import AppError


class SecretError(AppError): ...


class SecretNotFoundError(SecretError): ...


class SecretPassphraseError(SecretError): ...

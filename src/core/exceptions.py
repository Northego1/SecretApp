class AppError(Exception):
    def __init__(
        self,
        *args: object,
        status_code: int = 500,
        detail: str = "Unkown Error",
    ) -> None:
        super().__init__(*args)
        self.status_code = status_code
        self.detail = detail

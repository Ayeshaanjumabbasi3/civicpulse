class ConflictError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.detail = detail

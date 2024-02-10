class WbError(Exception):
    """
        Base class exception for wildberries
    """

    def __init__(self, msg="", response=None):
        super().__init__(self, msg)

        self.response = response


class WbBadRequestError(WbError):
    """Thrown when the server returns code 400."""
    pass


class WbForbiddenRequestError(WbError):
    """Thrown when the server returns code 403."""
    pass


class RetriableWbError(WbError):
    """Thrown when there was an error, but it would make sense to retry the request."""
    pass


class UnknownWbError(RetriableWbError):
    """Thrown when the exception type couldn't be determined"""
    pass

"""Classes for indicating the success or failure of an operation."""
from abc import ABC


class Result(ABC):

    """Indicates the success of an operation, or failure with a reason."""

    is_error = False
    is_ok = False


class Ok(Result):

    """Indicates the success of an operation."""

    def __init__(self, value):
        """Construct a new OK result with the given value."""
        super().__init__()
        self.value = value

    is_error = False
    is_ok = True


class Error(Result):

    """Indicates an operation failed because of the given error."""

    def __init__(self, error):
        """Construct a new error result with the given error."""
        super().__init__()
        self.error = error

    is_error = True
    is_ok = False

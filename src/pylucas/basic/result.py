# Standard
from typing import (
    Generic,
    Any,
    TypeVar
)
# Internal
# External

T = TypeVar('T')
V = TypeVar('V')

class ResultError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Result(Generic[T, V]):
    def __init__(self, state: bool, data: Any, addition: Any | str = ""):
        self.state: bool = bool(state)
        self.data: Any = data
        self.addition: Any = addition
    
    def __bool__(self):
        return self.state

    def __call__(self):
        return self.data

    def __repr__(self):
        return str(self.data) + ("" if self.addition == "" else " ") + str(self.addition)
    
    @property
    def Exception(self):
        return ResultError(self.data, self.addition)
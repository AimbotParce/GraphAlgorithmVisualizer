from typing import TypeVar

from .node import BaseNode

T = TypeVar("T")


class Node(BaseNode[T]):
    "Base node class with a visited flag."

    def __init__(self, id: str | int, content: T) -> None:
        super().__init__(id, content)
        self._visited = False

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value: bool) -> None:
        self._visited = value

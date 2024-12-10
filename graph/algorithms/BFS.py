from collections import deque
from typing import Any, TypeVar

from .. import Node

T = TypeVar("T")


class undefined:
    pass


def searchBreathFirst(start: Node[T], id: str | int = undefined, content: T = undefined) -> None | Node[T]:
    """
    Search the graph using the BFS algorithm. If id or content is provided, the
    search will stop when the node is found and return the node.

    Args:
        start (Node): The start node.
        id (str | int): The id of the node to search.
        content (T): The content of the node to search.
    """
    queue = deque([start])
    while queue:
        current = queue.popleft()
        current.visited = True
        if id is not undefined and current.id == id:
            return current
        if content is not undefined and current.content == content:
            return current
        for neighbor in current.children:
            if not neighbor.visited:
                queue.append(neighbor)

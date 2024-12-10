import contextlib
import contextvars
from collections import deque
from io import IOBase
from os import PathLike
from typing import Any, Callable, Generic, ParamSpec, TextIO, TypeVar, overload

T = TypeVar("T")
P = ParamSpec("P")


class NodeVisitLogger:
    @overload
    def __init__(self, fd: TextIO, fmt: str = "%(id)s") -> None: ...
    @overload
    def __init__(self, fd: PathLike, fmt: str = "%(id)s") -> None: ...
    @overload
    def __init__(self, fd: None, fmt: str = "%(id)s") -> None: ...

    def __init__(self, fd: PathLike | TextIO | None = None, fmt: str = "%(id)s"):
        if fd is None:
            self._fd = None
            self._log = list[str]()
        elif isinstance(fd, IOBase):
            self._fd = fd
            self._log = None
        else:
            self._fd = open(fd, "w")
            self._log = None
        self._fmt = fmt
        self._opened = not isinstance(fd, IOBase)
        self._token: contextvars.Token = None

    def __enter__(self) -> "NodeVisitLogger":
        self._token = current_logger.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        current_logger.reset(self._token)
        if self._opened:
            self._fd.close()

    def logVisit(self, node: "BaseNode") -> None:
        cont: dict[str, Any] = {}
        for k in node.__dict__:
            cont[k.lstrip("_")] = getattr(node, k)
        line = self._fmt % cont
        if self._log is not None:
            self._log.append(line)
        else:
            self._fd.write(line)
            self._fd.write("\n")

    @staticmethod
    def on_call(callable: Callable[P, T]) -> Callable[P, T]:
        def wrapper(node: "BaseNode", *args, **kwargs):
            if current_logger.get() is not None:
                current_logger.get().logVisit(node)
            return callable(node, *args, **kwargs)

        return wrapper


current_logger = contextvars.ContextVar[NodeVisitLogger]("current_logger", default=None)


class BaseNode(Generic[T]):
    def __init__(self, id: str | int, content: T):
        self._id = id
        self._content = content
        self._children = deque[BaseNode]()

    def addChild(self, child: "BaseNode[T]") -> None:
        self._children.append(child)

    @property
    @NodeVisitLogger.on_call
    def content(self) -> T:
        return self._content

    @property
    @NodeVisitLogger.on_call
    def children(self) -> deque["BaseNode"]:
        return self._children

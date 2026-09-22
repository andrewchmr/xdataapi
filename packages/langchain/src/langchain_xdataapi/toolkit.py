"""The whole read surface as one toolkit."""

from __future__ import annotations

from typing import Iterable

from langchain_core.tools import BaseTool
from langchain_core.tools.base import BaseToolkit
from pydantic import ConfigDict

from .client import XdataapiClient
from .tools import ALL_TOOLS


class XdataapiToolkit(BaseToolkit):
    """Every read tool, sharing one client and one credit budget.

    Example:
        >>> from langchain_xdataapi import XdataapiToolkit
        >>> toolkit = XdataapiToolkit.from_api_key(max_results=25)
        >>> tools = toolkit.get_tools()

    Args:
        client: A configured :class:`XdataapiClient`.
        include: Tool names to keep. ``None`` keeps them all.
        exclude: Tool names to drop, applied after ``include``.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: XdataapiClient
    include: tuple[str, ...] | None = None
    exclude: tuple[str, ...] = ()

    @classmethod
    def from_api_key(
        cls,
        api_key: str | None = None,
        *,
        max_results: int | None = None,
        include: Iterable[str] | None = None,
        exclude: Iterable[str] = (),
        **client_kwargs: object,
    ) -> "XdataapiToolkit":
        """Build a toolkit from a key, or from ``XDATAAPI_KEY``.

        ``max_results`` caps the page size of every paging tool, which caps what
        one agent step can spend.
        """
        return cls(
            client=XdataapiClient(api_key, max_results=max_results, **client_kwargs),  # type: ignore[arg-type]
            include=tuple(include) if include is not None else None,
            exclude=tuple(exclude),
        )

    def get_tools(self) -> list[BaseTool]:
        tools = [tool(client=self.client) for tool in ALL_TOOLS]
        if self.include is not None:
            wanted = set(self.include)
            tools = [t for t in tools if t.name in wanted]
        if self.exclude:
            unwanted = set(self.exclude)
            tools = [t for t in tools if t.name not in unwanted]
        return tools

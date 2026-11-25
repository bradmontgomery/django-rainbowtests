"""ANSI color helpers built on rich."""

import io
from collections.abc import Callable

from rich.console import Console
from rich.text import Text


def _make_style(style: str) -> Callable[[str], str]:
    """Return a function that wraps text in the ANSI codes for a rich ``style``."""

    def styler(text: str) -> str:
        if not text:
            return ""
        buffer = io.StringIO()
        console = Console(file=buffer, force_terminal=True, no_color=False)
        console.print(Text(text, style=style), end="")
        return buffer.getvalue()

    return styler


blue = _make_style("bold blue")
cyan = _make_style("bold cyan")
green = _make_style("green")
magenta = _make_style("bold magenta")
red = _make_style("bold red")
white = _make_style("bold white")
yellow = _make_style("bold yellow")

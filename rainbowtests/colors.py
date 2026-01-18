import io

from rich.console import Console
from rich.text import Text


def _make_style(style: str):
    """Create a styling function using rich.

    Returns a callable that applies the given rich style to text and
    returns an ANSI-colored string.
    """

    def styler(text: str) -> str:
        if not text:
            return ""
        t = Text(text, style=style)
        console = Console(file=io.StringIO(), force_terminal=True, no_color=False)
        console.print(t, end="")
        return console.file.getvalue()

    return styler


blue = _make_style("bold blue")
cyan = _make_style("bold cyan")
green = _make_style("green")
magenta = _make_style("bold magenta")
red = _make_style("bold red")
white = _make_style("bold white")
yellow = _make_style("bold yellow")

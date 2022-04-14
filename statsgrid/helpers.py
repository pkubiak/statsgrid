"""Module contains helper functions"""
from typing import Dict, List, Any, Tuple, Union
import colorsys


BUILTIN_COLORS: Dict[str, str] = {
    "red": "#f2495c",
    "error": "#f2495c",
    "orange": "#ff9830",
    "warning": "#ff9830",
    "yellow": "#fade2a",
    "green": "#73bf69",
    "success": "#73bf69",
    "blue": "#5794f2",
    "info": "#5794f2",
    "purple": "#b877d9",
}


def _render_attr(value: Any) -> str:
    if isinstance(value, dict):
        return ";".join(f"{k}:{v}" for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return " ".join(value)
    return str(value)


def tag(
    name: str,
    content: Union[str, List[str], None] = None,
    *,
    attrs: Dict[str, Any] = None,
    close: bool = True,
) -> str:
    """
    TODO: Simple HTML Tag wrapper.

    Args:
        name (str): tag name (e.g. div)
        content (List[str], optional): Inner content of tag. Defaults to None.
        attrs (Dict[str, Any], optional): Mapping of tag attributes. Defaults to None.
        close (bool, optional): If False no closing tag is generated. Defaults to True.

    Raises:
        TypeError: _description_
        ValueError: _description_

    Returns:
        str: Tag rendered as HTML
    """
    attrs_html = " ".join(
        f'{k}="{_render_attr(v)}"' for k, v in (attrs or {}).items() if v
    )
    if attrs_html:
        attrs_html = " " + attrs_html

    if content is None:
        content = []
    if isinstance(content, str):
        content = [content]

    if not isinstance(content, list):
        raise TypeError("Content must be str | list")

    content_html = "".join(str(v) for v in content)

    if not close:
        if content_html:
            raise ValueError("Tags with content must be closed")
        return f"<{name}{attrs_html}>"

    return f"<{name}{attrs_html}>{content_html}</{name}>"


def _hex_to_rgb(color: str) -> Tuple[int, int, int]:
    color = color.strip("#")
    assert len(color) == 6
    red, green, blue = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    return (red, green, blue)


def _rgb_to_hex(red: float, green: float, blue: float) -> str:
    assert 0 <= red <= 1 and 0 <= green <= 1 and 0 <= blue <= 1
    return "#%02x%02x%02x" % (
        round(255 * red),
        round(255 * green),
        round(255 * blue),
    )  # noqa


def build_linear_gradient(color: str) -> Tuple[str, str]:
    """
    TODO: Build CSS linear-gradient based on given color

    Args:
        color (str): _description_

    Returns:
        Tuple[str, str]: _description_
    """
    red, green, blue = _hex_to_rgb(color)
    is_dark = (red * 0.299 + green * 0.587 + blue * 0.114) <= 186
    factor = -1.0 if is_dark else 0.7

    h, l, s = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)  # noqa

    color1 = colorsys.hls_to_rgb(
        (h + 8 / 360) % 1, min(1, max(l + 0.15 * factor, 0)), s
    )
    color2 = colorsys.hls_to_rgb(
        (h - 8 / 360) % 1, min(1, max(l + 0.05 * factor, 0)), s
    )
    hex_1, hex_2 = _rgb_to_hex(*color1), _rgb_to_hex(*color2)

    return "#fff" if is_dark else "#000", f"linear-gradient(120deg, {hex_1}, {hex_2})"

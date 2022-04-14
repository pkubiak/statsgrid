"""Module contains helper functions"""
from typing import Dict, List, Any, Tuple
import colorsys


BUILTIN_COLORS = {
    "red": "#f2495c",
    "orange": "#ff9830",
    "yellow": "#fade2a",
    "green": "#73bf69",
    "blue": "#5794f2",
    "purple": "#b877d9",
}
for a, b in [
    ("error", "red"),
    ("warning", "orange"),
    ("info", "blue"),
    ("success", "green"),
]:
    BUILTIN_COLORS[a] = BUILTIN_COLORS[b]


def _render_attr(value: Any) -> str:
    if isinstance(value, dict):
        return ";".join(f"{k}:{v}" for k, v in value.items())
    if isinstance(value, (list, tuple, set)):
        return " ".join(value)
    return str(value)


def tag(
    name: str,
    content: List[str] = None,
    *,
    attrs: Dict[str, Any] = None,
    close: bool = True,
) -> str:
    """
    Simple HTML Tag wrapper.

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


def hex_to_rgb(color: str) -> Tuple[int, int, int]:
    color = color.strip("#")
    assert len(color) == 6
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    return (r, g, b)


def rgb_to_hex(r: float, g: float, b: float) -> Tuple[str, str]:
    assert 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1
    return "#%02x%02x%02x" % (round(255 * r), round(255 * g), round(255 * b))


def build_linear_gradient(color: str) -> Tuple[str, str]:
    factor = 1.0
    r, g, b = hex_to_rgb(color)
    text = "#000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#fff"
    factor = -1.0 if text == "#fff" else 0.7

    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    color1 = colorsys.hls_to_rgb(
        (h + 8 / 360) % 1, min(1, max(l + 0.15 * factor, 0)), s
    )
    color2 = colorsys.hls_to_rgb(
        (h - 8 / 360) % 1, min(1, max(l + 0.05 * factor, 0)), s
    )
    color1, color2 = rgb_to_hex(*color1), rgb_to_hex(*color2)

    return text, f"linear-gradient(120deg, {color1}, {color2})"

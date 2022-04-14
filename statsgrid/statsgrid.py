"""Module provides implementation of StatsGrid"""
import os
import re
from typing import Any, List, Optional, Tuple, Union

from .helpers import tag, build_linear_gradient, BUILTIN_COLORS


with open(
    os.path.join(os.path.dirname(__file__), "style.css"), "r", encoding="utf-8"
) as file:
    _BASE_CSS = file.read()


def _render_value(value: Any) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def render_cell(
    title: str,
    value: Any,
    *,
    size: Optional[int] = None,
    color: Optional[str] = None,
    style: str = "gradient",
) -> str:
    """
    TODO: Render single grid cell as HTML

    Args:
        title (str): _description_
        value (Any): _description_
        size (Optional[int], optional): _description_. Defaults to None.
        color (Optional[str], optional): _description_. Defaults to None.
        style (str, optional): _description_. Defaults to "gradient".

    Raises:
        ValueError: _description_
        NotImplementedError: _description_
        ValueError: _description_

    Returns:
        str: HTML representation of cell
    """
    styles_outter = {}
    styles_inner = {}
    if size:
        styles_outter["flex-grow"] = str(size)

    if style == "gradient":
        if color is not None:
            if color == "transparent":
                foreground, background = "auto", "transparent"
            else:
                hex_color = BUILTIN_COLORS.get(color, color)
                if not re.fullmatch("#[0-9a-f]{6}", hex_color):
                    raise ValueError(f"Unsupported cell color: {hex_color}")

                foreground, background = build_linear_gradient(hex_color)
            styles_inner["background"] = background
            styles_inner["color"] = foreground
    elif style == "text":
        raise NotImplementedError()
    else:
        raise ValueError(f"Unsupported cell style: {style}")

    value_str = _render_value(value)

    return tag(
        "div",
        [
            tag(
                "div",
                [
                    tag("h2", title, attrs={"title": title}),
                    tag("h1", value_str, attrs={"title": value_str}),
                ],
                attrs=dict(style=styles_inner),
            )
        ],
        attrs={
            "style": styles_outter,
        },
    )


def _render_cell_tuple(cell: Tuple) -> str:
    assert 2 <= len(cell) <= 3
    if len(cell) == 2:
        cell += ({},)
    key, value, opt = cell
    return render_cell(key, value, **opt)


class StatsGrid:
    """TODO: TBA"""

    def __init__(
        self,
        data,
        *,
        caption: Optional[str] = None,
        font_size: Optional[int] = None,
        style: Optional[Union[str, List[str]]] = None,
        caption_position: str = "top left",
    ):
        self.data = data
        self.caption = caption
        self.font_size = font_size
        self.style = [style] if isinstance(style, str) else list(style or [])

        # caption_position
        if not isinstance(caption_position, str):
            raise ValueError()
        try:
            vertical, horizontal = caption_position.split(" ")
            assert vertical in {"top", "bottom"}
            assert horizontal in {"left", "center", "right"}
        except (ValueError, AssertionError):
            raise ValueError(f"Wrong caption_position set: {caption_position}")

        self.caption_position = caption_position

    def __call__(self, **kwargs) -> "StatsGrid":
        params = {**self.__dict__, **kwargs}
        params.pop("_base_css", None)

        return StatsGrid(**params)

    def _build_grid_html(self) -> str:
        styles = {}
        classes = ["stats-grid"] + self.style

        if self.font_size:
            styles["font-size"] = f"{self.font_size}px !important"

        content = []
        if self.caption:
            caption_html = tag(
                "figcaption",
                self.caption,
                attrs={"style": f"text-align: {self.caption_position[1]}"},
            )

            if self.caption_position[0] == "top":
                content.append(caption_html)

        for row in self.data:
            content.append(tag("div", [_render_cell_tuple(cell) for cell in row]))

        if self.caption and self.caption_position[0] == "bottom":
            content.append(caption_html)

        return tag("figure", content, attrs={"class": classes, "style": styles})

    def to_html(self) -> str:
        """
        Create HTML representation of current StatsGrid

        Returns:
            str: HTML representation of StatsGrid
        """
        grid = self._build_grid_html()
        return f"<style>{_BASE_CSS}</style>{grid}"

    def _repr_html_(self) -> str:
        return self.to_html()

import os
from functools import cached_property
from typing import Any, List, Optional, Tuple, Union

from .helpers import tag


def _render_value(value: Any) -> str:
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _render_cell(cell: Tuple) -> str:
    assert 2 <= len(cell) <= 3
    if len(cell) == 2:
        cell += ({},)
    key, value, opt = cell

    classes = []
    styles = {}
    if "size" in opt:
        styles["flex-grow"] = str(opt["size"])

    if "style" in opt:
        classes.append(opt["style"])

    value_str = _render_value(value)

    return tag(
        "div",
        [
            tag(
                "div",
                [
                    tag("h2", key, attrs={"title": key}),
                    tag("h1", value_str, attrs={"title": value_str}),
                ],
            )
        ],
        attrs={
            "class": classes,
            "style": styles,
        },
    )


class StatsGrid:
    def __init__(
        self,
        data,
        *,
        caption: Optional[str] = None,
        font_size: Optional[int] = None,
        style: Union[str, List[str]] = [],
        caption_position: str = "top left",
    ):
        self.data = data
        self.caption = caption
        self.font_size = font_size
        self.style = [style] if isinstance(style, str) else list(style)

        # caption_position
        if not isinstance(caption_position, str):
            raise ValueError()
        caption_position = caption_position.split(" ")
        if (
            len(caption_position) != 2
            or caption_position[0] not in {"top", "bottom"}
            or caption_position[1] not in {"left", "center", "right"}
        ):
            raise ValueError()
        self.caption_position = caption_position

    def __call__(self, **kwargs) -> "StatsGrid":
        params = {**self.__dict__, **kwargs}
        params.pop("_base_css", None)

        return StatsGrid(**params)

    def to_svg(self):
        raise NotImplementedError()

    def to_png(self):
        raise NotImplementedError()

    @cached_property
    def _base_css(self) -> str:
        with open(
            os.path.join(os.path.dirname(__file__), "style.css"), "r", encoding="utf-8"
        ) as file:
            return file.read()

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
            content.append(tag("div", [_render_cell(cell) for cell in row]))

        if self.caption and self.caption_position[0] == "bottom":
            content.append(caption_html)

        return tag("figure", content, attrs={"class": classes, "style": styles})

    def to_html(self) -> str:
        grid = self._build_grid_html()
        return f"<style>{self._base_css}</style>{grid}"

    def _repr_html_(self) -> str:
        return self.to_html()

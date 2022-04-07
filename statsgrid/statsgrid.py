from functools import cached_property
import os
from typing import Optional, Any, Union, List, Tuple


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

    def _render_value(self, value: Any) -> str:
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)

    def _render_cell(self, cell: Tuple) -> str:
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

        # render
        if styles:
            styles_html = ";".join(f"{k}:{v}" for k, v in styles.items())
            styles_html = f' style="{styles_html}"'
        else:
            styles_html = ""

        classes_html = " ".join(classes)
        if classes_html:
            classes_html = f' class="{classes_html}"'

        value_str = self._render_value(value)

        return f'<div{classes_html}{styles_html}><div><h2 title="{key}">{key}</h2><h1 title="{value_str}">{value_str}</h1></div></div>'

    def _build_grid_html(self) -> str:
        font_size_html = (
            f' style="font-size:{self.font_size}px !important"'
            if self.font_size
            else ""
        )
        classes = " ".join(["stats-grid"] + self.style)
        output = [f'<figure class="{classes}"{font_size_html}>']

        if self.caption:
            caption_html = f'<figcaption style="text-align: {self.caption_position[1]}">{self.caption}</figcaption>'

            if self.caption_position[0] == "top":
                output.append(caption_html)

        for row in self.data:
            output.append("<div>")
            for cell in row:
                output.append(self._render_cell(cell))
            output.append("</div>")

        if self.caption and self.caption_position[0] == "bottom":
            output.append(caption_html)
        output.append("</figure>")

        return "".join(output)

    def to_html(self) -> str:
        grid = self._build_grid_html()
        return f"<style>{self._base_css}</style>{grid}"

    def _repr_html_(self) -> str:
        return self.to_html()

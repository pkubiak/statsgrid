from functools import cached_property
import os
from typing import Optional, Any


class StatsGrid:
    def __init__(self, data, *, caption: Optional[str] = None):
        self.data = data
        self.caption = caption

    def to_svg(self):
        raise NotImplementedError()
    
    def to_png(self):
        raise NotImplementedError()

    @cached_property
    def _base_css(self):
        with open(os.path.join(os.path.dirname(__file__), "style.css")) as file:
            return file.read()

    def _render_value(self, value: Any) -> str:
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)
    
    def _render_cell(self, cell):
        assert 2 <= len(cell) <= 3
        if len(cell) == 2:
            cell += ({}, )
        key, value, opt = cell

        classes = ["stat"]
        styles = {}
        if 'size' in opt:
            styles["flex-grow"] = str(opt['size'])

        if 'style' in opt and opt['style'] in {"success"}:
            classes.append(opt['style'])
            
        
        # render
        if styles:
            styles_html = ";".join(f"{k}:{v}" for k, v in styles.items())
            styles_html = f' style="{styles_html}"'
        else:
            styles_html = ''
            
        classes_html = " ".join(classes)
        value_str = self._render_value(value)

        return f'<div class="{classes_html}"{styles_html}><div><h2>{key}</h2><h1>{value_str}</h1></div></div>'

    def _build_grid_html(self):
        output = ['<figure class="stats-grid">']
        if self.caption:
            output.append(f'<figcaption>{self.caption}</figcaption>')

        for row in self.data:
            output.append('<div class="row">')
            for cell in row:
                output.append(self._render_cell(cell))
            output.append('</div>')
        output.append("</figure>")

        return "".join(output)

    def to_html(self):
        grid = self._build_grid_html()
        return f"<style>{self._base_css}</style>{grid}"

    def _repr_html_(self):
        return self.to_html()


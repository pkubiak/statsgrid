from typing import Dict, List, Any

from numpy import isin


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
    attrs: Dict[str, str] = None,
    close: bool = True,
) -> str:
    attrs_html = " ".join(f'{k}="{_render_attr(v)}"' for k, v in (attrs or {}).items() if v)
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

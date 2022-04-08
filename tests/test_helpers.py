import pytest
from statsgrid.helpers import tag


def test_full_rendering():
    assert (
        tag("div", "content", attrs=dict(id="hello")) == '<div id="hello">content</div>'
    )


def test_name_is_required():
    with pytest.raises(TypeError):
        tag()


def test_only_name():
    assert tag("div") == "<div></div>"


def test_name_with_content():
    assert tag("div", "hello") == "<div>hello</div>"


def test_name_with_attrs():
    assert tag("div", attrs={"id": "hello"}) == '<div id="hello"></div>'


def test_nested_tags():
    assert tag("div", tag("h1", "hello")) == "<div><h1>hello</h1></div>"


def test_multi_content():
    assert tag("div", ["hello", tag("h1", "title")]) == "<div>hello<h1>title</h1></div>"


def test_ignore_empty_attrs():
    assert tag("div", attrs={"class": ""}) == "<div></div>"


def test_no_closing():
    assert tag("img", attrs={"src": "img.png"}, close=False) == '<img src="img.png">'


def test_unclosed_with_content():
    with pytest.raises(ValueError):
        tag("img", "hello world", close=False)


def test_non_string_content():
    assert tag("div", [1, None, [1, 2, 3]]) == "<div>1None[1, 2, 3]</div>"


def test_wrong_content_type():
    with pytest.raises(TypeError):
        tag("div", {"hello"})


def test_rendering_dict_attr():
    html = tag("div", attrs={"style": {"font-size": "12px", "color": "black"}})

    assert html == '<div style="font-size:12px;color:black"></div>'


def test_rendering_list_attr():
    html = tag("div", attrs={"class": ["a", "b", "c"]})
    assert html == '<div class="a b c"></div>'

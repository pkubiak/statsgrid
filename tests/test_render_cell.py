from statsgrid.statsgrid import render_cell


def test_xyz():
    html = render_cell("key", "value")
    assert (
        html
        == '<div><div><h2 title="key">key</h2><h1 title="value">value</h1></div></div>'
    )


def test_render_with_color():
    html = render_cell("key", "value", color="warning")
    assert (
        "linear-gradient" in html
    )

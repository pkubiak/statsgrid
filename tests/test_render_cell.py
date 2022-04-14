from statsgrid.statsgrid import render_cell


def test_xyz():
    html = render_cell(("key", "value"))
    assert (
        html
        == '<div><div><h2 title="key">key</h2><h1 title="value">value</h1></div></div>'
    )


def test_render_with_style():
    html = render_cell("key", "value", style="warning")
    assert (
        html
        == '<div class="warning"><div><h2 title="key">key</h2><h1 title="value">value</h1></div></div>'
    )

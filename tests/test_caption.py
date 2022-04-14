import re
from itertools import product

import pytest
from statsgrid import StatsGrid


def test_without_caption():
    sg = StatsGrid([])
    assert "<figcaption" not in sg.to_html()


def test_grid_with_caption():
    sg = StatsGrid([], caption="Hello StatsGrid")
    assert "<figcaption" in sg.to_html()
    assert "Hello StatsGrid" in sg.to_html()


@pytest.mark.parametrize(
    "vertical,horizontal", product(["top", "bottom"], ["left", "right", "center"])
)
def test_caption_position(vertical, horizontal):
    sg = StatsGrid(
        [[("cell", "value")]],
        caption="mycaption",
        caption_position=f"{vertical} {horizontal}",
    )

    html = sg.to_html().replace("\n", "")

    assert "<figcaption" in html
    figcaption = re.search("<figcaption.*</figcaption>", html).group()

    assert "mycaption" in figcaption

    # caption is horizontally aligned
    assert f"text-align: {horizontal}" in figcaption

    # caption is vertically aligned
    if vertical == "top":
        assert re.search("<figure[^>]*><figcaption", html)
    else:
        assert "</figcaption></figure>" in html


@pytest.mark.parametrize(
    "position",
    [
        None,
        "left right",
        "left bottom",  # wrong locations order
        "center left",  # center is not supported as vertical location
        "góra prawo",
        "left",
        "bottom",  # both locations (vertical / horizontal) should be passed
    ],
)
def test_wrong_caption_positions(position):
    with pytest.raises(ValueError):
        StatsGrid([], caption="caption", caption_position=position)


def test_position_without_caption():
    """Caption position should be ensured even when caption text is not defined."""
    with pytest.raises(ValueError):
        StatsGrid([], caption_position=None)

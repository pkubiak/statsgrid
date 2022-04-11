<img alt="Icon" src="https://raw.githubusercontent.com/thiagoolsilva/cryptography-cli/main/misc/app_icon.png" align="left" hspace="1" vspace="1">

# statsgrid

![Licence MIT](https://img.shields.io/github/license/pkubiak/statsgrid)
![Python 3.0](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pkubiak/statsgrid/Python%20package)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pkubiak/statsgrid/HEAD?labpath=examples%2Fdemo.ipynb)

</br>

## Description

Module for creating Grafana style metrics dashboards in python.

![Preview image](/misc/preview.jpg)


## Examples

```python
from statsgrid import StatsGrid

StatsGrid([
    [
        ("accuracy", "0.71 ↗", dict(style="success")),
        ("precision", "0.92 ↘", dict(style="warning")),
        ("f1-score",  "0.80} ↗", dict(style="success"))
    ], [
        ("train-corpus-size", 1234567),
        ("test-corpus-size", 34567),
        ("no-classes", 42),
        ("training-time [s]", 123.45),
    ], [
        ("model-location", "s3://mybucket/model.pth", dict(size=3)),
        ("model-size [MiB]", 234.54), 
    ]
], caption="Classifier Training Summary", style="dark")
```

Check [/examples](/examples) directory for sample Jupyter Notebooks or run it using [mybinder.org](https://mybinder.org/v2/gh/pkubiak/statsgrid/HEAD?labpath=examples%2Fdemo.ipynb)

## API Reference
TBA

## CHANGELOG

- 2022.04.08
    - initial version 

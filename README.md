# imodmodel

[![License](https://img.shields.io/pypi/l/imodmodel.svg?color=green)](https://github.com/alisterburt/imodmodel/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/imodmodel.svg?color=green)](https://pypi.org/project/imodmodel)
[![Python Version](https://img.shields.io/pypi/pyversions/imodmodel.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/imodmodel/actions/workflows/ci.yml/badge.svg)](https://github.com/alisterburt/imodmodel/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/alisterburt/imodmodel/branch/main/graph/badge.svg)](https://codecov.io/gh/alisterburt/imodmodel)

IMOD model files as [pandas dataframes](https://pandas.pydata.org/) in Python.

## Installation
`imodmodel` can be installed from the [Python Package Index](https://pypi.org/) (PyPI)

```shell
pip install imodmodel
```

We recommend installing into a clean virtual environment.

## Usage

```python
import imodmodel

df = imodmodel.read('my_model_file.mod')
```

```ipython
In [3]: df.describe()
Out[3]: 
       object_id  contour_id           x           y       z
count       25.0   25.000000   25.000000   25.000000  25.000
mean         0.0    0.320000   65.413334   63.240001  73.280
std          0.0    0.476095   29.576687   28.116082   9.998
min          0.0    0.000000   10.666667    4.333333  59.000

```

That's it!
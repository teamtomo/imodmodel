# imodmodel

[![License](https://img.shields.io/pypi/l/imodmodel.svg?color=green)](https://github.com/alisterburt/imodmodel/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/imodmodel.svg?color=green)](https://pypi.org/project/imodmodel)
[![Python Version](https://img.shields.io/pypi/pyversions/imodmodel.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/imodmodel/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/alisterburt/imodmodel/actions/workflows/test_and_deploy.yml)

Read [IMOD model files](https://bio3d.colorado.edu/imod/doc/binspec.html) 
as [pandas dataframes](https://pandas.pydata.org/) 
in Python.


## Usage

### As pandas DataFrame

```python
import imodmodel

df = imodmodel.read('my_model_file.mod')
```

```ipython
In [3]: df.head()
Out[3]: 
   object_id  contour_id          x          y     z
0          0           0  64.333336  64.666664  80.0
1          0           0  47.000000  77.333336  80.0
2          0           0  51.333332  45.666668  80.0
3          0           0  87.333336  49.666668  80.0
4          0           0  76.000000  82.000000  80.0


```

### As ImodModel object

```python
from imodmodel import ImodModel
model = ImodModel.from_file("my_model_file.mod")
```

```ipython
In [3]: model.objects[0].contours[0].points
Out[3]: 
array([[  6.875,  62.875, 124.   ], ...])

In [4]: model.objects[0].meshes[0].vertices
Out[4]: 
array([[ 6.87500000e+00,  6.28750000e+01,  1.24000000e+02], ...])

In [5]: model.objects[0].meshes[0].indices
Out[5]: 
array([[156,  18, 152], ...])

In [6]: model.objects[0].meshes[0].face_values
Out[6]: 
array([0., 0., 35.22094345, ...])
```

That's it!

## Installation
`imodmodel` can be installed from the [Python Package Index](https://pypi.org/) (PyPI)

```shell
pip install imodmodel
```

We recommend installing into a clean virtual environment.

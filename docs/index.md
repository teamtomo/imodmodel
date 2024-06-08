# Overview

[![License](https://img.shields.io/pypi/l/imodmodel.svg?color=green)](https://github.com/alisterburt/imodmodel/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/imodmodel.svg?color=green)](https://pypi.org/project/imodmodel)
[![Python Version](https://img.shields.io/pypi/pyversions/imodmodel.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/imodmodel/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/alisterburt/imodmodel/actions/workflows/ci.yml)

Read [IMOD model files](https://bio3d.colorado.edu/imod/doc/binspec.html) 
as [pandas dataframes](https://pandas.pydata.org/) 
in Python.

## Usage

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

Annotations made in the [slicer window](https://bio3d.colorado.edu/imod/doc/3dmodHelp/slicer.html) are stored in the IMOD binary file with both centerpoints and angles.

These annotations can be read in by setting `annotation = 'slan'` when calling `imodmodel.read()`

```python
import imodmodel

df = imodmodel.read('file_with_slicer_angles.mod', annotation='slan')
```

```ipython
In [3]: df.head()
Out[3]:
   object_id  slan_id  time      x_rot  y_rot      z_rot    center_x    center_y  center_z label
0          0        0     1  13.100000    0.0 -30.200001  235.519577  682.744141     302.0
0          0        1     1 -41.400002    0.0 -47.700001  221.942444  661.193237     327.0
0          0        2     1 -41.400002    0.0 -41.799999  232.790726  671.332031     327.0
0          0        3     1 -35.500000    0.0 -36.000000  240.129181  679.927795     324.0
```

That's it!

## Installation
`imodmodel` can be installed from the [Python Package Index](https://pypi.org/) (PyPI)

```shell
pip install imodmodel
```

We recommend installing into a clean virtual environment.

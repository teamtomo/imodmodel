# Slicer Angles

Slicer angles saved in the [slicer window](https://bio3d.colorado.edu/imod/doc/3dmodHelp/slicer.html) 
are stored in the IMOD binary file with both centerpoints and angles.

These annotations can be read in by setting `annotation='slicer_angle'` when calling `imodmodel.read()`

```python
import imodmodel

df = imodmodel.read('file_with_slicer_angles.mod', annotation='slicer_angles')
```

```ipython
In [3]: df.head()
Out[3]:
   object_id  slicer_angle_id  time      x_rot  y_rot      z_rot    center_x    center_y  center_z label
0          0        0     1  13.100000    0.0 -30.200001  235.519577  682.744141     302.0
0          0        1     1 -41.400002    0.0 -47.700001  221.942444  661.193237     327.0
0          0        2     1 -41.400002    0.0 -41.799999  232.790726  671.332031     327.0
0          0        3     1 -35.500000    0.0 -36.000000  240.129181  679.927795     324.0
```

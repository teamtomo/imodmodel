
# Object-based API

The resulting dataframe from `imodmodel.read()` contains only information about the contours or slicer angles. 
The full set of information from the imod model file can be parsed using `ImodModel`

```python
from imodmodel import ImodModel

my_model = ImodModel.from_file("my_model_file.mod")
```

```ipython
in [3]: my_model.model_field_set
out[3]: 
{'id', 'extra', 'objects', 'slicer_angles', 'header'}
```

### my_model.id

`my_model.id` contains the IMOD file id and the version id

```ipython
in [4]: my_model.id
out[4]: 
ID(IMOD_file_id='IMOD', version_id='V1.2')
```

### my_model.header

`my_model.header` is contains the model structure data mainly used by IMOD.

```ipython
in [5]: my_model.header
out[5]:
ModelHeader(name='IMOD-NewModel', xmax=956, ymax=924, zmax=300, objsize=3, flags=62976, drawmode=1,
mousemode=1, blacklevel=145, whitelevel=173, xoffset=0.0, yoffset=0.0, zoffset=0.0, xscale=1.0, yscale=10,
zscale=1.0, object=2, contour=-1, point=-1, res=3, thresh=128, pixelsize=1.9733333587646484, units=-9,
csum=704518946, alpha=0.0, beta=0.0, gamma=0.0)
```

### my_model.objects

`my_model.objects` is a `list` IMOD objects.

```ipython
in [6]: my_model.objects[0].header
out[6]: 
ObjectHeader(name='', extra_data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], contsize=0,
flags=402653184, axis=0, drawmode=1, red=0.0, green=1.0, blue=0.0, pdrawsize=0, symbol=1, symsize=3,
linewidth2=1, linewidth=1, linesty=0, symflags=0, sympad=0, trans=0, meshsize=0, surfsize=0)
```

This is where object values like contours, meshes, and IMAT information are located.

```ipython
in [7]: my_model.objects[1].meshes[0].indices
out[7]: 
array([[38, 40, 52],
       [38, 52, 50],
       [50, 52, 64],
       [50, 64, 60],
       ...,
       [ 4, 10, 26],
       [ 4, 26, 20],
       [20, 26, 38],
       [20, 38, 32]])
```

```ipython
in [8]: my_model.objects[1].imat
out[8]: 
IMAT(ambient=102, diffuse=255, specular=127, shininess=4, fillred=0, fillgreen=0, fillblue=0,
quality=0, mat2=0, valblack=0, valwhite=255, matflags2=0, mat3b3=0)
```

```ipython
in [9]: my_model.objects[1].contours[0].points
out[9]:
array([[367.00006104, 661.83343506, 134.        ],
       [415.66674805, 667.83343506, 134.        ],
       [474.33340454, 662.50012207, 134.        ]])
```

### my_model.slicer_angles

`my_model.slicer_angles` is a `list` of slicer angles.

```ipython
in [10]: my_model.slicer_angles[0]
out[10]:
SLAN(time=1, angles=(0.0, 0.0, 0.0), center=(533.5, 717.0, 126.0), label='\x00')
```

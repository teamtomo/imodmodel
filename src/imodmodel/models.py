from enum import Enum
import os
import warnings
from typing import List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class ID(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    IMOD_file_id: str
    version_id: str


class GeneralStorage(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    type: int
    flags: int
    index: Union[float, int, Tuple[int, int], Tuple[int, int, int, int]]
    value: Union[float, int, Tuple[int, int], Tuple[int, int, int, int]]

class IntFlagModel(BaseModel):

    def __init__(self, int_value: int = -1, **kwargs):
        """Initialize the Flags from an integer value.
        """
        super().__init__(**kwargs)
        if int_value < 0:
            return
        for i, (key, _) in enumerate(self.__dict__.items()):
            if (int_value & (1 << i)) != 0:
                # Set the corresponding flag to True
                setattr(self, key, True)
            else:
                # Otherwise, keep it as False
                setattr(self, key, False)


    def __int__(self):
        """Return the integer value of the flags."""
        return_value = 0
        # Iterate over fields in the ModelFlags class
        for i, (key, value) in enumerate(self.__dict__.items()):
            if value:
                # Set the corresponding bit in the integer value
                return_value |= (1 << i)
        return return_value

class ContourFlags(IntFlagModel):
    flag0: bool = False
    flag1: bool = False
    flag2: bool = False
    open: bool = False
    wild: bool = False
    strippled: bool = False
    cursor_like: bool = False
    draw_allz: bool = False
    model_only: bool = False
    noconnect: bool = False
    flag10: bool = False
    flag11: bool = False
    flag12: bool = False
    flag13: bool = False
    flag14: bool = False
    flag15: bool = False
    flag16: bool = False
    scanline: bool = False
    connect_top: bool = False
    connect_bottom: bool = False
    connect_invert: bool = False
    

class ContourType(Enum):
    OPEN = "open"
    CLOSED = "closed"
    SCATTERED = "scattered"


class ContourHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    psize: int = 0
    flags: ContourFlags = ContourFlags(0)
    time: int = 0
    surf: int = 0

    @field_validator('flags', mode="before")
    @classmethod
    def set_flags(cls, value: Union[int,ContourFlags]):
        if isinstance(value,int):
            flags = ContourFlags(value)
        else:
            flags = value
        return flags


class Contour(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: ContourHeader = ContourHeader()
    points: np.ndarray 
    point_sizes: Optional[np.ndarray]  = None
    extra: List[GeneralStorage] = []

    model_config = ConfigDict(arbitrary_types_allowed=True,
                              validate_assignment=True)
    
    @field_validator('points')
    @classmethod
    def validate_points(cls, points: Union[np.ndarray, List[List[float]]]):
        if not isinstance(points, np.ndarray):
            points = np.array(points)
        if points.ndim != 2:
            raise ValueError('points must be 2D')
        if points.shape[1] != 3:
            raise ValueError(f'Invalid points shape: {points.shape}')
        return points

    @model_validator(mode='after')
    def update_sizes(self):
        self.header.psize = len(self.points)
        return(self)

class MeshFlags(IntFlagModel):
    flag0: bool = False
    flag1: bool = False
    flag2: bool = False
    flag3: bool = False
    flag4: bool = False
    flag5: bool = False
    flag6: bool = False
    flag7: bool = False
    flag8: bool = False
    flag9: bool = False
    flag10: bool = False
    flag11: bool = False
    flag12: bool = False
    flag13: bool = False
    flag14: bool = False
    flag15: bool = False
    normals_have_magnitude: bool = False
    flag17: bool = False
    flag18: bool = False
    flag19: bool = False
    resolution1: bool = False
    resolution2: bool = False
    resolution3: bool = False
    resolution4: bool = False
class MeshHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    vsize: int = 0
    lsize: int = 0
    flags: MeshFlags = MeshFlags(0)
    time: int = 0
    surf: int = 0

    @field_validator('flags', mode="before")
    @classmethod
    def set_flags(cls, value: Union[int,MeshFlags]):
        if isinstance(value,int):
            flags = MeshFlags(value)
        else:
            flags = value        
        return flags

class Mesh(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: MeshHeader = MeshHeader()
    raw_vertices: np.ndarray = np.zeros((0,))
    raw_indices: np.ndarray = np.zeros((0,))
    extra: List[GeneralStorage] = []

    model_config = ConfigDict(arbitrary_types_allowed=True,
                              validate_assignment=True)

    @model_validator(mode='after')
    def update_sizes(self):
        self.header.vsize = len(self.raw_vertices) // 3
        self.header.lsize = len(self.raw_indices) 
        return(self)
    
    @field_validator('raw_indices')
    @classmethod
    def validate_indices(cls, indices: np.ndarray):
        if indices.ndim > 1:
            raise ValueError('indices must be 1D')
        if indices[-1] != -1:
            raise ValueError('Indices must end with -1')
        if len(indices[np.where(indices >= 0)]) % 3 != 0:
            raise ValueError(f'Invalid indices shape: {indices.shape}')
        for i in (-20, -23, -24):
            if i in indices:
                warnings.warn(f'Unsupported mesh type: {i}')
        return indices

    @field_validator('raw_vertices')
    @classmethod
    def validate_vertices(cls, vertices: np.ndarray):
        if vertices.ndim > 1:
            raise ValueError('vertices must be 1D')
        if len(vertices) % 3 != 0:
            raise ValueError(f'Invalid vertices shape: {vertices.shape}')
        return vertices

    @property
    def vertices(self) -> np.ndarray:
        return self.raw_vertices.reshape((-1, 3))[::2]
    
    @vertices.setter
    def vertices(self, value: np.ndarray):
        if value.ndim != 2 or value.shape[1] != 3:
            raise ValueError('vertices must be 2D with shape (n, 3)')

        raw_vertices = np.zeros((value.shape[0] * 2, value.shape[1]))
        raw_vertices[::2] = value
        self.raw_vertices = raw_vertices.flatten()
    
    @property
    def normals(self) -> np.ndarray:
        return self.raw_vertices.reshape((-1, 3))[1::2]

    @property
    def indices(self) -> np.ndarray:
        return self.raw_indices[np.where(self.raw_indices >= 0)].reshape((-1, 3))//2

    @indices.setter
    def indices(self, value: np.ndarray):
        if value.ndim != 2 or value.shape[1] != 3:
            raise ValueError('indices must be 2D with shape (n, 3)')
        self.raw_indices = np.concatenate([
            np.array([-25]),
            value.flatten() * 2,
            np.array([-22]),
            np.array([-1]),
        ], dtype=np.int32)

    @property
    def face_values(self) -> Optional[np.ndarray]:
        """Extra value for each vertex face.
        The extra values are index, value  pairs
        However, the index is an index into the indices array,
        not directly an index of a vertex.
        Furthermore, the index has to be fixed because
        the original indices array has special command values (-25, -22, -1, ...)
        """
        values = np.zeros((len(self.vertices),))
        has_face_values = False
        for extra in self.extra:
            if not (extra.type == 10 and isinstance(extra.index, int)):
                continue
            has_face_values = True
            values[self.raw_indices[extra.index]] = extra.value
        if has_face_values:
            return values


class IMAT(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    ambient: int = 102
    diffuse: int = 255
    specular: int = 127
    shininess: int = 4
    fillred: int = 0
    fillgreen: int = 0
    fillblue: int = 0
    quality: int = 0
    mat2: int = 0
    valblack: int = 0
    valwhite: int = 255
    matflags2: int = 0 
    mat3b3: int = 0

class MINX(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    oscale: Tuple[float, float, float]
    otrans: Tuple[float, float, float]
    orot: Tuple[float, float, float]
    cscale: Tuple[float, float, float]
    ctrans: Tuple[float, float, float]
    crot: Tuple[float, float, float]

class View(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    fovy: float
    rad: float
    aspect: float
    cnear: float
    cfar: float
    rot: Tuple[float, float, float]
    trans: Tuple[float, float, float]
    scale: Tuple[float, float, float]
    mat: Tuple[
        float, float, float, float,
        float, float, float, float,
        float, float, float, float,
        float, float, float, float,
    ]
    world: int
    label: str
    dcstart: float
    dcend: float
    lightx: float
    lighty: float
    plax: float
    objvsize: int
    bytesObjv: int


class SLAN(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    time: int
    angles: Tuple[float,float,float]
    center: Tuple[float,float,float]
    label: str


class ObjectFlags(IntFlagModel):
    flag0: bool = False
    turn_off_display: bool = False
    draw_using_depth_cue: bool = False
    open: bool = False                                   # 3 /* Object contains Open/Closed contours */
    wild: bool = False                                   # 4 /* No constraints on contour data       */
    inside_out: bool = False
    use_fill_for_spheres: bool = False
    draw_spheres_central_section_only: bool = False
    fill: bool = False
    scattered: bool = False
    mesh: bool = False                                   # 10 /* Draw mesh in 3D, imod view        */
    noline: bool = False                                 # 11 
    use_value: bool = False                              # 12 
    planar: bool = False                                 # 13 
    fcolor: bool = False                                 # 14 
    anti_alias: bool = False                             # 15 
    scalar: bool = False                                 # 16 
    mcolor: bool = False                                 # 17 
    time: bool = False                                   # 18 
    two_side: bool = False                               # 19 
    thick_cont: bool = False                             # 20 
    extra_modv: bool = False                             # 21 
    extra_edit: bool = False                             # 22 
    pnt_nomodv: bool = False                             # 23 
    modv_only: bool = False                              # 24 
    flag25: bool = False                                 # 25 
    poly_cont: bool = False                              # 26 
    draw_label: bool = False                             # 27 
    scale_wdth: bool = False                             # 28 


class ObjectHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    name: str = ''
    extra_data: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    contsize: int = 0
    flags: ObjectFlags = ObjectFlags(0)
    axis: int = 0
    drawmode: int = 1
    red: float = 0.0
    green: float = 1.0
    blue: float = 0.0
    pdrawsize: int = 2
    symbol: int = 1
    symsize: int = 3
    linewidth2: int = 1
    linewidth: int = 1
    linesty: int = 0
    symflags: int = 0
    sympad: int = 0
    trans: int = 0
    meshsize: int = 0
    surfsize: int = 0


    @field_validator('flags', mode="before")
    @classmethod
    def set_flags(cls, value: Union[int,ObjectFlags]):
        if isinstance(value,int):
            flags = ObjectFlags(value)
        else:
            flags = value        
        return flags

class Object(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: ObjectHeader = ObjectHeader()
    contours: List[Contour] = []
    meshes: List[Mesh] = []
    extra: List[GeneralStorage] = []
    imat: Optional[IMAT] = None
    cview: Optional[int] = None

    model_config = ConfigDict(validate_assignment=True)

    def __init__(self, 
                 color: Optional[Tuple[float, float, float]] = None, 
                 **data):
        super().__init__(**data)
        if color is not None:
            self.color = color

    
    def update_sizes(self):
        self.header.contsize = len(self.contours)
        self.header.meshsize = len(self.meshes)
    
    @property
    def color(self):
        return (self.header.red, self.header.green, self.header.blue)
    
    @color.setter
    def color(self, value: Tuple[float, float, float]):
        self.header.red, self.header.green, self.header.blue = value


class ModelFlags(IntFlagModel):
    flag0: bool = False #0
    flag1: bool = False #1
    flag2: bool = False #2
    flag3: bool = False #3
    flag4: bool = False #4
    flag5: bool = False #5
    flag6: bool = False #6
    flag7: bool = False #7
    flag8: bool = False #8
    mesh_thickness_possible: bool = False #9
    z_coordinates_start_from_negative_half: bool = False #10
    model_has_not_been_written: bool = False #11
    multiple_clip_planes_possible: bool = False #12
    mat1_and_mat3_are_bytes: bool = False #13
    otrans_has_image_origin_values: bool = False #14
    current_tilt_angles_are_stored_correctly: bool = False #15
    model_last_viewed_onYZ_flipped_or_rotated: bool = False #16
    model_rotx: bool = False #17

    
class ModelHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    name: str = 'IMOD-NewModel'
    xmax: int = 0
    ymax: int = 0
    zmax: int = 0
    objsize: int = 0
    flags: ModelFlags = ModelFlags(0)
    drawmode: int = 1
    mousemode: int = 2
    blacklevel: int = 0
    whitelevel: int = 255
    xoffset: float = 0.0
    yoffset: float = 0.0
    zoffset: float = 0.0
    xscale: float = 1.0
    yscale: float = 1.0
    zscale: float = 1.0
    object: int = 0
    contour: int = 0
    point: int = -1
    res: int = 3
    thresh: int = 128
    pixelsize: float = 1.0
    units: int = 0
    csum: int = 0
    alpha: float = 0.0
    beta: float = 0.0
    gamma: float = 0.0

    @field_validator('flags', mode="before")
    @classmethod
    def set_flags(cls, value: Union[int,ModelFlags]):
        if isinstance(value, int):
            flags = ModelFlags(value)
        else:
            flags = value
        return flags

class ImodModel(BaseModel):
    """Contents of an IMOD model file.

    https://bio3d.colorado.edu/imod/doc/binspec.html
    """
    id: ID = ID(IMOD_file_id='IMOD', version_id='V1.2')
    header: ModelHeader = ModelHeader()
    objects: List[Object] = []
    slicer_angles: List[SLAN] = []
    minx: Optional[MINX] = None
    extra: List[GeneralStorage] = []

    model_config = ConfigDict(validate_assignment=True,
                              arbitrary_types_allowed=True)

    def update_sizes(self):
        self.header.objsize = len(self.objects)
    
    @classmethod
    def from_file(cls, filename: os.PathLike):
        """Read an IMOD model from disk."""
        from .parsers import parse_model
        with open(filename, 'rb') as file:
            return parse_model(file)
        
    @classmethod
    def from_dataframe(cls, dataframe: pd.DataFrame, type: ContourType = ContourType.SCATTERED):
        """Read an IMOD model from a pandas DataFrame."""
        
        # Ensure the DataFrame has the required columns
        required_columns = ['x', 'y', 'z']
        for col in required_columns:
            if col not in dataframe.columns:
                raise ValueError(f"DataFrame must contain the column '{col}'")
        if "object_id" not in dataframe.columns:
            dataframe["object_id"] = 0
        if "contour_id" not in dataframe.columns:
            dataframe["contour_id"] = 0
  
        model = ImodModel()
        for object_id, object_group in dataframe.groupby("object_id"):
            obj = Object()
            for contour_id, contour_group in object_group.groupby("contour_id"):
                contour = Contour(
                    points=contour_group[['x', 'y', 'z']].values,
                )
                obj.contours.append(contour)
            if type == ContourType.SCATTERED:
                obj.header.flags.scattered = True
                obj.header.flags.open = False
            elif type == ContourType.OPEN:
                obj.header.flags.scattered = False
                obj.header.flags.open = True
            elif type == ContourType.CLOSED:
                obj.header.flags.scattered = False
                obj.header.flags.open = False
            obj.update_sizes()
            model.objects.append(obj)
        model.update_sizes()
        return model

    def to_file(self, filename: os.PathLike):
        """Write an IMOD model to disk."""
        from .writers import write_model
        with open(filename, 'wb') as file:
            write_model(file, self)

import os
import warnings
from typing import List, Optional, Tuple, Union

import numpy as np
from pydantic import BaseModel, ConfigDict, field_validator


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


class ModelHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    name: str = 'IMOD-NewModel'
    xmax: int = 0
    ymax: int = 0
    zmax: int = 0
    objsize: int = 0
    flags: int = 402653704
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

    @field_validator('name', mode="before")
    @classmethod
    def decode_null_terminated_byte_string(cls, value: bytes):
        end = value.find(b'\x00')
        return value[:end].decode('utf-8')


class ObjectHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    name: str = ''
    extra_data: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    contsize: int = 1
    flags: int = 402653704
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

    @field_validator('name', mode="before")
    @classmethod
    def decode_null_terminated_byte_string(cls, value: bytes):
        end = value.find(b'\x00')
        return value[:end].decode('utf-8')


class ContourHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    psize: int
    flags: int
    time: int
    surf: int


class Contour(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: ContourHeader
    points: np.ndarray  # pt
    point_sizes: Optional[np.ndarray]  = None
    extra: List[GeneralStorage] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MeshHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    vsize: int
    lsize: int
    flag: int
    time: int
    surf: int

class Mesh(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: MeshHeader
    raw_vertices: np.ndarray
    raw_indices: np.ndarray
    extra: List[GeneralStorage] = []

    model_config = ConfigDict(arbitrary_types_allowed=True)

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
        return self.raw_vertices.reshape((-1, 3))

    @property
    def indices(self) -> np.ndarray:
        return self.raw_indices[np.where(self.raw_indices >= 0)].reshape((-1, 3))

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


class Object(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    header: ObjectHeader = ObjectHeader()
    contours: List[Contour] = []
    meshes: List[Mesh] = []
    extra: List[GeneralStorage] = []
    imat: Optional[IMAT] = None


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

    @classmethod
    def from_file(cls, filename: os.PathLike):
        """Read an IMOD model from disk."""
        from .parsers import parse_model
        with open(filename, 'rb') as file:
            return parse_model(file)
    
    def to_file(self, filename: os.PathLike):
        """Write an IMOD model to disk."""
        from .writers import write_model
        self.header.objsize = len(self.objects)
        with open(filename, 'wb') as file:
            write_model(file, self)

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
    name: str
    xmax: int
    ymax: int
    zmax: int
    objsize: int
    flags: int
    drawmode: int
    mousemode: int
    blacklevel: int
    whitelevel: int
    xoffset: float
    yoffset: float
    zoffset: float
    xscale: float
    yscale: float
    zscale: float
    object: int
    contour: int
    point: int
    res: int
    thresh: int
    pixelsize: float
    units: int
    csum: int
    alpha: float
    beta: float
    gamma: float

    @field_validator('name', mode="before")
    @classmethod
    def decode_null_terminated_byte_string(cls, value: bytes):
        end = value.find(b'\x00')
        return value[:end].decode('utf-8')


class ObjectHeader(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    name: str
    extra_data: List[int]
    contsize: int
    flags: int
    axis: int
    drawmode: int
    red: float
    green: float
    blue: float
    pdrawsize: int
    symbol: int
    symsize: int
    linewidth2: int
    linewidth: int
    linesty: int
    symflags: int
    sympad: int
    trans: int
    meshsize: int
    surfsize: int

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
    ambient: int
    diffuse: int
    specular: int
    shininess: int
    fillred: int
    fillgreen: int
    fillblue: int
    quality: int
    mat2: int
    valblack: int
    valwhite: int
    matflags2: int
    mat3b3: int

class MINX(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    oscale: Tuple[float, float, float]
    otrans: Tuple[float, float, float]
    orot: Tuple[float, float, float]
    cscale: Tuple[float, float, float]
    ctrans: Tuple[float, float, float]
    crot: Tuple[float, float, float]


class Size(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    sizes: float


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
    header: ObjectHeader
    contours: List[Contour] = []
    meshes: List[Mesh] = []
    extra: List[GeneralStorage] = []
    imat: Optional[IMAT] = None

    @classmethod
    def scattered_points(cls, points: np.ndarray, size = 2):
        """Create a new object with scattered points."""
        return cls(
                header=ObjectHeader(
                    name=b'', 
                    extra_data=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                    contsize=1, 
                    flags=402653704, 
                    axis=0, 
                    drawmode=1, 
                    red=0.0, 
                    green=1.0, 
                    blue=0.0, 
                    pdrawsize=size, 
                    symbol=1, 
                    symsize=3, 
                    linewidth2=1, 
                    linewidth=1, 
                    linesty=0, 
                    symflags=0, 
                    sympad=0, 
                    trans=0, 
                    meshsize=0, 
                    surfsize=0), 
                contours=[
                    Contour(header=ContourHeader(
                        psize=len(points), 
                        flags=16, 
                        time=0, 
                        surf=0), 
                        points=points,
                        extra=[]
                        )
                    ], 
                meshes=[], 
                extra=[], 
                imat=IMAT(
                    ambient=102, 
                    diffuse=255, 
                    specular=127, 
                    shininess=4, 
                    fillred=0, 
                    fillgreen=0, 
                    fillblue=0, 
                    quality=0, 
                    mat2=0, 
                    valblack=0, 
                    valwhite=255, 
                    matflags2=0, 
                    mat3b3=0)
            )


class ImodModel(BaseModel):
    """Contents of an IMOD model file.

    https://bio3d.colorado.edu/imod/doc/binspec.html
    """
    id: ID
    header: ModelHeader
    objects: List[Object]
    slicer_angles: List[SLAN] = []
    minx: Optional[MINX]
    extra: List[GeneralStorage] = []

    @classmethod
    def from_file(cls, filename: os.PathLike):
        """Read an IMOD model from disk."""
        from .parsers import parse_model
        with open(filename, 'rb') as file:
            return parse_model(file)

    @classmethod
    def new(cls):
        """Create a new, empty model."""
        return cls(
                id=ID(IMOD_file_id='IMOD', version_id='V1.2'),
                header=ModelHeader(
                    name=b'IMOD-NewModel', 
                    xmax=0, 
                    ymax=0, 
                    zmax=0, 
                    objsize=1, 
                    flags=15872, 
                    drawmode=1, 
                    mousemode=2, 
                    blacklevel=0, 
                    whitelevel=255, 
                    xoffset=0.0, 
                    yoffset=0.0, 
                    zoffset=0.0, 
                    xscale=1.0, 
                    yscale=1.0, 
                    zscale=1.0, 
                    object=0, 
                    contour=0, 
                    point=-1, 
                    res=3, 
                    thresh=128, 
                    pixelsize=1.0, 
                    units=0, 
                    csum=0, 
                    alpha=0.0, 
                    beta=0.0, 
                    gamma=0.0),
                objects=[],
                slicer_angles=[], 
                minx=None, 
                extra=[]
                )
    


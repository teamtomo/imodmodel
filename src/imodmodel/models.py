import os
from typing import Any, Tuple, List, Optional

import numpy as np
from pydantic import BaseModel, validator


class ID(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    IMOD_file_id: str
    version_id: str


class GeneralStorage(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    type: int
    flags: int
    index: Any
    value: Any


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

    @validator('name', pre=True)
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

    @validator('name', pre=True)
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

    class Config:
        arbitrary_types_allowed = True


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
    vertices: np.ndarray # vert
    indices: np.ndarray # list
    extra: List[GeneralStorage] = []

    class Config:
        arbitrary_types_allowed = True

    def reshaped_indices(self) -> np.ndarray:
        return self.indices[np.where(self.indices >= 0)].reshape((-1, 3))

    def extra_values(self) -> np.ndarray:
        # The extra values are index, value  pairs
        # However, the index is an index into the indices array,
        # not directly an index of a vertex.
        # Furthermore, the index has to be fixed because
        # the original indices array has special command values (-25, -22, -1, ...)
        values = np.zeros((len(self.vertices),))
        for extra in self.extra:
            if not (extra.type == 10 and isinstance(extra.index, int)):
                continue
            # removed_indices = np.nonzero(self.indices < 0)[0]
            # index_fixed = extra.index - len(np.nonzero(removed_indices < extra.index)[0])
            values[self.indices[extra.index]] = extra.value
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


class Object(BaseModel):
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    contours: List[Contour] = []
    meshes: List[Mesh] = []
    extra: List[GeneralStorage] = []


class ImodModel(BaseModel):
    """Contents of an IMOD model file.

    https://bio3d.colorado.edu/imod/doc/binspec.html
    """
    id: ID
    header: ModelHeader
    objects: List[Object]
    imat: Optional[IMAT]
    extra: List[GeneralStorage] = []

    @classmethod
    def from_file(cls, filename: os.PathLike):
        """Read an IMOD model from disk."""
        from .parsers import parse_model
        with open(filename, 'rb') as file:
            return parse_model(file)


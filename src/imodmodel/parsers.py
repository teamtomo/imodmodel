import re
from struct import Struct
from typing import Any, BinaryIO, Dict, Tuple

import numpy as np

from .models import (
    ID,
    IMAT,
    Contour,
    ContourHeader,
    Mesh,
    MeshHeader,
    ImodModel,
    ModelHeader,
    Object,
    ObjectHeader,
)
from .binary_specification import ModFileSpecification


def _parse_from_specification(
    file: BinaryIO, specification: Dict[str, str]
) -> Dict[str, Any]:
    format_str = f">{''.join(specification.values())}"
    data_1d = _parse_from_format_str(file, format_str)
    data = {}
    i = 0  # index into 1d data
    for key, value in specification.items():
        if value[0].isdigit() and value[-1] in "iIlLqQfd":  # parse multiple numbers
            n = int(re.match(r"\d+", value).group(0))  # type: ignore
            data[key] = data_1d[i:i+n]
            i += n - 1
        else:
            data[key] = data_1d[i]
        i += 1
    return data


def _parse_from_format_str(file: BinaryIO, format_str: str) -> Tuple[Any, ...]:
    struct = Struct(format_str)
    return struct.unpack(file.read(struct.size))


def _parse_id(file: BinaryIO) -> ID:
    data = _parse_from_specification(file, ModFileSpecification.ID)
    return ID(**data)


def _parse_model_header(file: BinaryIO) -> ModelHeader:
    data = _parse_from_specification(file, ModFileSpecification.MODEL_HEADER)
    return ModelHeader(**data)


def _parse_object_header(file: BinaryIO) -> ObjectHeader:
    data = _parse_from_specification(file, ModFileSpecification.OBJECT_HEADER)
    return ObjectHeader(**data)


def _parse_object(file: BinaryIO) -> Object:
    header = _parse_object_header(file)
    contours = []
    meshes = []
    for _ in range(header.contsize):
        _parse_control_sequence(file)
        contours.append(_parse_contour(file))
    for _ in range(header.meshsize):
        _parse_control_sequence(file)
        meshes.append(_parse_mesh(file))
    return Object(contours=contours, meshes=meshes)


def _parse_contour_header(file: BinaryIO) -> ContourHeader:
    data = _parse_from_specification(file, ModFileSpecification.CONTOUR_HEADER)
    return ContourHeader(**data)


def _parse_contour(file: BinaryIO) -> Contour:
    header = _parse_contour_header(file)
    pt = _parse_from_format_str(file, f">{'fff' * header.psize}")
    pt = np.array(pt).reshape((-1, 3))
    return Contour(header=header, points=pt)


def _parse_mesh_header(file: BinaryIO) -> MeshHeader:
    data = _parse_from_specification(file, ModFileSpecification.MESH_HEADER)
    print(data)
    return MeshHeader(**data)


def _parse_mesh(file: BinaryIO) -> Mesh:
    header = _parse_mesh_header(file)
    all_vertices = _parse_from_format_str(file, f">{'fff' * header.vsize}")
    all_vertices = np.array(all_vertices).reshape((-1, 3))
    # But indices are a list of indices into the vertices array,
    # but there are some special values:
    #  -1  end of list array                
    # -20  next item on list is normal vector.
    # -21  begin polygon with vertices and vertex indices only
    # -22  end polygon
    # -23  begin vertex,normal polygon pairs with normal,vertex indices
    # -24  begin large convex polygon with normals
    # -25  begin vertex,normal polygon pairs with vertex indices
    # So we check where a polygon begins (for now only -25 is supported)
    # split it there and turn it into a list of polygon indices
    all_indices = _parse_from_format_str(file, f">{'i' * header.lsize}")
    all_indices = np.array(all_indices)
    if all_indices[-1] != -1:
        raise ValueError(f'Mesh indices array must end with -1 but ends with {all_indices[-1]}')
    all_indices = all_indices[:-1]
    polygon_start_indices = np.nonzero((all_indices == -25))[0]
    split_indices = np.array_split(all_indices, polygon_start_indices)[1:] # first one is always empty
    # Validate: they should end with a -22
    for polygon_indices in split_indices:
        if polygon_indices[-1] != -22:
            raise ValueError(f"Invalid polygon indices end: {polygon_indices[-1]}")
    # Cut of first and last value of each polygon index list
    split_indices = [idx[1:-1].reshape((-1, 3)) for idx in split_indices]
    return Mesh(header=header, vertices=all_vertices, indices=split_indices)


def _parse_control_sequence(file: BinaryIO) -> str:
    return file.read(4).decode("utf-8")


def _parse_chunk_size(file: BinaryIO) -> int:
    """Numbers are stored in big endian regardless of machine architecture."""
    return int.from_bytes(file.read(4), byteorder="big")


def _parse_imat(file: BinaryIO) -> IMAT:
    _parse_chunk_size(file)
    data = _parse_from_specification(file, ModFileSpecification.IMAT)
    return IMAT(**data)


def _parse_unknown(file: BinaryIO) -> None:
    bytes_to_skip = _parse_chunk_size(file)
    file.read(bytes_to_skip)


def parse_model(file: BinaryIO) -> ImodModel:
    id = _parse_id(file)
    header = _parse_model_header(file)
    control_sequence = _parse_control_sequence(file)
    imat = None

    objects = []
    while control_sequence != "IEOF":
        if control_sequence == "OBJT":
            objects.append(_parse_object(file))
        elif control_sequence == "IMAT":
            imat = _parse_imat(file)
        else:
            _parse_unknown(file)
        control_sequence = _parse_control_sequence(file)
    return ImodModel(id=id, header=header, objects=objects, imat=imat)

import re
from struct import Struct
from typing import Any, BinaryIO, Dict, List, Tuple, Union

import numpy as np

from .models import (
    ID,
    IMAT,
    SLAN,
    Contour,
    ContourHeader,
    GeneralStorage,
    Mesh,
    MeshHeader,
    MINX,
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


def _parse_from_type_flags(file: BinaryIO, flags: int) -> Union[int, float, Tuple[int, int], Tuple[int, int, int, int]]:
    """Determine the next type from a flag, and parse the correct type.
    The general storage chunks (MOST, OBST, MEST, COST) carry values as type unions.
    The type of the union is stored in a 2-bit flag:
    - 0b00: int
    - 0b01: float
    - 0b10: short, short
    - 0b11: byte, byte, byte, byte
    """
    flag_mask, flag_int, flag_float, flag_short, flag_byte = 0b11, 0b00, 0b01, 0b10, 0b11
    if flags & flag_mask == flag_int:
        return _parse_from_format_str(file, '>i')[0]
    elif flags & flag_mask == flag_float:
        return _parse_from_format_str(file, '>f')[0]
    elif flags & flag_mask == flag_short:
        return _parse_from_format_str(file, '>2h')
    elif flags & flag_mask == flag_byte:
        return _parse_from_format_str(file, '>4b')
    else:
        raise ValueError(f'Invalid flags: {flags}')
    

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
    return Object(header=header)


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
    return MeshHeader(**data)


def _parse_mesh(file: BinaryIO) -> Mesh:
    header = _parse_mesh_header(file)
    vertices = _parse_from_format_str(file, f">{'fff' * header.vsize}")
    vertices = np.array(vertices)
    indices = _parse_from_format_str(file, f">{'i' * header.lsize}")
    indices = np.array(indices)
    # Only support the simplest mesh case, which is that each polygon
    # starts with -25 and ends with -22, and the list is terminated by -1
    if any(i in indices for i in (-20, -21, -23, -24)):
        raise ValueError("This mesh type is not yet supported")
    return Mesh(header=header, raw_vertices=vertices, raw_indices=indices)


def _parse_control_sequence(file: BinaryIO) -> str:
    return file.read(4).decode("utf-8")


def _parse_chunk_size(file: BinaryIO) -> int:
    """Numbers are stored in big endian regardless of machine architecture."""
    return int.from_bytes(file.read(4), byteorder="big")


def _parse_imat(file: BinaryIO) -> IMAT:
    _parse_chunk_size(file)
    data = _parse_from_specification(file, ModFileSpecification.IMAT)
    return IMAT(**data)

def _parse_minx(file: BinaryIO) -> MINX:
    _parse_chunk_size(file)
    data = _parse_from_specification(file, ModFileSpecification.MINX)
    return MINX(**data)

def _parse_general_storage(file: BinaryIO) -> List[GeneralStorage]:
    size = _parse_chunk_size(file)
    if size % 12 != 0:
        raise ValueError(f"Chunk size not divisible by 12: {size}")
    storages = list()
    n_chunks = size // 12
    for _ in range(n_chunks):
        type, flags = _parse_from_format_str(file, '>hh')
        index = _parse_from_type_flags(file, flags)
        value = _parse_from_type_flags(file, flags>>2)
        storages.append(GeneralStorage(type=type, flags=flags, index=index, value=value))
    return storages

def _parse_point_sizes(file: BinaryIO, psize : int) -> np.ndarray:
    _parse_chunk_size(file)
    point_sizes = _parse_from_format_str(file, f">{'f' * psize}")
    return np.array(point_sizes).reshape(-1)

def _parse_slicer_angle(file: BinaryIO) -> SLAN:
    _parse_chunk_size(file)
    data = _parse_from_specification(file, ModFileSpecification.SLAN)
    return SLAN(**data)

def _parse_unknown(file: BinaryIO) -> None:
    bytes_to_skip = _parse_chunk_size(file)
    file.read(bytes_to_skip)


def parse_model(file: BinaryIO) -> ImodModel:
    id = _parse_id(file)
    header = _parse_model_header(file)
    control_sequence = _parse_control_sequence(file)
    slicer_angles = []
    minx = None
    extra = list()

    objects = []
    while control_sequence != "IEOF":
        if control_sequence == "OBJT":
            objects.append(_parse_object(file))
        elif control_sequence == "IMAT":
            objects[-1].imat = _parse_imat(file)
        elif control_sequence == "CONT":
            objects[-1].contours.append(_parse_contour(file))
        elif control_sequence == "MESH":
            objects[-1].meshes.append(_parse_mesh(file))
        elif control_sequence == "MOST":
            extra += _parse_general_storage(file)
        elif control_sequence == "OBST":
            objects[-1].extra += _parse_general_storage(file)
        elif control_sequence == "COST":
            objects[-1].contours[-1].extra += _parse_general_storage(file)
        elif control_sequence == "MEST":
            objects[-1].meshes[-1].extra += _parse_general_storage(file)
        elif control_sequence == "SLAN":
            slicer_angles.append(_parse_slicer_angle(file))
        elif control_sequence == "MINX":
            minx = _parse_minx(file)
        elif control_sequence == "SIZE":
            psize = objects[-1].contours[-1].header.psize
            objects[-1].contours[-1].point_sizes =_parse_point_sizes(file,psize)
        else:
            _parse_unknown(file)
        control_sequence = _parse_control_sequence(file)
    return ImodModel(id=id, header=header, objects=objects, slicer_angles=slicer_angles, minx=minx, extra=extra)

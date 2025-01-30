
from struct import Struct
from typing import BinaryIO, List, Union

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



def _write_to_format_str(file: BinaryIO, format_str: str, data: Union[tuple, list]):
    # Convert data to bytes
    data = [s.encode("utf-8") if isinstance(s, str) else s for s in data]
    struct = Struct(format_str)
    file.write(struct.pack(*data))


def _write_to_specification(file: BinaryIO, specification: dict, data: dict):
    format_str = f">{''.join(specification.values())}"
    data_1d = []
    for key, value in specification.items():
        if value[0].isdigit() and value[-1] in "iIlLqQfd":
            data_1d.extend(data[key])
        else:
            data_1d.append(data[key])
    _write_to_format_str(file, format_str, data_1d)


def _write_id(file: BinaryIO, id: ID):
    _write_to_specification(file, ModFileSpecification.ID, id.dict())


def _write_model_header(file: BinaryIO, header: ModelHeader):
    _write_to_specification(file, ModFileSpecification.MODEL_HEADER, header.dict())


def _write_object_header(file: BinaryIO, header: ObjectHeader):
    _write_to_specification(file, ModFileSpecification.OBJECT_HEADER, header.dict())


def _write_contour_header(file: BinaryIO, header: ContourHeader):
    _write_to_specification(file, ModFileSpecification.CONTOUR_HEADER, header.dict())


def _write_mesh_header(file: BinaryIO, header: MeshHeader):
    _write_to_specification(file, ModFileSpecification.MESH_HEADER, header.dict())


def _write_imat(file: BinaryIO, imat: IMAT):
    _write_chunk_size(file, 48)
    _write_to_specification(file, ModFileSpecification.IMAT, imat.dict())


def _write_minx(file: BinaryIO, minx: MINX):
    _write_chunk_size(file, 72)
    _write_to_specification(file, ModFileSpecification.MINX, minx.dict())


def _write_slicer_angle(file: BinaryIO, slicer_angle: SLAN):
    _write_chunk_size(file, 48)
    _write_to_specification(file, ModFileSpecification.SLAN, slicer_angle.dict())


def _write_general_storage(file: BinaryIO, storages: List[GeneralStorage]):
    size = len(storages) * 12
    _write_chunk_size(file, size)
    for storage in storages:
        _write_to_format_str(file, '>hh', (storage.type, storage.flags))
        _write_to_format_str(file, '>i' if isinstance(storage.index, int) else '>f', (storage.index,))
        _write_to_format_str(file, '>i' if isinstance(storage.value, int) else '>f', (storage.value,))


def _write_chunk_size(file: BinaryIO, size: int):
    file.write(size.to_bytes(4, byteorder="big"))


def _write_point_sizes(file: BinaryIO, point_sizes: np.ndarray):
    point_sizes = point_sizes.flatten()
    _write_control_sequence(file, "SIZE")
    _write_chunk_size(file, 4 *  len(point_sizes))
    _write_to_format_str(file, f">{'f' * len(point_sizes)}", point_sizes)

def _write_control_sequence(file: BinaryIO, sequence: str):
    file.write(sequence.encode("utf-8"))


def _write_contour(file: BinaryIO, contour: Contour):
    _write_contour_header(file, contour.header)
    points = contour.points.flatten()
    _write_to_format_str(file, f">{'f' * len(points)}", points)

    if contour.point_sizes is not None:
        _write_point_sizes(file, contour.point_sizes)
    if contour.extra:
        _write_general_storage(file, contour.extra)


def _write_mesh(file: BinaryIO, mesh: Mesh):
    _write_mesh_header(file, mesh.header)
    vertices = mesh.raw_vertices.flatten()
    indices = mesh.raw_indices.flatten()
    _write_to_format_str(file, f">{'f' * len(vertices)}", vertices)
    _write_to_format_str(file, f">{'i' * len(indices)}", indices)
    if mesh.extra:
        _write_general_storage(file, mesh.extra)


def _write_object(file: BinaryIO, obj: Object):
    _write_object_header(file, obj.header)
    for contour in obj.contours:
        _write_control_sequence(file, "CONT")
        _write_contour(file, contour)
    for mesh in obj.meshes:
        _write_control_sequence(file, "MESH")
        _write_mesh(file, mesh)
    if obj.imat:
        _write_control_sequence(file, "IMAT")
        _write_imat(file, obj.imat)
    if obj.extra:
        _write_control_sequence(file, "OBST")
        _write_general_storage(file, obj.extra)


def write_model(file: BinaryIO, model: ImodModel):
    _write_id(file, model.id)
    _write_model_header(file, model.header)
    for obj in model.objects:
        _write_control_sequence(file, "OBJT")
        _write_object(file, obj)
    for slicer_angle in model.slicer_angles:
        _write_control_sequence(file, "SLAN")
        _write_slicer_angle(file, slicer_angle)
    if model.minx:
        _write_control_sequence(file, "MINX")
        _write_minx(file, model.minx)
    if model.extra:
        _write_control_sequence(file, "MOST")
        _write_general_storage(file, model.extra)
    _write_control_sequence(file, "IEOF")

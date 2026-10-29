import struct
from io import BytesIO

import numpy as np
import pytest

from imodmodel.parsers import (
    _parse_chunk_size,
    _parse_contour,
    _parse_control_sequence,
    _parse_from_type_flags,
    _parse_general_storage,
    _parse_id,
    _parse_imat,
    _parse_model_header,
    _parse_object_header,
    _parse_point_sizes,
    _parse_slicer_angle,
    parse_model,
)


def test_parse_id(two_contour_model_file_handle):
    """Check that the ID is parsed correctly."""
    model_id = _parse_id(two_contour_model_file_handle)
    assert model_id.IMOD_file_id == "IMOD"
    assert model_id.version_id == "V1.2"
    two_contour_model_file_handle.close()


def test_parse_model_header(two_contour_model_file_handle):
    """Check that the model header is parsed correctly."""
    two_contour_model_file_handle.seek(8)
    object_header = _parse_model_header(two_contour_model_file_handle)
    expected = {
        "alpha": 0.0,
        "beta": 0.0,
        "blacklevel": 38,
        "contour": 0,
        "csum": 382790896,
        "drawmode": 1,
        "flags": 62464,
        "gamma": 0.0,
        "mousemode": 1,
        "name": "IMOD-NewModel",
        "object": 0,
        "objsize": 1,
        "pixelsize": 0.4480000138282776,
        "point": 8,
        "res": 3,
        "thresh": 128,
        "units": -9,
        "whitelevel": 121,
        "xmax": 128,
        "xoffset": 0.0,
        "xscale": 1.0,
        "ymax": 128,
        "yoffset": 0.0,
        "yscale": 1.0,
        "zmax": 128,
        "zoffset": 0.0,
        "zscale": 1.0,
    }
    result = dict(object_header)
    result["flags"] = int(result["flags"])
    assert result == expected
    two_contour_model_file_handle.close()


@pytest.mark.parametrize(
    "position, expected",
    [
        (240, "OBJT"),
        (420, "CONT"),
        (644, "CONT"),
        (760, "IMAT"),
        (784, "VIEW"),
    ],
)
def test_parse_control_sequence(
    two_contour_model_file_handle, position: int, expected: str
):
    """Check that control sequences are correctly parsed."""
    two_contour_model_file_handle.seek(position)
    control_sequence = _parse_control_sequence(two_contour_model_file_handle)
    assert control_sequence == expected
    two_contour_model_file_handle.close()


def test_parse_object_header(two_contour_model_file_handle):
    """Check that object headers are correctly parsed."""
    two_contour_model_file_handle.seek(244)
    object_header = _parse_object_header(two_contour_model_file_handle)
    expected = {
        "axis": 0,
        "blue": 0.0,
        "contsize": 2,
        "drawmode": 1,
        "extra_data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "flags": 402653184,
        "green": 1.0,
        "linesty": 0,
        "linewidth": 1,
        "linewidth2": 1,
        "meshsize": 0,
        "name": "",
        "pdrawsize": 0,
        "red": 0.0,
        "surfsize": 0,
        "symbol": 1,
        "symflags": 0,
        "sympad": 0,
        "symsize": 3,
        "trans": 0,
    }
    result = dict(object_header)
    result["flags"] = int(result["flags"])
    assert result == expected


@pytest.mark.parametrize(
    "position, expected_header, expected_points",
    [
        (
            424,
            {"flags": 0, "psize": 17, "surf": 0, "time": 0},
            np.array(
                [
                    [64.33333588, 64.66666412, 80.0],
                    [47.0, 77.33333588, 80.0],
                    [51.33333206, 45.66666794, 80.0],
                    [87.33333588, 49.66666794, 80.0],
                    [76.0, 82.0, 80.0],
                    [34.33333206, 84.33333588, 80.0],
                    [40.66666794, 31.0, 80.0],
                    [97.33333588, 45.66666794, 80.0],
                    [81.0, 93.33333588, 80.0],
                    [20.0, 93.66666412, 80.0],
                    [32.33333206, 16.33333397, 80.0],
                    [110.0, 41.33333206, 80.0],
                    [86.0, 102.0, 80.0],
                    [10.66666698, 107.33333588, 80.0],
                    [23.66666603, 4.33333349, 80.0],
                    [121.66666412, 37.0, 80.0],
                    [96.33333588, 110.33333588, 80.0],
                ]
            ),
        ),
        (
            648,
            {"flags": 0, "psize": 8, "surf": 0, "time": 0},
            np.array(
                [
                    [64.33333588, 64.0, 59.0],
                    [56.0, 52.66666794, 59.0],
                    [85.33333588, 47.66666794, 59.0],
                    [77.0, 77.0, 59.0],
                    [45.0, 80.0, 59.0],
                    [48.33333206, 48.66666794, 59.0],
                    [96.33333588, 43.0, 59.0],
                    [83.0, 82.0, 59.0],
                ]
            ),
        ),
    ],
)
def test_parse_contour(
    two_contour_model_file_handle,
    position: int,
    expected_header: dict[str, int],
    expected_points: np.ndarray,
):
    """Check that contours are correctly parsed."""
    two_contour_model_file_handle.seek(position)
    contour = _parse_contour(two_contour_model_file_handle)
    header = dict(contour.header)
    header["flags"] = int(header["flags"])
    assert header == expected_header
    assert np.allclose(contour.points, expected_points)
    two_contour_model_file_handle.close()


def test_parse_chunk_size(two_contour_model_file_handle):
    """Check that chunk sizes are parsed correctly."""
    two_contour_model_file_handle.seek(764)
    chunk_size = _parse_chunk_size(two_contour_model_file_handle)
    assert chunk_size == 16
    two_contour_model_file_handle.close()


def test_parse_imat(two_contour_model_file_handle):
    """Check that IMAT blocks are correctly parsed."""
    two_contour_model_file_handle.seek(768)
    imat = _parse_imat(two_contour_model_file_handle)
    expected = {
        "ambient": 0,
        "diffuse": 0,
        "fillblue": 0,
        "fillgreen": 0,
        "fillred": 0,
        "mat2": 16711680,
        "mat3b3": 87,
        "matflags2": 69,
        "quality": 0,
        "shininess": 0,
        "specular": 0,
        "valblack": 86,
        "valwhite": 73,
    }
    assert imat.dict() == expected
    two_contour_model_file_handle.close()


@pytest.mark.parametrize(
    "position, expected_time, expected_angles, expected_center, expected_label",
    [
        (
            1047,
            1,
            np.array([13.100000, 0.0, -30.200001]),
            np.array([235.519577, 682.744141, 302.0]),
            "label1",
        ),
        (
            1115,
            1,
            np.array([-41.400002, 0.0, -47.700001]),
            np.array([221.942444, 661.193237, 327.0]),
            "",
        ),
        (
            1183,
            1,
            np.array([-41.400002, 0.0, -41.799999]),
            np.array([232.790726, 671.332031, 327.0]),
            "label3",
        ),
        (
            1251,
            1,
            np.array([-35.500000, 0.0, -36.000000]),
            np.array([240.129181, 679.927795, 324.0]),
            "",
        ),
    ],
)
def test_parse_slicer_angles(
    slicer_angle_model_file_handle,
    position: int,
    expected_time: int,
    expected_angles: np.ndarray,
    expected_center: np.ndarray,
    expected_label: str,
):
    slicer_angle_model_file_handle.seek(position)
    slicer_angle = _parse_slicer_angle(slicer_angle_model_file_handle)
    assert slicer_angle.time == expected_time
    assert np.allclose(slicer_angle.angles, expected_angles)
    assert np.allclose(slicer_angle.center, expected_center)
    assert slicer_angle.label == expected_label
    slicer_angle_model_file_handle.close()


@pytest.mark.parametrize(
    "data, flag, index_expected, value_expected",
    [
        (struct.pack(">ii", 1, 2), 0b000, 1, 2),
        (struct.pack(">if", 1, 2.0), 0b0100, 1, 2.0),
        (struct.pack(">ihh", 1, 2, 3), 0b1000, 1, (2, 3)),
        (struct.pack(">i4b", 1, 2, 3, 4, 5), 0b1100, 1, (2, 3, 4, 5)),
    ],
)
def test_parse_from_flags(data, flag, index_expected, value_expected):
    """Check that unions are correctly parsed"""
    stream = BytesIO(data)
    index = _parse_from_type_flags(stream, flag)
    value = _parse_from_type_flags(stream, flag >> 2)
    assert index == index_expected
    assert value == value_expected


def test_parse_curvature(meshed_curvature_model_file_handle):
    """Check that curvature values stored in GeneralStorage are correctly parsed"""
    meshed_curvature_model_file_handle.seek(20924)
    general_storages = _parse_general_storage(meshed_curvature_model_file_handle)
    assert len(general_storages) == 377
    for store in general_storages:
        assert store.type == 10
        assert store.flags == 4
        assert isinstance(store.index, int)
        assert isinstance(store.value, float)


@pytest.mark.parametrize(
    "position, psize, expected_point_sizes",
    [(492, 4, np.array([28.39998245, 33.99998474, 18.79999161, 22.79998779]))],
)
def test_parse_point_sizes(
    point_sizes_model_file_handle,
    position: int,
    psize: int,
    expected_point_sizes: np.ndarray,
):
    """Check that point sizes are correctly parsed."""
    point_sizes_model_file_handle.seek(position)
    point_sizes = _parse_point_sizes(point_sizes_model_file_handle, psize)
    assert np.allclose(point_sizes, expected_point_sizes)
    point_sizes_model_file_handle.close()


def test_parse_model(two_contour_model_file_handle):
    """Check that model file is parsed correctly."""
    parse_model(two_contour_model_file_handle)
    two_contour_model_file_handle.close()

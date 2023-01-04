from typing import Dict

import numpy as np
import pytest

from imodmodel.parsers import (
    _parse_id,
    _parse_model_header,
    _parse_control_sequence,
    _parse_object_header,
    _parse_contour,
    _parse_imat,
    _parse_chunk_size,
    parse_model,
)


def test_parse_id(two_contour_model_file_handle):
    """Check that the ID is parsed correctly."""
    id = _parse_id(two_contour_model_file_handle)
    assert id.IMOD_file_id == 'IMOD'
    assert id.version_id == 'V1.2'
    two_contour_model_file_handle.close()


def test_parse_model_header(two_contour_model_file_handle):
    """Check that the model header is parsed correctly."""
    two_contour_model_file_handle.seek(8)
    object_header = _parse_model_header(two_contour_model_file_handle)
    expected = {
        'alpha': 0.0,
        'beta': 0.0,
        'blacklevel': 38,
        'contour': 0,
        'csum': 382790896,
        'drawmode': 1,
        'flags': 62464,
        'gamma': 0.0,
        'mousemode': 1,
        'name': 'IMOD-NewModel',
        'object': 0,
        'objsize': 1,
        'pixelsize': 0.4480000138282776,
        'point': 8,
        'res': 3,
        'thresh': 128,
        'units': -9,
        'whitelevel': 121,
        'xmax': 128,
        'xoffset': 0.0,
        'xscale': 1.0,
        'ymax': 128,
        'yoffset': 0.0,
        'yscale': 1.0,
        'zmax': 128,
        'zoffset': 0.0,
        'zscale': 1.0
    }
    assert object_header.dict() == expected
    two_contour_model_file_handle.close()


@pytest.mark.parametrize(
    "position, expected",
    [
        (240, 'OBJT'),
        (420, 'CONT'),
        (644, 'CONT'),
        (760, 'IMAT'),
        (784, 'VIEW'),
    ]
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
        'axis': 0,
        'blue': 0.0,
        'contsize': 2,
        'drawmode': 1,
        'extra_data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'flags': 402653184,
        'green': 1.0,
        'linesty': 0,
        'linewidth': 1,
        'linewidth2': 1,
        'meshsize': 0,
        'name': '',
        'pdrawsize': 0,
        'red': 0.0,
        'surfsize': 0,
        'symbol': 1,
        'symflags': 0,
        'sympad': 0,
        'symsize': 3,
        'trans': 0
    }
    assert object_header.dict() == expected


@pytest.mark.parametrize(
    'position, expected_header, expected_points',
    [
        (
            424,
            {'flags': 0, 'psize': 17, 'surf': 0, 'time': 0},
            np.array([[64.33333588, 64.66666412, 80.],
                      [47., 77.33333588, 80.],
                      [51.33333206, 45.66666794, 80.],
                      [87.33333588, 49.66666794, 80.],
                      [76., 82., 80.],
                      [34.33333206, 84.33333588, 80.],
                      [40.66666794, 31., 80.],
                      [97.33333588, 45.66666794, 80.],
                      [81., 93.33333588, 80.],
                      [20., 93.66666412, 80.],
                      [32.33333206, 16.33333397, 80.],
                      [110., 41.33333206, 80.],
                      [86., 102., 80.],
                      [10.66666698, 107.33333588, 80.],
                      [23.66666603, 4.33333349, 80.],
                      [121.66666412, 37., 80.],
                      [96.33333588, 110.33333588, 80.]])
        ),
        (
            648,
            {'flags': 0, 'psize': 8, 'surf': 0, 'time': 0},
            np.array([[64.33333588, 64., 59.],
                      [56., 52.66666794, 59.],
                      [85.33333588, 47.66666794, 59.],
                      [77., 77., 59.],
                      [45., 80., 59.],
                      [48.33333206, 48.66666794, 59.],
                      [96.33333588, 43., 59.],
                      [83., 82., 59.]])
        )
    ]
)
def test_parse_contour(
    two_contour_model_file_handle,
    position: int,
    expected_header: Dict[str, int],
    expected_points: np.ndarray,
):
    """Check that contours are correctly parsed."""
    two_contour_model_file_handle.seek(position)
    contour = _parse_contour(two_contour_model_file_handle)
    assert contour.dict()['header'] == expected_header
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
        'ambient': 0,
        'diffuse': 0,
        'fillblue': 0,
        'fillgreen': 0,
        'fillred': 0,
        'mat2': 16711680,
        'mat3b3': 87,
        'matflags2': 69,
        'quality': 0,
        'shininess': 0,
        'specular': 0,
        'valblack': 86,
        'valwhite': 73
    }
    assert imat.dict() == expected
    two_contour_model_file_handle.close()


def test_parse_model(two_contour_model_file_handle):
    """Check that model file is parsed correctly."""
    parse_model(two_contour_model_file_handle)
    two_contour_model_file_handle.close()

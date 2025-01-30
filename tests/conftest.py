import pytest
from pathlib import Path

TEST_DATA_DIRECTORY = Path(__file__).parent / 'test_data'


@pytest.fixture
def two_contour_model_file() -> Path:
    """A simple model file with two contours."""
    return TEST_DATA_DIRECTORY / 'two_contour_example.mod'


@pytest.fixture
def two_contour_model_file_handle(two_contour_model_file):
    """A file handle for a simple model with two contours."""
    return open(two_contour_model_file, mode='rb')


@pytest.fixture
def meshed_contour_model_file() -> Path:
    """A model file with meshed contours."""
    return TEST_DATA_DIRECTORY / 'meshed_contour_example.mod'


@pytest.fixture
def meshed_curvature_model_file() -> Path:
    """A model file with curvature measurements from imodcurvature"""
    return TEST_DATA_DIRECTORY / 'meshed_curvature_example.mod'


@pytest.fixture
def meshed_curvature_model_file_handle(meshed_curvature_model_file):
    """A file handle with curvature measurements from imodcurvature"""
    return open(meshed_curvature_model_file, mode='rb')

@pytest.fixture
def slicer_angle_model_file() -> Path:
    """A model file from Mohammed's slicerangle measurements."""
    return TEST_DATA_DIRECTORY / 'slicer_angle_example.mod'

@pytest.fixture
def slicer_angle_model_file_handle(slicer_angle_model_file):
    """A file handle with Mohammed's slicerangle measurements."""
    return open(slicer_angle_model_file, mode='rb')

@pytest.fixture
def multiple_objects_model_file() -> Path:
    """A model file containing multiple object data."""
    return TEST_DATA_DIRECTORY / 'multiple_objects_example.mod'

@pytest.fixture
def multiple_objects_model_file_handle(slicer_angle_model_file):
    """A file handle with multiple object data."""
    return open(slicer_angle_model_file, mode='rb')

@pytest.fixture
def point_sizes_model_file() -> Path:
    """A model file containing multiple object data."""
    return TEST_DATA_DIRECTORY / 'point_sizes_example.mod'

@pytest.fixture
def point_sizes_model_file_handle(point_sizes_model_file):
    """A file handle with multiple object data."""
    return open(point_sizes_model_file, mode='rb')

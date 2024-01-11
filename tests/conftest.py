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

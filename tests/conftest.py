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

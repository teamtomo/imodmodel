import pandas as pd
import pytest

import imodmodel
from pathlib import Path
TEST_FILE = Path(__file__).parent / 'test_data' / 'two_contour_example.mod'


@pytest.mark.filterwarnings("ignore:UserWarning")
def test_read():
    """Test that reading a simple example file works."""
    df = imodmodel.read(TEST_FILE)
    assert isinstance(df, pd.DataFrame)

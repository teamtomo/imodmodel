import pandas as pd
import pytest
import imodmodel


@pytest.mark.filterwarnings("ignore:UserWarning")
def test_read(two_contour_model_file):
    """Test that reading a simple example file works."""
    df = imodmodel.read(two_contour_model_file)
    assert isinstance(df, pd.DataFrame)

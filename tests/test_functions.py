import pandas as pd

import imodmodel


def test_read(two_contour_model_file):
    """Check that model files can be read."""
    df = imodmodel.read(two_contour_model_file)
    assert isinstance(df, pd.DataFrame)
    expected_columns = ['object_id', 'contour_id', 'x', 'y', 'z']
    assert all(col in expected_columns for col in df.columns)
    assert df.shape == (25, 5)
    assert df['object_id'].nunique() == 1
    assert df['contour_id'].nunique() == 2

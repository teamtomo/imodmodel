import pandas as pd

import imodmodel


def test_read(two_contour_model_file, meshed_contour_model_file):
    """Check that model files can be read."""
    example_files = [two_contour_model_file, meshed_contour_model_file]
    expected_columns = ['object_id', 'contour_id', 'x', 'y', 'z']

    for file in example_files:
        df = imodmodel.read(file)
        assert isinstance(df, pd.DataFrame)
        assert all(col in expected_columns for col in df.columns)

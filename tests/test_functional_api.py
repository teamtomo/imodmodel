import pandas as pd
import pytest

import imodmodel


def test_read(two_contour_model_file, meshed_contour_model_file, slan_model_file):
    """Check that model files can be read."""
    example_contour_files = [two_contour_model_file, meshed_contour_model_file]
    example_slan_files = [slan_model_file]
    expected_contour_columns = ['object_id', 'contour_id', 'x', 'y', 'z']
    expected_slan_columns = [
        'object_id', 'slan_id', 'time', 'x_rot', 'y_rot', 'z_rot', 'center_x',
        'center_y', 'center_z', 'label']

    for file in example_contour_files:
        contour_df = imodmodel.read(file)
        assert isinstance(contour_df, pd.DataFrame)
        assert all(col in expected_contour_columns for col in contour_df.columns)


    for file in example_slan_files:
        slan_df = imodmodel.read(file,annotation='slan')
        assert isinstance(slan_df, pd.DataFrame)
        assert all(col in expected_slan_columns for col in slan_df.columns)

def test_no_slan(two_contour_model_file):
    """Check that an error is raised if a model with no SLANs is read with the 'slan' annotation."""
    with pytest.raises(ValueError,match="Model has no SLANs."):
        df = imodmodel.read(two_contour_model_file, annotation='slan')

def test_unknown_annotation(two_contour_model_file):
    """Check that an error is raised if an unknown annotation is requested."""
    with pytest.raises(ValueError,match="Unknown annotation type: unknown"):
        df = imodmodel.read(two_contour_model_file, annotation='unknown')

import pandas as pd
import pytest

import imodmodel


def test_read(two_contour_model_file, meshed_contour_model_file, slicer_angle_model_file):
    """Check that model files can be read."""
    example_contour_files = [two_contour_model_file, meshed_contour_model_file, slicer_angle_model_file]
    example_slicer_angle_files = [slicer_angle_model_file]
    expected_contour_columns = ['object_id', 'contour_id', 'x', 'y', 'z']
    expected_slicer_angle_columns = [
        'object_id', 'slicer_angle_id', 'time', 'x_rot', 'y_rot', 'z_rot', 'center_x',
        'center_y', 'center_z', 'label']

    for file in example_contour_files:
        contour_df = imodmodel.read(file)
        assert isinstance(contour_df, pd.DataFrame)
        assert all(col in expected_contour_columns for col in contour_df.columns)

    for file in example_slicer_angle_files:
        slicer_angle_df = imodmodel.read(file, annotation='slicer_angles')
        assert isinstance(slicer_angle_df, pd.DataFrame)
        assert all(col in expected_slicer_angle_columns for col in slicer_angle_df.columns)


def test_no_slicer_angles(two_contour_model_file):
    """Check that an error is raised if a model with no slicer_angles is read with the 'slicer_angle' annotation."""
    with pytest.raises(ValueError, match="Model has no slicer angles."):
        df = imodmodel.read(two_contour_model_file, annotation='slicer_angles')


def test_unknown_annotation(two_contour_model_file):
    """Check that an error is raised if an unknown annotation is requested."""
    with pytest.raises(ValueError, match="Unknown annotation type: unknown"):
        df = imodmodel.read(two_contour_model_file, annotation='unknown')

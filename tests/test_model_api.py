import pytest
from imodmodel import ImodModel
from imodmodel.models import (
    Contour,
    ContourHeader,
    Mesh,
    IMAT,
    SLAN,
    MeshHeader,
    Object,
    ObjectHeader,
)


@pytest.mark.parametrize(
    "file_fixture_contour, meshes_expected",
    [
        ('two_contour_model_file', 0),
        ('meshed_contour_model_file', 1),

    ]
)
def test_read_contour(file_fixture_contour, meshes_expected, request):
    """Check the model based API"""
    file = request.getfixturevalue(file_fixture_contour)
    model = ImodModel.from_file(file)
    assert isinstance(model, ImodModel)
    assert len(model.objects) == 1
    assert isinstance(model.objects[0], Object)
    assert isinstance(model.objects[0].header, ObjectHeader)
    assert isinstance(model.objects[0].contours[0], Contour)
    assert isinstance(model.objects[0].contours[0].header, ContourHeader)
    assert len(model.objects[0].meshes) == meshes_expected
    if meshes_expected:
        assert isinstance(model.objects[0].meshes[0], Mesh)
        assert isinstance(model.objects[0].meshes[0].header, MeshHeader)

@pytest.mark.parametrize(
    "file_fixture_slicer_angle",
    [
        ('slicer_angle_model_file'),
    ]
)
def test_read_slicer_angle(file_fixture_slicer_angle, request):
    """Check the model based API"""
    file = request.getfixturevalue(file_fixture_slicer_angle)
    model = ImodModel.from_file(file)
    assert isinstance(model, ImodModel)
    assert len(model.slicer_angles) == 4
    assert isinstance(model.slicer_angles, list)
    assert isinstance(model.slicer_angles[0], SLAN)

@pytest.mark.parametrize(
    "file_fixture_multiple_objects, objects_expected", 
    [
        ('multiple_objects_model_file', 3),
    ]
)
def test_multiple_objects(file_fixture_multiple_objects, objects_expected, request):
    file = request.getfixturevalue(file_fixture_multiple_objects)
    model = ImodModel.from_file(file)
    assert isinstance(model, ImodModel)
    assert len(model.objects) == objects_expected
    assert isinstance(model.objects[0], Object)
    assert isinstance(model.objects[0].imat, IMAT)
    assert isinstance(model.objects[1].contours[0], Contour)
    assert isinstance(model.objects[1], Object)
    assert isinstance(model.objects[1].imat, IMAT)
    assert isinstance(model.objects[2].contours[0], Contour)


def test_read_minx(meshed_contour_model_file):
    """Check reading of model to image transformation information."""
    model = ImodModel.from_file(meshed_contour_model_file)
    assert isinstance(model, ImodModel)
    assert model.minx.cscale == pytest.approx((10.680000, 10.680000, 10.680000), abs=1e-6)
    assert model.minx.ctrans == pytest.approx((-2228.0, 2228.0, 681.099976), abs=1e-6)
    assert model.minx.crot == pytest.approx((0.0, 0.0, 0.0), abs=1e-6)


def test_write_scattered_points(tmp_path):
    """Check writing of scattered points model. Test by parsing the written file."""
    import numpy as np

    model = ImodModel()
    model.objects.append(Object.new_scattered_points_object(
        points=np.array([(1, 2, 3), (0, 1, 1), (8, 4, 5)])
    ))
    model.to_file(tmp_path / "scattered_points_model.imod")
    second_model = ImodModel.from_file(tmp_path / "scattered_points_model.imod")
    assert np.allclose(model.objects[0].contours[0].points, second_model.objects[0].contours[0].points)

def test_write_multiple_scattered_points(tmp_path):
    """Check writing of scattered points model. Test by parsing the written file."""
    import numpy as np

    model = ImodModel()
    model.objects.append(Object.new_scattered_points_object(
        points=np.array([(1, 2, 3), (0, 1, 1), (8, 4, 5)])
    ))
    model.objects.append(Object.new_scattered_points_object(
        points=np.array([(9, 0, 1), (8.2, 1, 1), (8.9, 4, 5)])
    ))
    model.to_file(tmp_path / "multiple_scattered_points_model.imod")
    second_model = ImodModel.from_file(tmp_path / "multiple_scattered_points_model.imod")
    assert np.allclose(model.objects[0].contours[0].points, second_model.objects[0].contours[0].points)
    assert np.allclose(model.objects[1].contours[0].points, second_model.objects[1].contours[0].points)

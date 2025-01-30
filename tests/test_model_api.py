import pytest
import numpy as np
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

def test_point_sizes(point_sizes_model_file):
    model = ImodModel.from_file(point_sizes_model_file)
    assert isinstance(model, ImodModel)
    
    # check point sizes are on contour in object with point sizes
    object_with_point_sizes = model.objects[0]
    assert isinstance(object_with_point_sizes.contours[0].point_sizes, np.ndarray)
    
    # check point sizes aren't on contour in object without point sizes
    object_without_point_sizes = model.objects[1]
    assert object_without_point_sizes.contours[0].point_sizes is None


def test_read_write_read_roundtrip(two_contour_model_file, tmp_path):
    """Check that reading and writing a model file results in the same data."""
    import numpy as np

    model = ImodModel.from_file(two_contour_model_file)
    model.to_file(tmp_path / "test_model.imod")
    model2 = ImodModel.from_file(tmp_path / "test_model.imod")
    assert model.header == model2.header
    assert model.objects[0].header == model2.objects[0].header
    assert model.objects[0].contours[0].header == model2.objects[0].contours[0].header
    assert np.allclose(model.objects[0].contours[0].points, model2.objects[0].contours[0].points)
    assert model.objects[0].contours[1].header == model2.objects[0].contours[1].header
    assert np.allclose(model.objects[0].contours[1].points, model2.objects[0].contours[1].points)
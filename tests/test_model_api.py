import pytest
from imodmodel import ImodModel
from imodmodel.models import (
    Contour,
    ContourHeader,
    Mesh,
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
    "file_fixture_slan",
    [
        ('slan_model_file'),
    ]
)
def test_read_slan(file_fixture_slan, request):
    """Check the model based API"""
    file = request.getfixturevalue(file_fixture_slan)
    model = ImodModel.from_file(file)
    assert isinstance(model, ImodModel)
    assert len(model.objects) == 1
    assert isinstance(model.objects[0], Object)
    assert isinstance(model.objects[0].slans[0], SLAN)

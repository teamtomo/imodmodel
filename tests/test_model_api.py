import pytest
from pytest_lazyfixture import lazy_fixture

from imodmodel import ImodModel
from imodmodel.models import Object, ObjectHeader, Contour, ContourHeader, Mesh, MeshHeader

@pytest.mark.parametrize(
    "file, meshes_expected",
    [
        (lazy_fixture('two_contour_model_file'), 0),
        (lazy_fixture('meshed_contour_model_file'), 1),

    ]
)
def test_read(file, meshes_expected):
    """Check the model based API"""
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

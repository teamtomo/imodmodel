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
    # Check that the label is string
    assert isinstance(model.slicer_angles[0].label, str)

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


def test_read_write_read_roundtrip_slicer_angles(slicer_angle_model_file, tmp_path):
    """Check that reading and writing a model file results in the same data."""
    model = ImodModel.from_file(slicer_angle_model_file)
    model.to_file(tmp_path / "test_model.imod")
    model2 = ImodModel.from_file(tmp_path / "test_model.imod")
    assert model.slicer_angles[0].label == model2.slicer_angles[0].label

    
def test_color_syntactic_sugar(two_contour_model_file):
    """Check that the color property of the model object is a tuple."""
    model = ImodModel.from_file(two_contour_model_file)
    assert model.objects[0].color == (0.0, 1.0, 0.0)

    random_color = tuple(np.random.rand(3))  # Generate a random color tuple
    model.objects[0].color = random_color
    # Check if the color has been updated
    assert model.objects[0].header.red == random_color[0]
    assert model.objects[0].header.green == random_color[1]
    assert model.objects[0].header.blue == random_color[2]

    test_object = Object(color=random_color)
    assert test_object.header.red == random_color[0]
    assert test_object.header.green == random_color[1]
    assert test_object.header.blue == random_color[2]

    # Test that directly changing header set color tuple
    test_object.header.red = 0.5
    test_object.header.green = 0.2
    test_object.header.blue = 0.8
    assert test_object.color == (0.5, 0.2, 0.8)

def test_object_creation_and_write(tmp_path):
    
    test_model = ImodModel(
        objects = [
            Object(
            contours = [
                Contour(
                    points = np.random.rand(23, 3),  # Random points for the contour
                ) for _ in range(25)
            ]) for _ in range(30)
        ]
    )

    test_model.to_file(tmp_path / "test_model_many_contours.imod")
    
    # Now read the model back to check if it was written correctly
    model_read_back = ImodModel.from_file(tmp_path / "test_model_many_contours.imod")
    assert isinstance(model_read_back, ImodModel)
    assert len(model_read_back.objects) == 30
    assert len(model_read_back.objects[0].contours) == 25  
    assert model_read_back.objects[0].contours[0].points.shape == (23, 3) 

def test_model_flags(two_contour_model_file,tmp_path):
    """Check the model flags property."""
    model = ImodModel.from_file(two_contour_model_file)
    
    # Check the initial flags
    assert model.header.flags.flag0 is False
    assert model.header.flags.current_tilt_angles_are_stored_correctly is True
    assert int(model.header.flags) == 62464

    model.header.flags.flag0 = True
    assert int(model.header.flags) == 62465
    model.header.flags.current_tilt_angles_are_stored_correctly = False
    assert int(model.header.flags) == 29697

    model.to_file(tmp_path / "test_model_with_flags.imod")
    # Read back the model to check if flags were set correctly
    read_back_model = ImodModel.from_file(tmp_path / "test_model_with_flags.imod")
    assert read_back_model.header.flags.flag0 is True
    assert read_back_model.header.flags.current_tilt_angles_are_stored_correctly is False


def test_object_flags(two_contour_model_file,tmp_path):
    model = ImodModel.from_file(two_contour_model_file)
    initial_object = model.objects[0]
    
    # Check the initial flags
    assert initial_object.header.flags.flag0 is False
    assert initial_object.header.flags.draw_label is True
    assert int(initial_object.header.flags) == 402653184

    initial_object.header.flags.flag0 = True
    assert int(initial_object.header.flags) == 402653185
    initial_object.header.flags.draw_label = False

    model.to_file(tmp_path / "test_object_flags.mode")
    read_back_model = ImodModel.from_file(tmp_path / "test_object_flags.mode")
    read_back_object = read_back_model.objects[0]
    assert read_back_object.header.flags.flag0 == True
    assert read_back_object.header.flags.draw_label == False


def test_contour_flags(two_contour_model_file, tmp_path):
    """Check the contour flags property."""
    model = ImodModel.from_file(two_contour_model_file)
    initial_contour = model.objects[0].contours[0]

    # Check the initial flags
    assert initial_contour.header.flags.flag0 is False
    assert int(initial_contour.header.flags) == 0

    # Modify the flags
    initial_contour.header.flags.flag0 = True
    assert int(initial_contour.header.flags) == 1

    # Write the model to a file and read it back
    model.to_file(tmp_path / "test_contour_flags.imod")
    read_back_model = ImodModel.from_file(tmp_path / "test_contour_flags.imod")
    read_back_contour = read_back_model.objects[0].contours[0]

    # Verify the flags after reading back
    assert read_back_contour.header.flags.flag0 is True
    assert int(read_back_contour.header.flags) == 1
from typing import List

import pandas as pd

from .models import Contour, ImodModel, SLAN


def model_to_dataframe(model: ImodModel, annotation: str = 'contour') -> pd.DataFrame:
    """Convert ImodModel model into a pandas DataFrame."""
    object_dfs: List[pd.DataFrame] = []
    if annotation == 'slicer_angles':
        if len(model.slicer_angles) == 0:
            raise ValueError("Model has no slicer angles.")
        for slicer_angle_idx, slicer_angle in enumerate(model.slicer_angles):
            slicer_angle_df = slicer_angle_to_dataframe(slicer_angle, slicer_angle_idx)
            object_dfs.append(slicer_angle_df)
    elif annotation == 'contour':
        for object_idx, object in enumerate(model.objects):
                for contour_idx, contour in enumerate(object.contours):
                    contour_df = contour_to_dataframe(contour, object_idx, contour_idx)
                    object_dfs.append(contour_df)
    else:
        raise ValueError(f"Unknown annotation type: {annotation}")
    return pd.concat(object_dfs)


def contour_to_dataframe(
    contour: Contour, object_id: int, contour_id: int
) -> pd.DataFrame:
    """Convert Contour model into a pandas DataFrame."""
    n_points = len(contour.points)
    contour_data = {
        "object_id": [object_id for _ in range(n_points)],
        "contour_id": [contour_id for _ in range(n_points)],
        "x": contour.points[:, 0],
        "y": contour.points[:, 1],
        "z": contour.points[:, 2],
    }
    return pd.DataFrame(contour_data)


def slicer_angle_to_dataframe(slicer_angle: SLAN, slicer_angle_id: int) -> pd.DataFrame:
    """Convert slicer angle model into a pandas DataFrame."""
    slicer_angle_data = {
        "slicer_angle_id": [slicer_angle_id],
        "time": [slicer_angle.time],
        "x_rot": [slicer_angle.angles[0]],
        "y_rot": [slicer_angle.angles[1]],
        "z_rot": [slicer_angle.angles[2]],
        "center_x": [slicer_angle.center[0]],
        "center_y": [slicer_angle.center[1]],
        "center_z": [slicer_angle.center[2]],
        "label": [slicer_angle.label],
    }
    return pd.DataFrame(slicer_angle_data)

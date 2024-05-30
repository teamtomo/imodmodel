from typing import List

import pandas as pd

from .models import Contour, ImodModel, SLAN


def model_to_dataframe(model: ImodModel) -> pd.DataFrame:
    """Convert ImodModel model into a pandas DataFrame."""
    object_dfs: List[pd.DataFrame] = []
    for object_idx, object in enumerate(model.objects):
        if hasattr(object, 'slans') and object.slans:
            for slan_idx, slan in enumerate(object.slans):
                slan_df = slan_to_dataframe(slan, object_idx, slan_idx)
                object_dfs.append(slan_df)
        else:
            for contour_idx, contour in enumerate(object.contours):
                contour_df = contour_to_dataframe(contour, object_idx, contour_idx)
                object_dfs.append(contour_df)
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


def slan_to_dataframe(slan: SLAN, object_id: int, slan_id: int) -> pd.DataFrame:
    """Convert SLAN model into a pandas DataFrame."""
    slan_data = {
        "object_id": [object_id],
        "slan_id": [slan_id],
        "time": [slan.time],
        "x_rot": [slan.angles[0]],
        "y_rot": [slan.angles[1]],
        "z_rot": [slan.angles[2]],
        "center_x": [slan.center[0]],
        "center_y": [slan.center[1]],
        "center_z": [slan.center[2]],
        "label": [slan.label],
    }
    return pd.DataFrame(slan_data)

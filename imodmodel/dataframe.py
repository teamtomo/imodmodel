from typing import List

import pandas as pd

from .models import Contour, ImodModel


def model_to_dataframe(model: ImodModel) -> pd.DataFrame:
    """Convert ImodModel model into a pandas DataFrame."""
    contour_dfs: List[pd.DataFrame] = []
    for object_idx, object in enumerate(model.objects):
        for contour_idx, contour in enumerate(object.contours):
            contour_df = contour_to_dataframe(contour, object_idx, contour_idx)
            contour_dfs.append(contour_df)
    return pd.concat(contour_dfs)


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

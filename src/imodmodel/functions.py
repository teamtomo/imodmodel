import os
import pandas as pd
from .models import ImodModel, ContourType
from .dataframe import model_to_dataframe


def read(filename: os.PathLike, annotation: str = 'contour') -> pd.DataFrame:
    """Read an IMOD model filename into a pandas DataFrame.

    Parameters
    ----------
    filename : filename to read
    annotation: which annotation of the model to return ['contour', 'slicer_angles'] (default: 'contour')
    """
    model = ImodModel.from_file(filename)
    return model_to_dataframe(model,annotation)

def write(dataframe: pd.DataFrame, filename: os.PathLike, type: ContourType=ContourType.SCATTERED) -> None:
    """Write a pandas DataFrame to an IMOD model file.

    Parameters
    ----------
    dataframe : pandas DataFrame to write
    filename : filename to write
    """
    model = ImodModel.from_dataframe(dataframe, type=type)
    model.to_file(filename)

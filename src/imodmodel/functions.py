"""Functional API for reading and writing IMOD model files."""

import os

import pandas as pd

from .dataframe import model_to_dataframe
from .models import ContourType, ImodModel


def read(filename: os.PathLike, annotation: str = "contour") -> pd.DataFrame:
    """Read an IMOD model filename into a pandas DataFrame.

    Parameters
    ----------
    filename : os.PathLike
        filename to read
    annotation : str
        which annotation of the model to return
        ['contour', 'slicer_angles'] (default: 'contour')
    """
    model = ImodModel.from_file(filename)
    return model_to_dataframe(model, annotation)


def write(
    dataframe: pd.DataFrame,
    filename: os.PathLike,
    type: ContourType = ContourType.SCATTERED,
) -> None:
    """Write a pandas DataFrame to an IMOD model file.

    Parameters
    ----------
    dataframe : pd.DataFrame
        pandas DataFrame to write
    filename : os.PathLike
        filename to write
    type : ContourType
        type of the contours to write (default: ContourType.SCATTERED)
    """
    model = ImodModel.from_dataframe(dataframe, type=type)
    model.to_file(filename)

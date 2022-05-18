import os
import pandas as pd

from .parser import ImodModelFileParser


def read(filename: os.PathLike) -> pd.DataFrame:
    """Read an IMOD model file into a pandas DataFrame.

    Parameters
    ----------
    filename : file to read
    """
    return ImodModelFileParser(filename).model.as_dataframe()

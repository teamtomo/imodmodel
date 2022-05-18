import os
import pandas as pd

from .parser import ImodModelFileParser


def read(filename: os.PathLike) -> pd.DataFrame:
    """Read an IMOD model file into a pandas DataFrame.

    Parameters
    ----------
    filename : file to read
    """
    parser = ImodModelFileParser(filename)
    parser.close_file()
    return parser.model.as_dataframe()

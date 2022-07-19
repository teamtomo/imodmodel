import os
import pandas as pd
from .data_structures import Model
from .utils import model_to_dataframe


def read(filename: os.PathLike) -> pd.DataFrame:
    """Read an IMOD model filename into a pandas DataFrame.

    Parameters
    ----------
    filename : filename to read
    """
    model = Model.from_file(filename)
    return model_to_dataframe(model)

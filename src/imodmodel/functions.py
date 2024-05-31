import os
import pandas as pd
from .models import ImodModel
from .dataframe import model_to_dataframe


def read(filename: os.PathLike, annotation: str = None) -> pd.DataFrame:
    """Read an IMOD model filename into a pandas DataFrame.

    Parameters
    ----------
    filename : filename to read
    annotation: can specify slicer angle annotations by setting annotation='slan' if annotation=None,
    contours are used instead.
    """
    model = ImodModel.from_file(filename)
    return model_to_dataframe(model,annotation)

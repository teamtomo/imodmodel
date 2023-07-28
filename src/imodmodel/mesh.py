from typing import List

import numpy as np

def parse_imod_indices(indices: np.ndarray) -> List[np.ndarray]:
    """ Turn an indices list as stored in imod models into a list of polygon indices arrays"""
    if indices[-1] != -1:
        raise ValueError(f'Mesh indices array must end with -1 but ends with {indices[-1]}')
    indices = indices[:-1]
    polygon_start_indices = np.nonzero((indices == -25))[0]
    split_indices = np.array_split(indices, polygon_start_indices)[1:] # first one is always empty
    # Validate: they should end with a -22
    for split in split_indices:
        if split[-1] != -22:
            raise ValueError(f"Invalid polygon indices end: {split[-1]}")
    # Cut of first and last value for each polygon (they should be -25 and -22 always)
    # and reshape 
    split_indices = [split[1:-1].reshape((-1, 3)) for split in split_indices]
    return split_indices


def cleanup_mesh(vertices: np.ndarray, indices: np.ndarray):
    unique_indices = np.unique(indices)
    new_indices = np.zeros_like(indices)
    for i in range(len(unique_indices)):
        new_indices += (indices == unique_indices[i]) * i
    new_vertices = vertices[unique_indices]
    return new_vertices, new_indices
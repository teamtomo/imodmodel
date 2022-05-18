import numpy as np

from .specification import header_spec, object_spec, contour_spec, imat_spec


class ImodDataStructure:
    def _initialise_from_specification(self, specification):
        for key in specification.keys():
            self.__setattr__(key, None)

    def add_data_from_dict(self, data):
        for key, value in data.items():
            self.__setattr__(key, value)


class Model(ImodDataStructure):
    def __init__(self):
        self.header = None
        self.objects = []

    def add_object(self, object):
        self.objects.append(object)

    def as_contour_dict(self):
        if len(self.objects) != 1:
            raise ValueError('only working for simple models containing one object')

        object = self.objects[0]
        data = {contour_idx: contour.pt for contour_idx, contour in enumerate(object.contours)}
        return data

    def as_contour_array(self):
        contour_data = self.as_contour_dict()
        n = sum([contour.shape[0] for contour in contour_data.values()])
        contour_array = np.empty((n, 4))

        row = 0
        for contour_idx, contour in contour_data.items():
            previous_row = row
            row += contour.shape[0]
            contour_array[previous_row:row, :3] = contour
            contour_array[previous_row:row, 3] = contour_idx

        return contour_array

    def as_dataframe(self):
        import pandas as pd
        columns = ['x', 'y', 'z', 'contour_idx']
        df = pd.DataFrame(self.as_contour_array(), columns=columns)
        return df


class Object(ImodDataStructure):
    def __init__(self):
        self._initialise_from_specification(object_spec)
        self.contours = []
        self.meshes = []
        self.imat = None

    def add_data(self, data):
        if isinstance(data, Contour):
            self._add_contour(data)
        elif isinstance(data, Mesh):
            self._add_mesh(data)
        elif isinstance(data, Imat):
            self.imat = Imat

    def _add_contour(self, contour):
        self.contours.append(contour)

    def _add_mesh(self, mesh):
        self.meshes.append(mesh)


class Header(ImodDataStructure):
    def __init__(self):
        self._initialise_from_specification(header_spec)


class Contour(ImodDataStructure):
    def __init__(self):
        self._initialise_from_specification(contour_spec)


class Mesh(ImodDataStructure):
    pass


class Imat(ImodDataStructure):
    def __init__(self):
        self._initialise_from_specification(imat_spec)

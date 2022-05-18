import os
from struct import Struct
from warnings import warn

import numpy as np

from .data_structures import Model, Header, Object, Contour, Imat
from .specification import id_spec, header_spec, object_spec, contour_spec, imat_spec


class ImodModelFileParser:
    def __init__(self, filename: os.PathLike):
        self.filename = filename
        self.file = None
        self.buffer = None
        self.control_sequence = None
        self.end_of_file_reached = False
        self.model = Model()
        self.parse_file()

    def parse_file(self):
        self.open_file()
        self.parse_id()
        self.parse_header()
        self.update_control_sequence()
        while self.control_sequence == 'OBJT':
            self.parse_object()
        self.close_file()

    def open_file(self):
        self.file = open(self.filename, 'rb')

    def parse_id(self):
        self.id = self.parse_from_constant_specification(id_spec)

    def parse_header(self):
        header = Header()
        header_data = self.parse_from_constant_specification(header_spec)
        header.add_data_from_dict(header_data)
        self.model.header = header

    def specification_from_control_sequence(self, control_sequence):
        return self._control_sequences[control_sequence]

    def parse_object(self):
        object = Object()

        # parse object header
        object_header_data = self.parse_from_constant_specification(object_spec)
        object.add_data_from_dict(object_header_data)

        # parse object data
        end_of_object = False
        while end_of_object is False:
            self.update_control_sequence()
            if self.control_sequence in ('OBJT', 'IEOF', 'EOF'):
                end_of_object = True
                continue
            self.update_object_from_control_sequence(object)

        # add object to model
        self.model.add_object(object)

    def parse_contour(self):
        contour = Contour()
        data_keys = list(contour_spec.keys())
        raw_format = self.format_from_specification(contour_spec)

        # read in number of points in contour
        contour.psize = int.from_bytes(self.read_from_buffer(4), byteorder='big')
        data_keys = data_keys[1:]

        # modify format specification string to account for number of points in contour
        n_floats = 3 * contour.psize
        format_str = f'>{raw_format[2:-2]}{n_floats}f'

        # unpack data as tuple
        raw_data = self.parse_from_format_str(format_str)

        # update contour with data
        for idx, key in enumerate(data_keys):
            if key == 'pt':
                contour.pt = np.array(raw_data[idx:]).reshape((-1, 3))
                continue
            contour.__setattr__(key, raw_data[idx])

        return contour

    def parse_imat(self):
        imat = Imat()
        imat_data = self.parse_from_constant_specification(imat_spec)
        imat.add_data_from_dict(imat_data)
        return imat

    def format_from_specification(self, specification: dict):
        return f">{''.join(specification.values())}"

    def parse_from_constant_specification(self, specification):
        format = self.format_from_specification(specification)
        data = self.parse_from_format_str(format)
        return {k: v for k, v in zip(specification.keys(), data)}

    def parse_from_format_str(self, format_str):
        struct = Struct(format_str)
        buffer = self.read_from_buffer(struct.size)
        data = struct.unpack(buffer)
        return data

    def read_from_buffer(self, n: int):
        return self.file.read(n)

    def close_file(self):
        self.file.close()

    @property
    def _parser_functions(self):
        parser_functions = {
            'CONT': self.parse_contour,
            'IMAT': self.parse_imat,
        }
        return parser_functions

    def update_control_sequence(self):
        try:
            self.control_sequence = self.read_from_buffer(4).decode('utf-8')
        except UnicodeDecodeError:
            self.control_sequence = None

    def update_object_from_control_sequence(self, object):
        parser_function = self._parser_functions.get(self.control_sequence)
        if parser_function:
            data = parser_function()
            object.add_data(data)
        else:
            warn(f'could not parse the control sequence {self.control_sequence}')

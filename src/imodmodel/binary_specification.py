"""Struct format strings for the IMOD binary model file format."""

from typing import ClassVar


class ModFileSpecification:
    """Binary specification, see https://bio3d.colorado.edu/imod/doc/binspec.html."""

    ID: ClassVar[dict[str, str]] = {"IMOD_file_id": "4s", "version_id": "4s"}
    MODEL_HEADER: ClassVar[dict[str, str]] = {
        "name": "128s",
        "xmax": "i",
        "ymax": "i",
        "zmax": "i",
        "objsize": "i",
        "flags": "I",
        "drawmode": "i",
        "mousemode": "i",
        "blacklevel": "i",
        "whitelevel": "i",
        "xoffset": "f",
        "yoffset": "f",
        "zoffset": "f",
        "xscale": "f",
        "yscale": "f",
        "zscale": "f",
        "object": "i",
        "contour": "i",
        "point": "i",
        "res": "i",
        "thresh": "i",
        "pixelsize": "f",
        "units": "i",
        "csum": "i",
        "alpha": "f",
        "beta": "f",
        "gamma": "f",
    }
    OBJECT_HEADER: ClassVar[dict[str, str]] = {
        "name": "64s",
        "extra_data": "16I",
        "contsize": "i",
        "flags": "I",
        "axis": "i",
        "drawmode": "i",
        "red": "f",
        "green": "f",
        "blue": "f",
        "pdrawsize": "i",
        "symbol": "B",
        "symsize": "B",
        "linewidth2": "B",
        "linewidth": "B",
        "linesty": "B",
        "symflags": "B",
        "sympad": "B",
        "trans": "B",
        "meshsize": "i",
        "surfsize": "i",
    }
    CONTOUR_HEADER: ClassVar[dict[str, str]] = {
        "psize": "i",
        "flags": "I",
        "time": "i",
        "surf": "i",
    }
    MESH_HEADER: ClassVar[dict[str, str]] = {
        "vsize": "i",
        "lsize": "i",
        "flags": "I",
        "time": "h",
        "surf": "h",
    }
    IMAT: ClassVar[dict[str, str]] = {
        "ambient": "B",
        "diffuse": "B",
        "specular": "B",
        "shininess": "B",
        "fillred": "B",
        "fillgreen": "B",
        "fillblue": "B",
        "quality": "B",
        "mat2": "I",
        "valblack": "B",
        "valwhite": "B",
        "matflags2": "B",
        "mat3b3": "B",
    }
    VIEW: ClassVar[dict[str, str]] = {
        "fovy": "f",
        "rad": "f",
        "aspect": "f",
        "cnear": "f",
        "cfar": "f",
        "rot": "3f",
        "trans": "3f",
        "scale": "3f",
        "mat": "16f",
        "world": "i",
        "label": "32c",
        "dcstart": "f",
        "dcend": "f",
        "lightx": "f",
        "lighty": "f",
        "plax": "f",
        "objvsize": "i",
        "bytesObjv": "i",
    }
    SLAN: ClassVar[dict[str, str]] = {
        "time": "i",
        "angles": "3f",
        "center": "3f",
        "label": "32s",
    }
    MINX: ClassVar[dict[str, str]] = {
        "oscale": "3f",
        "otrans": "3f",
        "orot": "3f",
        "cscale": "3f",
        "ctrans": "3f",
        "crot": "3f",
    }
    SIZE: ClassVar[dict[str, str]] = NotImplemented
    MESH: ClassVar[dict[str, str]] = NotImplemented
    LABL: ClassVar[dict[str, str]] = NotImplemented
    OLBL: ClassVar[dict[str, str]] = NotImplemented
    CLIP: ClassVar[dict[str, str]] = NotImplemented
    MCLP: ClassVar[dict[str, str]] = NotImplemented
    MEPA: ClassVar[dict[str, str]] = NotImplemented
    SKLI: ClassVar[dict[str, str]] = NotImplemented
    OGRP: ClassVar[dict[str, str]] = NotImplemented

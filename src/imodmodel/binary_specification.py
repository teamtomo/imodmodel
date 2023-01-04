class ModFileSpecification:
    """https://bio3d.colorado.edu/imod/doc/binspec.html"""
    ID = {
        'IMOD_file_id': '4s',
        'version_id': '4s'
    }
    MODEL_HEADER = {
        'name': '128s',
        'xmax': 'i',
        'ymax': 'i',
        'zmax': 'i',
        'objsize': 'i',
        'flags': 'I',
        'drawmode': 'i',
        'mousemode': 'i',
        'blacklevel': 'i',
        'whitelevel': 'i',
        'xoffset': 'f',
        'yoffset': 'f',
        'zoffset': 'f',
        'xscale': 'f',
        'yscale': 'f',
        'zscale': 'f',
        'object': 'i',
        'contour': 'i',
        'point': 'i',
        'res': 'i',
        'thresh': 'i',
        'pixelsize': 'f',
        'units': 'i',
        'csum': 'i',
        'alpha': 'f',
        'beta': 'f',
        'gamma': 'f',
    }
    OBJECT_HEADER = {
        'name': '64s',
        'extra_data': '16I',
        'contsize': 'i',
        'flags': 'I',
        'axis': 'i',
        'drawmode': 'i',
        'red': 'f',
        'green': 'f',
        'blue': 'f',
        'pdrawsize': 'i',
        'symbol': 'B',
        'symsize': 'B',
        'linewidth2': 'B',
        'linewidth': 'B',
        'linesty': 'B',
        'symflags': 'B',
        'sympad': 'B',
        'trans': 'B',
        'meshsize': 'i',
        'surfsize': 'i'
    }
    CONTOUR_HEADER = {
        'psize': 'i',
        'flags': 'I',
        'time': 'i',
        'surf': 'i',
    }
    IMAT = {
        'ambient': 'B',
        'diffuse': 'B',
        'specular': 'B',
        'shininess': 'B',
        'fillred': 'B',
        'fillgreen': 'B',
        'fillblue': 'B',
        'quality': 'B',
        'mat2': 'I',
        'valblack': 'B',
        'valwhite': 'B',
        'matflags2': 'B',
        'mat3b3': 'B'
    }

    VIEW = {
        'fovy': 'f',
        'rad': 'f',
        'aspect': 'f',
        'cnear': 'f',
        'cfar': 'f',
        'rot': '3f',
        'trans': '3f',
        'scale': '3f',
        'mat': '16f',
        'world': 'i',
        'label': '32c',
        'dcstart': 'f',
        'dcend': 'f',
        'lightx': 'f',
        'lighty': 'f',
        'plax': 'f',
        'objvsize': 'i',
        'bytesObjv': 'i'
    }
    SIZE = NotImplemented
    MESH = NotImplemented
    MINX = NotImplemented
    LABL = NotImplemented
    OLBL = NotImplemented
    CLIP = NotImplemented
    MCLP = NotImplemented
    MOST = NotImplemented
    OBST = NotImplemented
    COST = NotImplemented
    MEST = NotImplemented
    SLAN = NotImplemented
    MEPA = NotImplemented
    SKLI = NotImplemented
    OGRP = NotImplemented

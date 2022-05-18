id_spec = {
    'IMOD_file_id': '4s',
    'version_id': '4s'
}

header_spec = {
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

object_spec = {
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

contour_spec = {
    'psize': 'i',
    'flags': 'I',
    'time': 'i',
    'surf': 'i',
    'pt': '3f'
}

imat_spec = {
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

size_spec = {
    'sizes': 'f'
}

view_spec = {
    'fovy' : 'f',
    'rad' : 'f',
    'aspect' : 'f',
    'cnear' : 'f',
    'cfar' : 'f',
    'rot' : '3f',
    'trans' : '3f',
    'scale' : '3f',
    'mat' : '16f',
    'world' : 'i',
    'label' : '32c',
    'dcstart' : 'f',
    'dcend' : 'f',
    'lightx' : 'f',
    'lighty' : 'f',
    'plax' : 'f',
    'objvsize' : 'i',
    'bytesObjv' : 'i'
}

mesh_spec = NotImplemented
minx_spec = NotImplemented
labl_spec = NotImplemented
olbl_spec = NotImplemented
clip_spec = NotImplemented
mclp_spec = NotImplemented
most_spec = NotImplemented
obst_spec = NotImplemented
cost_spec = NotImplemented
mest_spec = NotImplemented
slan_spec = NotImplemented
mepa_spec = NotImplemented
skli_spec = NotImplemented
ogrp_spec = NotImplemented

control_sequences = {
    'OBJT': object_spec,
    'CONT': contour_spec,
    'MESH': mesh_spec,
    'MINX': minx_spec,
    'LABL': labl_spec,
    'OLBL': olbl_spec,
    'CLIP': clip_spec,
    'MCLP': mclp_spec,
    'IMAT': imat_spec,
    'SIZE': size_spec,
    'VIEW': view_spec,
    'MOST': most_spec,
    'OBST': obst_spec,
    'COST': cost_spec,
    'MEST': mest_spec,
    'SLAN': slan_spec,
    'MEPA': mepa_spec,
    'SKLI': skli_spec,
    'OGRP': ogrp_spec
}

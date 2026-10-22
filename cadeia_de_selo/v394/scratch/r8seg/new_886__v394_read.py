def _v394_read(a):
    a = _v394_matrix(a, "reading input")
    g = _v394_geometry()
    return g['Pplus'] @ a @ g['Pplus'] + g['Pminus'] @ a @ g['Pminus']
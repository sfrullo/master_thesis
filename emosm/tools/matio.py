# conding: utf-8

import os
import os.path as path

from scipy.io import loadmat

PYRESEMBLANCE_MAT_DIR = path.join(path.dirname(__file__), "../pyresemblance/mat")

def load_mat_file(filename, field=None):
    try:
        print path.join(PYRESEMBLANCE_MAT_DIR, filename)
        data = loadmat(path.join(PYRESEMBLANCE_MAT_DIR, filename))
        if field is None:
        	field = path.basename(filename.split('.mat')[0])
        return data[field]
    except Exception as e:
        return []

import os
import os.path as path

from scipy.io import loadmat

PYRESEMBLANCE_MAT_DIR = path.join(path.dirname(__file__), "pyresemblance/mat")

def load_gradient_mat(filename):
    try:
    	print path.join(PYRESEMBLANCE_MAT_DIR, "gradient", filename)
        data = loadmat(path.join(PYRESEMBLANCE_MAT_DIR, "gradient", filename))
        return data[filename.split('.mat')[0]]
    except Exception as e:
        return []

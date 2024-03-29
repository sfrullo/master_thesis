# coding: utf-8

import numpy as np

from emosm.tools import matio

test_threedlark_kernel_fspecial_disk_1 = np.array([
    [[0.002345658856671, 0.078786685906930, 0.002345658856671],
    [0.078786685906930, 1.000000000000000, 0.078786685906930],
    [0.002345658856671, 0.078786685906930, 0.002345658856671]],

    [[0.016426554551363, 0.208494041376074, 0.016426554551363],
    [0.208494041376074, 1.000000000000000, 0.208494041376074],
    [0.016426554551363, 0.208494041376074, 0.016426554551363]],

    [[0.002345658856671, 0.078786685906930, 0.002345658856671],
    [0.078786685906930, 1.000000000000000, 0.078786685906930],
    [0.002345658856671, 0.078786685906930, 0.002345658856671]]
])


test_edge_mirror_3 = [

    {
        "input" : np.array([
            [[1,3], [2,4]],
            [[5,7], [6,8]]
        ]),

        "expected_result" : np.array([
            [[8,6,8,6], [7,5,7,5], [8,6,8,6], [7,5,7,5]],
            [[4,2,4,2], [3,1,3,1], [4,2,4,2], [3,1,3,1]],
            [[8,6,8,6], [7,5,7,5], [8,6,8,6], [7,5,7,5]],
            [[4,2,4,2], [3,1,3,1], [4,2,4,2], [3,1,3,1]]
        ])
    },

]


test_get_gradient = [

    {
        "input" : matio.load_mat_file("person01_boxing_d2_uncomp_64_64_40.mat"),
        "expected_result" : [ matio.load_mat_file("gradient/" + z + ".mat") for z in ["zx","zy","zt"] ],
    }
]
# coding: utf-8

# native

# external
import numpy as np
import matplotlib.pyplot as plt

from biosppy.signals.tools import windower

# feature extractors that take into account the asynchrony of physiological signal response
# based on:
# Courtemanche, François & Dufresne, Aude & L. LeMoyne, Elise. (2014).
# Multiresolution Feature Extraction During Psychophysiological Inference: Addressing Signals Asynchronicity.

LATENCY_DURATION_MAP = {

    "mean" : {
        "function" : np.mean,
        "signals" :{
            "ECG" : {
                "arousal" : (0, 1000),
                "valence" : (4750, 1000)
            },
            "EDA" : {
                "arousal" : (7000, 2750),
                "valence" : (0, 1000)
            },
            "Resp" : {
                "arousal" : (3000, 1000),
                "valence" : (0, 1000)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
    "std" : {
        "function" : np.std,
        "signals" :{
            "ECG" : {
                "arousal" : (0, 5750),
                "valence" : (0, 1000)
            },
            "EDA" : {
                "arousal" : (3500, 2000),
                "valence" : (0, 1000)
            },
            "Resp" : {
                "arousal" : (750, 1000),
                "valence" : (0, 1000)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
    "min" : {
        "function" : np.min,
        "signals" :{
            "ECG" : {
                "arousal" : (1000, 1250),
                "valence" : (3000, 2750)
            },
            "EDA" : {
                "arousal" : (7000, 2250),
                "valence" : (0, 1000)
            },
            "Resp" : {
                "arousal" : (1750, 1750),
                "valence" : (0, 1000)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
    "max" : {
        "function" : np.max,
        "signals" :{
            "ECG" : {
                "arousal" : (0, 5750),
                "valence" : (6250, 1250)
            },
            "EDA" : {
                "arousal" : (5500, 4250),
                "valence" : (0, 1000)
            },
            "Resp" : {
                "arousal" : (3500, 1250),
                "valence" : (6500, 5000)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
    "mean_diff" : {
        "function" : lambda x: np.mean(np.diff(x)),
        "signals" :{
            "ECG" : {
                "arousal" : (3000, 1250),
                "valence" : (2750, 2750)
            },
            "EDA" : {
                "arousal" : (3250, 2000),
                "valence" : (6500, 5500)
            },
            "Resp" : {
                "arousal" : (0, 1000),
                "valence" : (5750, 1000)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
    "mean_abs_diff" : {
        "function" : lambda x: np.mean(np.abs(np.diff(x))),
        "signals" :{
            "ECG" : {
                "arousal" : (750, 4250),
                "valence" : (0, 1000)
            },
            "EDA" : {
                "arousal" : (3750, 1500),
                "valence" : (0, 1000)
            },
            "Resp" : {
                "arousal" : (750, 1000),
                "valence" : (750, 1500)
            },
            "SKT" : {
                "arousal" : (0, 1000),
                "valence" : (0, 1000)
            }
        }
    },
}

def extract(data, sigtype, attribute="mean", psyco_construct="arousal", fps=24):

    if psyco_construct not in ["valence", "arousal"]:
        raise ValueError("Request a valid psycological construct: [valence, arousal]")

    latency, duration = LATENCY_DURATION_MAP[attribute]["signals"][sigtype][psyco_construct]
    function = LATENCY_DURATION_MAP[attribute]["function"]

    latency = int( fps * latency / 1000 )
    duration = int( fps * duration / 1000 )

    w_size = int(latency + duration)

    f = lambda d: function(d[latency:])

    index, features = windower(data, size=w_size, step=1, fcn=f)

    return index, features

def extract_physiological_feature(data, opts):
    # compute features for each session

    if not isinstance(data, list):
        data = [data]

    sigtype = opts["sigtype"]
    attribute = opts["attribute"]
    psyco_construct = opts["psyco_construct"]
    fps = opts["fps"]

    max_sample = opts.get("max_sample")

    features = []
    for d in data:
        signal = d.get_data(preprocess=True, new_fps=fps)
        index, f = extract(signal, sigtype=sigtype, attribute=attribute, psyco_construct=psyco_construct, fps=fps)
        if max_sample is not None:
            f = f[:max_sample]
        features.append(f)

    features = np.vstack(features)

    return features.T
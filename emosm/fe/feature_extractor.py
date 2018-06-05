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
			"EDA" : {
				"arousal" : (7000, 2750),
				"valence" : (0, 1000)
			},
			"Resp" : {
				"arousal" : (3000, 1000),
				"valence" : (0, 1000)
			}
		}
	},
	"std" : {
		"function" : np.std,
		"signals" :{
			"EDA" : {
				"arousal" : (3500, 2000),
				"valence" : (0, 1000)
			},
			"Resp" : {
				"arousal" : (750, 1000),
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

	print data

	print w_size

	f = lambda d: function(d[latency:])

	index, features = windower(data, size=w_size, step=1, fcn=f)

	return index, features
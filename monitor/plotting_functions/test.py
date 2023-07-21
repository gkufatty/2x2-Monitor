import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm, colors
import matplotlib.patches as mpatches
import numpy as np
import awkward as ak
import h5py
import argparse
from matplotlib.backends.backend_pdf import PdfPages

class TestPlot(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            plt.figure(fig.number)
            plt.close()
            fig = None
            
            # do stuff to make new plot
        fig = plt.figure(dpi=100, figsize=(6,18))

        packets = fh['packets']

        plt.hist(packets['timestamp'],bins=100)
        plt.xlabel('timestamp')
   
        return fig




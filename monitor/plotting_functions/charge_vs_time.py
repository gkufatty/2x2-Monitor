import matplotlib.pyplot as plt
import numpy as np

class chargetime(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            # do stuff to update plot
            pass
        else:
            # do stuff to make new plot
            packets=fh['packets']
            for iogroup in range(1,9,1):
              iogroup_mask=(packets['io_group']==iogroup) & data_packet_mask
              plt.hist(packets['timestamp'][iogroup_mask]%SPILL_PERIOD,weights=packets['dataword'][iogroup_mask],bins=200,label='io_group '+str(iogroup),alpha=0.5)
            plt.xlabel('timestamp%spill_period')
            plt.ylabel('charge [ADC]')
            plt.legend(ncol=4,bbox_to_anchor=(-0.05,1.00),loc='lower left')

      
        return fig

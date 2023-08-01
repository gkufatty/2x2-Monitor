import matplotlib.pyplot as plt
import numpy as np

class ChargePerTime(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            plt.figure(fig.number)
            plt.close()
            fig = None
            
        # do stuff to make new plot
        fig = plt.figure(dpi=100, figsize=(10,6))
        SPILL_PERIOD = 1.2e7
        packets=fh['packets']
        data_packet_mask = packets['packet_type']==0
        for iogroup in range(1,9,1):
            iogroup_mask=(packets['io_group']==iogroup) & data_packet_mask
            plt.hist(packets['timestamp'][iogroup_mask]%SPILL_PERIOD,weights=packets['dataword'][iogroup_mask],bins=200,label='io_group '+str(iogroup),alpha=0.5)
        plt.xlabel('timestamp%spill_period')
        plt.ylabel('charge [ADC]')
        plt.legend(ncol=4,bbox_to_anchor=(-0.05,1.00),loc='lower left')
        
        return fig

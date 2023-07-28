import matplotlib.pyplot as plt
import numpy as np

class timestamp(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            # do stuff to update plot
            pass
        else:
            # do stuff to make new plot
            packets=fh['packets']
            packet_index=np.array(list(range(0,len(packets))))
            data_packet_mask = packets['packet_type']==0
            trig_packet_mask = packets['packet_type']==4
            sync_packet_mask = packets['packet_type']==7
            rollover_packet_mask=(packets['packet_type']==6) & (packets['trigger_type'] == 83)
            other_packet_mask= ~(data_packet_mask | trig_packet_mask | sync_packet_mask | rollover_packet_mask)
            fig,axes = plt.subplots(2,2,dpi=100,figsize=(10,8))
            axes[0,0].plot(packets['timestamp'][data_packet_mask],packet_index[data_packet_mask],'o',label='data packets', linestyle='None')
            axes[0,0].plot(packets['timestamp'][trig_packet_mask],packet_index[trig_packet_mask],'o',label='trigger packets',linestyle='None')
            axes[0,0].plot(packets['timestamp'][sync_packet_mask],packet_index[sync_packet_mask],'o',label='sync packet',linestyle='None')
            axes[0,0].plot(packets['timestamp'][rollover_packet_mask],packet_index[rollover_packet_mask],'o',label='rolloever packet',linestyle='None')
            axes[0,0].plot(packets['timestamp'][other_packet_mask],packet_index[other_packet_mask],'o',label='other',linestyle='None')
            axes[1,0].hist(packets['timestamp'],bins=100)
            axes[0,1].plot(packets['receipt_timestamp'][data_packet_mask],packet_index[data_packet_mask],'o',label='data packets', linestyle='None')
            axes[0,1].plot(packets['receipt_timestamp'][trig_packet_mask],packet_index[trig_packet_mask],'o',label='trigger packets',linestyle='None')
            axes[0,1].plot(packets['receipt_timestamp'][sync_packet_mask],packet_index[sync_packet_mask],'o',label='sync packet',linestyle='None')
            axes[0,1].plot(packets['receipt_timestamp'][rollover_packet_mask],packet_index[rollover_packet_mask],'o',label='rolloever packet',linestyle='None') 
            axes[0,1].plot(packets['receipt_timestamp'][other_packet_mask],packet_index[other_packet_mask],'o',label='other',linestyle='None')
            axes[0,1].legend()
            axes[1,1].hist(packets['receipt_timestamp'], bins=100)
            axes[0,0].legend()
            axes[0,0].set_ylabel('packet index')
            axes[1,0].set(xlabel='timestamp')
            axes[1,1].set(xlabel='receipt timestamp')
            fig.suptitle('Time structure of packets')

        return fig

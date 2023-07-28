import matplotlib.pyplot as plt

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
            fig = plt.figure(dpi=100)
            plt.plot(packets['timestamp'][data_packet_mask],packet_index[data_packet_mask],'o',label='data packets', linestyle='None')
            plt.plot(packets['timestamp'][trig_packet_mask],packet_index[trig_packet_mask],'o',label='trigger packets',linestyle='None')
            plt.plot(packets['timestamp'][sync_packet_mask],packet_index[sync_packet_mask],'o',label='sync packet',linestyle='None')
            plt.plot(packets['timestamp'][rollover_packet_mask],packet_index[rollover_packet_mask],'o',label='rolloever packet',linestyle='None')
            plt.plot(packets['timestamp'][other_packet_mask],packet_index[other_packet_mask],'o',label='other',linestyle='None')
            plt.xlabel('timestamp')
            plt.ylabel('packet index')
            plt.legend()
        return fig

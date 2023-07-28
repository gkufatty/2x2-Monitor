import matplotlib.pyplot as plt

class timestamp(object):
  
  packets=sim_h5['packets']
  packet_index=np.array(list(range(0,len(packets))))
  data_packet_mask = packets['packet_type']==0
  trig_packet_mask = packets['packet_type']==4
  sync_packet_mask = packets['packet_type']==7
  rollover_packet_mask=(packets['packet_type']==6) & (packets['trigger_type'] == 83)
  other_packet_mask= ~(data_packet_mask | trig_packet_mask | sync_packet_mask | rollover_packet_mask)
  
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            # do stuff to update plot
            pass
        else:
            # do stuff to make new plo
            fig = plt.figure(dpi=100, figsize=(6,18))
            packets = fh['packets']
            plt.hist(packets['timestamp'],bins=100)
            plt.xlabel('timestamp')
        return fig

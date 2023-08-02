import matplotlib.pyplot as plt
import numpy as np

class IndexVSTimestamp(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            plt.figure(fig.number)
            plt.close()
            fig = None
            
        # do stuff to make new plot
        fig = plt.figure(dpi=100, figsize=(10,6))
        SPILL_PERIOD = 1.2e7
        packets=fh['packets']
        light_trig = fh['light_trig']
        data_packet_mask = packets['packet_type'] == 0
        trig_packet_mask = packets['packet_type'] == 7
      
        tstamp_trig0 = packets['timestamp'][data_packet_mask]
        tstamp_trig7 = packets['timestamp'][trig_packet_mask]
      
        ## IDENTIFY THE INDEX WHERE THE TURNOVER OCCURS
        try:
            charge_cutoff = np.where(tstamp_trig0 > 1.999**31)[0][-1]
            light_cutoff = np.where(tstamp_trig7 > 1.999**31)[0][-1]
            wvfm_cutoff = np.where(light_trig['ts_sync'] > 1.999**31)[0][-1]
            tstamp_real_trig0 = np.concatenate((tstamp_trig0[:(charge_cutoff+1)],((2**31)+tstamp_trig0[(charge_cutoff+1):])))
            tstamp_real_trig7 = np.concatenate((tstamp_trig7[:(light_cutoff+1)],((2**31)+tstamp_trig7[(light_cutoff+1):])))
            l_tsync_real = np.concatenate((light_trig['ts_sync'][:(wvfm_cutoff+1)],((2**31)+light_trig['ts_sync'][(wvfm_cutoff+1):])))
        except: 
            tstamp_real_trig0 = tstamp_trig0
            tstamp_real_trig7 = tstamp_trig7
            l_tsync_real = light_trig['ts_sync']
        ## DEFINE SPILLID (EVENTID) FOR PACKETS AND LIGHT
        light_spillIDs = (np.rint(l_tsync_real/SPILL_PERIOD)).astype(int)
        packet0_spillIDs = (np.rint(tstamp_real_trig0/SPILL_PERIOD)).astype(int)
        packet7_spillIDs = (np.rint(tstamp_real_trig7/SPILL_PERIOD)).astype(int)
        list_spillIDs = np.unique(light_spillIDs)
        ## DEFINE THE INDICES OF EACH TIMESTAMP
        indices = np.arange(0,len(packets['timestamp']),1)
        indices_0 = indices[data_packet_mask]
        indices_7 = indices[trig_packet_mask]
        ## PLOT
        bins = np.linspace(min(packet7_spillIDs),max(packet7_spillIDs),392)
        bin_width = bins[2] - bins[1]
        counts, bins = np.histogram(np.array(light_spillIDs), bins=bins)
        plt.hist(bins[:-1], bins, weights=counts, color='tomato', label='Light: '+str(len(light_trig['ts_sync']))+' triggers')
        counts, bins = np.histogram(np.array(packet7_spillIDs), bins=bins)
        plt.hist(bins[:-1], bins, weights=counts, histtype="step", color='dodgerblue', label='Pacman: '+str(len(packet7_spillIDs))+' triggers')
        plt.title('Triggers Per Spill ('+str(len(list_spillIDs))+' Spills)\n', fontsize=16)
        plt.xlabel('Spill', fontsize=14)
        plt.ylabel('Triggers', fontsize=14)
        plt.ylim(0,max(counts)+2)
        plt.grid(axis='y', color='0.85')
        plt.legend(loc='upper left', fontsize=14)
        
        return fig

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
        ## PLOT INDICE VS. TIMESTAMP
        fig = plt.figure(figsize=(18,6))
        plt.plot(tstamp_real_trig0,indices_0, "o", color='dodgerblue', label='larpix')
        plt.plot(tstamp_real_trig7,indices_7,".", color='tomato', label='light')
        plt.axvline(x=(2**31), label='LArPix Clock Rollover')
        plt.title('Larpix (Spill) Trigger vs. Light Trigger\n', fontsize=18)
        plt.xlabel(r'Timestamp [0.01$\mu$s]', fontsize=14)
        plt.ylabel('Packet Index', fontsize=16)
        plt.legend(fontsize=16)    
        
        return fig

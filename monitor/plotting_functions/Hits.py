import matplotlib.pyplot as plt
import numpy as np

class HitsHistogram(object):
    def __call__(self, filename, fh, fig=None):
        if fig is not None:
            plt.figure(fig.number)
            plt.close()
            fig = None
            
        # do stuff to make new plot
        fig = plt.figure(dpi=100, figsize=(10,6))
        tracks = fh['tracks']
        packets=fh['packets']
 
        def get_eventIDs(event_packets, mc_packets_assn):    
          event_IDs = []
          eventID = tracks['eventID'] # eventIDs associated to each track
          track_id_assn = mc_packets_assn['track_ids'] # track indices corresponding to each packet

            # Loop over each packet
          for ip, packet in enumerate(event_packets):
            if packet['packet_type'] != 0:
              continue
            packet_track_ids = track_id_assn[ip]
            packet_track_ids = packet_track_ids[packet_track_ids != -1]
            packet_event_IDs = eventID[packet_track_ids]
            unique_packet_event_ID = np.unique(packet_event_IDs)
            assert(len(unique_packet_event_ID == 1))
            packet_event_ID = unique_packet_event_ID[0]              
            event_IDs.append(packet_event_ID)
          return np.array(event_IDs)

        mc_packets_assn = fh['mc_packets_assn']
        event_IDs = get_eventIDs(packets, mc_packets_assn)
        unique_event_IDs, hit_counts = np.unique(event_IDs, return_counts = True)
        plt.hist(hit_counts, bins = 50)
        plt.title("Pixels hit per event")
        plt.xlabel("Pixels")
        plt.ylabel("Counts")
        
        return fig

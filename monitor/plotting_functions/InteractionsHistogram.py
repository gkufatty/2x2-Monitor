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
        genie_hdr=fh['genie_hdr']
        n_vertices=np.zeros(genie_hdr['eventID'].max())
        for i in range(len(n_vertices)):    
            n_vertices[i]=np.count_nonzero(genie_hdr['eventID']==i)
        plt.hist(n_vertices,bins=np.arange(-0.5, n_vertices.max()+1.5,1))
        plt.title('Total interactions per spill')
        plt.xlabel('Interactions')
        plt.ylabel('Counts')
        
        return fig

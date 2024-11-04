import tsmd.competitors.competitors_tools.locomotif_original_tools as loctools
import numpy as np

class LocoMotif:

    def __init__(self, min_wlen, max_wlen, rho=0.8,  n_patterns=None, start_mask=None, end_mask=None, overlap=0, warping=True):
        self.rho=rho
        self.l_min=min_wlen
        self.l_max=max_wlen
        self.nb=n_patterns
        self.start_mask=start_mask
        self.end_mask=end_mask
        self.overlap=overlap
        self.warping=warping

    def fit(self,signal):
        self.signal=signal
        self.n=self.signal.shape[0]
        self.motif_sets=loctools.apply_locomotif(signal,self.rho,self.l_min,self.l_max,self.nb,self.start_mask,self.end_mask,self.overlap,self.warping)

    @property
    def prediction_mask_(self):
        nb_motifs=len(self.motif_sets)
        mask=np.zeros((nb_motifs,self.n))
        for i in range(nb_motifs):
            for occurence_s,occurence_e in self.motif_sets[i]:
                mask[i,occurence_s:occurence_e]=1
        return mask
        
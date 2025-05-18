import numpy as np

# import tsmd.competitors.competitors_tools.motiflets_tools as ml
import tsmd.competitors.competitors_tools.motiflets_w_numba_tools as ml


class Motiflets:
    """k-Motiflets algorithm for motif discovery.

    Parameters
    ----------
    k_max : int 
        Maximum number of occurrences of a single motif.
    min_wlen : int
        Minimium window length.
    max_wlen : int 
        Maximum window length.
    elbow_deviation : float, optional (default=1.0)
        The minimal absolute deviation needed to detect an elbow.
        It measures the absolute change in deviation from k to k+1.
        1.05 corresponds to 5% increase in deviation.
    slack : float, optional (default=0.5)
        Defines an exclusion zone around each subsequence to avoid trivial matches.
        Defined as percentage of m. E.g. 0.5 is equal to half the window length.
    
    Attributes
    ----------
    prediction_mask_ : np.ndarray of shape (n_patterns, n_samples)
        Binary mask indicating the presence of motifs across the signal.  
        Each row corresponds to one discovered motif, and each column to a time step.  
        A value of 1 means the motif is present at that time step, and 0 means it is not.
        """

    def __init__(
            self,
            k_max,
            min_wlen,
            max_wlen,
            elbow_deviation=1.00,
            slack=0.5,
    ):
        self.elbow_deviation = elbow_deviation
        self.slack = slack

        self.motif_length_range = np.int32(
            np.arange(
                min_wlen,
                max_wlen + 1,
                (max_wlen+1-min_wlen) / 3
            )
        )
        self.motif_length = 0

        self.k_true = k_max

        # k_max has to be set to at least k_max + 2 to find an elbow at k_max
        self.k_max = k_max + 2

    def fit(self, signal):
        """Fit Motiflets
        
        Parameters
        ----------
        signal : numpy array of shape (n_samples, )
            The input samples (time series length).
        
        Returns
        -------
        self : object
            Fitted estimator.
        """
        self.signal = signal
        self.fit_motif_length()
        # self.fit_k_elbow()

    def fit_motif_length(
            self,
            subsample=1
    ):
        """Computes the AU_EF plot to extract the best motif lengths

            This is the method to find and plot the characteristic motif-lengths, for k in
            [2...k_max], using the area AU-EF plot.

            Details are given within the paper 5.2 Learning Motif Length l.

            Parameters
            ----------
            k_max: int
                use [2...k_max] to compute the elbow plot.
            motif_length_range: array-like
                the interval of lengths

            Returns
            -------
            best_motif_length: int
                The motif length that maximizes the AU-EF.

            """
        self.motif_length, au_ef_minima, au_efs, elbows, top_motiflets, dists \
            = ml.find_au_ef_motif_length(
            self.signal,
            self.k_max,
            self.motif_length_range,
            exclusion=None,
            elbow_deviation=self.elbow_deviation,
            slack=self.slack,
            subsample=subsample)

        motiflets = []
        for i in range(len(top_motiflets)):
            motiflets.append(top_motiflets[i][np.append(elbows[i], [self.k_true])])
            ## motiflets.append(top_motiflets[i][elbows[i]])
        self.motiflets = motiflets
        self.motif_lengths = self.motif_length_range

        return self.motif_length

    @property
    def prediction_mask_(self) -> np.ndarray:
        n_motifs = np.sum([len(self.motiflets[i]) for i in range(len(self.motiflets))])

        pos = 0
        mask = np.zeros((n_motifs, self.signal.shape[0]))
        for i in range(len(self.motiflets)):
            motif_length = self.motif_lengths[i]
            for motif_starts in self.motiflets[i]:
                for j in range(len(motif_starts)):
                    mask[pos, motif_starts[j]:motif_starts[j] + motif_length] = 1
                pos += 1
        return mask

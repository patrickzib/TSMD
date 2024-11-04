
import numpy as np

import warnings
warnings.filterwarnings('ignore')

class LatentMotif(object): 
    
    def __init__(self,n_patterns:int,wlen:int,radius:float,alpha = 1.0,learning_rate =0.1,n_iterations = 100, n_starts = 1, verbose = False) -> None:
        """Initialization

        Args:
            n_patterns (int): number of patterns
            wlen (int): window length 
            radius (float): cluster radius
            alpha (float, optional): regularization parameter. Defaults to 1.0.
            learning_rate (float, optional): learning rate. Defaults to 0.1.
            n_iterations (int, optional): number of gradient iteration. Defaults to 100.
            n_strats (int, optional): number of trials. Defaults to 10.
            verbose (bool, optional): verbose. Defaults to False.
        """
        self.n_patterns = n_patterns
        self.wlen = wlen
        self.radius = radius
        self.alpha = alpha
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.n_starts = n_starts
        self.verbose = verbose

    def _freq(self, patterns:np.ndarray)->float: #verified
        """Frequence score

        Args:
            patterns (np.ndarray): patterns, shape(n_patterns, wlen)

        Returns:
            float: frequence score
        """
        dist = np.sum((self.set_[:,np.newaxis,:] - patterns[np.newaxis,...])**2,axis=2)
        exp_dist = np.exp(-self.alpha/self.radius * dist)
        freq = 1/(self.n_patterns * self.set_size_) * np.sum(exp_dist)
        return freq

    def _pen(self, patterns): #verified 
        """penalty score

        Args:
            patterns (np.ndarray): patterns, shape(n_patterns, wlen)

        Returns:
            float: penalty score
        """
        if self.n_patterns>1:
            dist = np.sum((patterns[:,np.newaxis,:] - patterns[np.newaxis,...])**2,axis=2)
            pen_m = np.where(dist < 2*self.radius, (1 - dist/(2*self.radius))**2, 0)
            pen = 2/(self.n_patterns*(self.n_patterns -1))*np.sum(np.triu(pen_m,k=1))
        else: 
            pen = 0
        return pen  

    def _score(self,patterns): #verified
        """Score

        Args:
            patterns (np.ndarray): patterns, shape(n_patterns, wlen)

        Returns:
            float: Score
        """
        return self._freq(patterns) - self._pen(patterns)


    def _freq_derivative(self, patterns): 
        """Frequence deriavative

        Args:
            patterns (np.ndarray): patterns, shape(n_patterns, wlen)

        Returns:
            float: frequence derivative
        """
        diff = self.set_[:,np.newaxis,:] - patterns[np.newaxis,...]
        exp_dist = np.exp(-self.alpha/self.radius * np.sum(diff**2,axis=2))
        div_freq = -2 * self.alpha / (self.n_patterns * self.set_size_ * self.radius) * np.sum(exp_dist[...,np.newaxis]*diff, axis=0)
        return div_freq

    def _pen_derivative(self, patterns): 
        """Frequence derivative

        Args:
            patterns (np.ndarray): patterns, shape(n_patterns, wlen)

        Returns:
            float: frequence derivative
        """
        diff = patterns[:,np.newaxis,:] - patterns[np.newaxis,...]
        dist = np.sum(diff**2, axis =2)
        pen_m = np.where(dist < 2*self.radius, 2* self.radius - dist, 0)
        div_pen = -2 / (self.radius**2 * self.n_patterns * (self.n_patterns - 1)) * np.sum(pen_m[...,np.newaxis]*diff,axis=0)
        return div_pen
        

    def fit(self,signal:np.ndarray)->None:
        """Fit

        Args:
            signal (np.ndarray): signal, shape: (L,)
        """

        #initialization 
        self.signal_ = signal
        self.set_ = np.lib.stride_tricks.sliding_window_view(signal,self.wlen)
        self.set_ = (self.set_-np.mean(self.set_,axis=1).reshape(-1,1))/np.std(self.set_,axis=1).reshape(-1,1)
        self.set_size_ = self.set_.shape[0]
        self.score_ = -np.inf
        self.patterns_ = np.zeros((self.n_patterns,self.wlen))

        if self.verbose: 
            print("Start Trials")
        for i in range(self.n_starts): 
            patterns, score = self.one_fit_()
            if self.verbose:
                print(f"Trial: {i+1}/{self.n_starts}, score : {score}")
            if score > self.score_: 
                self.score_ = score
                self.patterns_ = patterns

        if self.verbose: 
            print(f"Successfully finished, best score: {self.score_}")

        return self
    
    def one_fit_(self):
        """One learning trial

        Returns:
            np.ndarray, float: patterns, score
        """

        patterns = np.random.randn(self.n_patterns, self.wlen)
        rate_adapt = np.zeros((self.n_patterns, self.wlen))

        for i in range(self.n_iterations): 
            if self.n_patterns>1:
                div = self._freq_derivative(patterns) - self._pen_derivative(patterns)
            else: 
                div = self._freq_derivative(patterns)
            rate_adapt += div**2
            patterns -= self.learning_rate/np.sqrt(rate_adapt) * div

            if self.verbose: 
                print(f"Iteration: {i+1}/{self.n_iterations}, score: {self._score(patterns)} ")

        score = self._score(patterns)
        return patterns, score

    @property
    def prediction_mask_(self)->np.ndarray: 
        """Create prediction mask

        Returns:
            np.ndarray: prediction mask, shape (n_patterns, L-wlen+1)
        """
        dist = np.sum((self.set_[:,np.newaxis,:] - self.patterns_[np.newaxis,...])**2,axis=2)
        idx_lsts = []
        for line in dist.T: 
            idxs = np.arange(self.set_size_-self.wlen+1)
            idx_lst = []
            t_distance = np.min(line)
            while t_distance < self.radius:
                try: 
                    #local next neighbor
                    t_idx = np.argmin(line)
                    idx_lst.append(idxs[t_idx])
                    t_distance = line[t_idx]

                    #remove window
                    remove_idx = np.arange(max(0,t_idx-self.wlen+1),min(len(line),t_idx+self.wlen))
                    idxs = np.delete(idxs,remove_idx)
                    line = np.delete(line,remove_idx)

                except: 
                    break
            idx_lsts.append(idx_lst)

        mask = np.zeros((self.n_patterns,self.signal_.shape[0]))
        for i,p_idx in enumerate(idx_lsts):
            for idx in p_idx:
                mask[i,idx:idx+self.wlen] =1 
        
        #remove null lines
        mask=mask[~np.all(mask == 0, axis=1)]

        return mask
import numpy as np
from joblib import Parallel,delayed
import tsmd.tools.distance as distance
import itertools as it 


import warnings
warnings.filterwarnings('ignore')

class Baseline(object): 

    def __init__(self,n_patterns:int,radius:int,wlen:int,distance_name:str,distance_params = dict(),n_jobs = 1) -> None:
        """KNN initialization

        Args:
            n_neighbors (int): Number of neighbors
            wlen (int): Window length
            distance_name (str): name of the distance
            distance_params (_type_, optional): additional distance parameters. Defaults to dict().
            n_jobs (int, optional): number of processes. Defaults to 1.
        """
        self.n_patterns = n_patterns
        self.radius = radius
        self.wlen = wlen
        self.distance_name = distance_name
        self.distance_params = distance_params
        self.n_jobs = n_jobs


    def _search_neighbors(self,idx:int,line:np.ndarray)-> tuple: 
        """Find index and distance value of the non overlapping nearest neighbors under a radius.

        Args:
            idx (int): index of the considerded line in the crossdistance matrix
            line (np.ndarray): line of the crossdistance matrix. shape: (n_sample,)

        Returns:
            tuple: neighbor index np.ndarray, neighbor distance np.ndarray
        """

        #initilization
        neighbors = []
        dists = []
        idxs = np.arange(line.shape[0])
        remove_idx = np.arange(max(0,idx-self.wlen+1),min(line.shape[0],idx+self.wlen))
        line[remove_idx] = np.inf
        #idxs = np.delete(idxs,remove_idx)
        #line = np.delete(line,remove_idx)

        #search loop
        t_distance = np.min(line)
        while t_distance < self.radius:
            #local next neighbor
            t_idx = np.argmin(line)
            t_distance = line[t_idx]
            if line[t_idx] < self.radius:
                neighbors.append(idxs[t_idx])
                dists.append(line[t_idx])
                #remove window
                remove_idx = np.arange(max(0,t_idx-self.wlen+1),min(len(line),t_idx+self.wlen))
                line[remove_idx] = np.inf
                #idxs = np.delete(idxs,remove_idx)
                #line = np.delete(line,remove_idx)

            
        return neighbors,dists
    
    def _elementary_neighborhood(self,start:int,end:int)->tuple:
        """Find elementary neighborhood of a chunk of successive lines of the crossdistance matrix

        Args:
            start (int): chunk start
            end (int): chunck end

        Returns:
            tuple: neighborhood count, neighborhood std
        """
        #initialization
        neighbors =[]
        dists = []
        line = self.distance_.first_line(start)
        t_neighbors,t_dists = self._search_neighbors(start,line)
        neighbors.append(t_neighbors)
        dists.append(t_dists)
        
        #main loop
        for i in range(start+1,end): 
            line = self.distance_.next_line()
            t_neighbors,t_dists = self._search_neighbors(i,line)
            neighbors.append(t_neighbors)
            dists.append(t_dists)
        return neighbors,dists

    def neighborhood_(self)->None: 

        #divide the signal accordingly to the number of jobs
        set_idxs = np.linspace(0,self.mdim_,self.n_jobs+1,dtype=int)
        set_idxs = np.vstack((set_idxs[:-1],set_idxs[1:])).T

        # set the parrallel computation
        results = Parallel(n_jobs=self.n_jobs, prefer="processes")(
            delayed(self._elementary_neighborhood)(*set_idx)for set_idx in set_idxs
        )

        idxs,dists = list(zip(*results))
        self.idxs_ = list(it.chain(*idxs))
        self.dists_ = list(it.chain(*dists))
        return self

    def find_patterns_(self): 

        self.counts_ = np.array([len(lst) for lst in self.idxs_])
        stds = []
        stds = []
        for lst in self.dists_: 
            if len(lst)>0: 
                stds.append(np.std(lst))
            else: 
                stds.append(np.inf)
        self.stds_ = np.array(stds)
        self.sort_idx_ = np.lexsort((self.stds_,-self.counts_))
        patterns = [self.sort_idx_[0]]

        for idx in self.sort_idx_[1:]: 
            if len(patterns) <self.n_patterns: 
                dist_to_patten = np.array([self.distance_.individual_distance(idx,p_idx) for p_idx in patterns])
                if np.all(dist_to_patten > 2*self.radius): 
                    patterns.append(idx)
            else: 
                break

        self.patterns_ = patterns

    def fit(self,signal:np.ndarray)->None:
        """Compute the best patterns

        Args:
            signal (np.ndarray): Univariate time-series, shape: (L,)
        """
        
        #initialisation
        self.signal_ = signal
        self.mdim_ = len(signal)-self.wlen+1 
        self.distance_ = getattr(distance,self.distance_name)(self.wlen,**self.distance_params)
        self.distance_.fit(signal)

        #Compute neighborhood
        self.neighborhood_()
        #find patterns
        self.find_patterns_()

        return self

    @property
    def prediction_mask_(self)->np.ndarray:
        """Create prediction mask

        Returns:
            np.ndarray: prediction mask, shape (n_patterns, L-wlen+1)
        """
        mask = np.zeros((self.n_patterns,self.signal_.shape[0]))
        for i,p_idx in enumerate(self.patterns_):
            mask[i,p_idx:p_idx+self.wlen] =1
            for idx in self.idxs_[p_idx]:
                mask[i,idx:idx+self.wlen] =1 
        #remove null lines
        mask=mask[~np.all(mask == 0, axis=1)]
        return mask
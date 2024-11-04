import numpy as np
from joblib import Parallel,delayed
import tsmd.tools.distance as distance
from functools import partial


import warnings
warnings.filterwarnings('ignore')

class PanMatrixProfile(object): 

    def __init__(self,n_patterns:int,min_wlen:int,max_wlen:int,distance_name:str,distance_params = dict(),radius_ratio = 3,normalized=False,n_jobs = 1) -> None:
        """Initialization

        Args:
            n_patterns (int): Number of neighbors
            min_wlen (int): Minimum window length
            max_wlen (int): Maximum window length
            distance_name (str): name of the distance
            distance_params (_type_, optional): additional distance parameters. Defaults to dict().
            radius_ratio (float): radius as a ratio of min_dist. 
            n_jobs (int, optional): number of processes. Defaults to 1.
        """
        self.n_patterns = n_patterns
        self.radius_ratio = radius_ratio
        self.min_wlen = min_wlen
        self.max_wlen = max_wlen
        self.distance_name = distance_name
        self.distance_params = distance_params
        self.normalized = normalized
        self.n_jobs = n_jobs

    def _search_neighbors(self,wlen_idx:int,seed_idx:int,line:np.ndarray)-> tuple: 
        """Find index and distance value of the non overlapping nearest neighbors under a radius.

        Args:
            wlen_idx (int): index of the window length and associated profile
            seed_idx (int): index of the considerded line in the crossdistance matrix
            line (np.ndarray): line of the crossdistance matrix. shape: (n_sample,)

        Returns:
            tuple: neighbor index np.ndarray, neighbor distance np.ndarray
        """

        #initilization
        neighbors = []
        dists = []
        idxs = np.arange(self.mdims_[wlen_idx])
        remove_idx = np.arange(max(0,seed_idx-self.wlens_[wlen_idx]+1),min(self.mdims_[wlen_idx],seed_idx+self.wlens_[wlen_idx]))
        idxs = np.delete(idxs,remove_idx)
        line = np.delete(line,remove_idx)

        #search loop
        radius = np.min(line)*self.radius_ratio
        t_distance = np.min(line)
        while t_distance < radius:
            try: 
                #local next neighbor
                t_idx = np.argmin(line)
                if line[t_idx] == np.inf:
                    break
                neighbors.append(idxs[t_idx])
                dists.append(line[t_idx])

                #remove window
                remove_idx = np.arange(max(0,t_idx-self.wlens_[wlen_idx]+1),min(len(line),t_idx+self.wlens_[wlen_idx]))
                idxs = np.delete(idxs,remove_idx)
                line = np.delete(line,remove_idx)

                t_distance = dists[-1]
            except: 
                break
            
        return neighbors,dists

    def _elementary_profile(self,idx:int,start:int,end:int)->tuple:
        """Find elementary profile of a chunk of successive lines of the crossdistance matrix

        Args:
            start (int): chunk start
            end (int): chunck end

        Returns:
            tuple: neighborhood count, neighborhood std
        """
        #initialization
        neighbors =[]
        dists = []
        line = self.distance_[idx].first_line(start)
        mask = np.arange(max(0,start-self.wlens_[idx]+1), min(self.mdims_[idx],start+self.wlens_[idx]))
        line[mask] = np.inf
        t_idx = np.argmin(line)
        t_dist = line[t_idx]
        neighbors.append(t_idx)
        dists.append(t_dist)
        
        #main loop
        for i in range(start+1,end): 
            line = self.distance_[idx].next_line()
            mask = np.arange(max(0,i-self.wlens_[idx]+1), min(self.mdims_[idx],i+self.wlens_[idx]))
            line[mask] = np.inf
            t_idx = np.argmin(line)
            t_dist = line[t_idx]
            neighbors.append(t_idx)
            dists.append(t_dist)
        return neighbors,dists

    def profile_(self,idx:int)->np.ndarray: 
        """Compute profile of wlen

        Args:
            idx (int): window length index

        Returns:
            np.ndarray: profile, nearest neighbor index
        """

        #divide the signal accordingly to the number of jobs
        set_idxs = np.linspace(0,self.mdims_[idx],self.n_jobs+1,dtype=int)
        set_idxs = np.vstack((set_idxs[:-1],set_idxs[1:])).T

        # set the parrallel computation
        results = Parallel(n_jobs=self.n_jobs, prefer="processes")(
            delayed(partial(self._elementary_profile,idx))(*set_idx)for set_idx in set_idxs
        )

        idxs,dists = list(zip(*results))

        return np.hstack(dists),np.hstack(idxs)

    def _temporary_mask(self,wlen_idx:int,mask:list,patterns:list)->list: 
        """Create mask associated with the current research windows

        Args:
            wlen_idx (int): window length index
            mask (list): current mask
            patterns (list): list of patterns already detected

        Returns:
            list: mask for the search of neighbors
        """
        t_mask = mask.copy()
        for _, p_idxs in patterns: 
            for p_idx in p_idxs: 
                t_mask += np.arange(max(0,p_idx-self.wlens_[wlen_idx]+1),p_idx+1).astype(int).tolist()
        t_mask = np.array(t_mask)
        keep_idx = np.where(t_mask<=self.mdims_[wlen_idx])
        return t_mask[keep_idx].tolist()

    def find_patterns_(self): 
        profiles = self.profiles_.copy()
        mask = []
        patterns = []

        for iteration in np.arange(self.n_patterns): 
            if iteration == 0: 
                min_idx = np.argmin(profiles)
                wlen_idx, seed_idx = np.unravel_index(min_idx,profiles.shape)
                line = self.distance_[wlen_idx].first_line(seed_idx)
            else: 
                overlapping = True
                while overlapping and not np.all(profiles == np.inf): 
                    min_idx = np.argmin(profiles)
                    wlen_idx, seed_idx = np.unravel_index(min_idx,profiles.shape)
                    t_mask = self._temporary_mask(wlen_idx,mask,patterns)
                    if seed_idx not in t_mask: 
                        overlapping = False
                    else: 
                        profiles[:,seed_idx] = np.inf
                if not overlapping:
                    line = self.distance_[wlen_idx].first_line(seed_idx)
                    line[t_mask] = np.inf

            if np.all(profiles == np.inf):
                break
            
            p_idxs,dists = self._search_neighbors(wlen_idx,seed_idx,line)
            p_idxs = np.hstack((np.array([seed_idx]),p_idxs))
            patterns.append((self.wlens_[wlen_idx],p_idxs))
            mask += np.hstack([np.arange(max(0, idx - self.min_wlen +1),min(self.mdims_[wlen_idx],idx+self.wlens_[wlen_idx])) for idx in p_idxs]).astype(int).tolist()
            profiles[:,mask] = np.inf

        self.test_ = profiles
        
        self.patterns_ = patterns

    def fit(self,signal:np.ndarray)->None:
        """Compute the best patterns

        Args:
            signal (np.ndarray): Univariate time-series, shape: (L,)
        """
        
        #initialisation
        self.signal_ = signal
        self.profiles_ = []
        self.idxs_ = []
        self.distance_ = []
        self.wlens_ = np.arange(self.min_wlen,self.max_wlen+1)
        self.mdims_ = signal.shape[0] - self.wlens_ + 1
        for i,wlen in enumerate(self.wlens_):
            self.distance_.append(getattr(distance,self.distance_name)(self.wlens_[i],**self.distance_params))
            self.distance_[i].fit(signal)

            #Compute profile and idxs
            profile,idxs = self.profile_(i)
            gap = self.wlens_[i] - self.min_wlen
            if gap>0: 
                gap_profile = np.full(gap,np.inf)
                gap_idxs = np.full(gap,np.nan)
                profile = np.hstack((profile,gap_profile))
                idxs = np.hstack((idxs,gap_idxs))
            self.profiles_.append(profile)
            self.idxs_.append(idxs)
        
        self.profiles_ = np.array(self.profiles_)
        self.idxs_ = np.array(self.idxs_)

        if self.normalized: 
            self.profiles_ = self.profiles_ / np.sqrt(self.wlens_).reshape(-1,1)

        #find patterns
        self.find_patterns_()

        return self

    @property
    def prediction_mask_(self):
        mask = np.zeros((self.n_patterns,self.signal_.shape[0]))
        for i,(wlen,p_idxs) in enumerate(self.patterns_):
            for idx in p_idxs:
                mask[i,int(idx):int(idx+wlen)] =1 
        #remove null lines
        mask=mask[~np.all(mask == 0, axis=1)]
        return mask
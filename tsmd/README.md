# Motif Discovery Methods

In order to address the research questions enumerated in the previous section, we have to carefully select algorithms  from different families to best represent the diversity of Motif Discovery techniques. In total, we selected 11 Motif Discovery algorithms.

The following motivations drive our selection of Motif Discovery methods: 
1. Our collection of methods should have at least one representative from each of the main families of methods we presented earlier. 
2. Priority is given to methods that have represented a great advance in the field.
3. Our collection should contain recent approaches tackling a large panel of challenges.
4. We finally favor algorithms for which implementation was proposed, or the code description was detailed enough.

These criteria led us to choose the following methods: 

### SetFinder 

This algorithm finds the K-motif sets directly, based on a counting and separating principle. In practice, each subsequence is compared to every other, and the non-overlapping matches  are counted. Then, each subsequence with a non-zero count is checked to ensure that its distance to another subsequence with a larger number of matches is greater than a given threshold.

### LatentMotif 

This method addresses a variant of the K-Motifs problem as a constrained optimization task, where the center of the motif is learned (the center doesn't need to be a subsequence of $S$ but can belong to any element in $\mathbb{R}^n$). The initial objective and constraint functions are regularized to enable gradient ascent. The learned subsequences are then returned as the centers of the motif sets. To identify all occurrences of each motif set, a complete scan of the time series subsequences is conducted. Non-overlapping subsequences within a distance $R$ of the learned center are considered occurrences of the motif set.


### STOMP
The STOMP algorithm is a similarity-based method and proposes a fast computation of the Matrix Profile by efficiently leveraging the Fast Fourier Transform (FFT). Once the  Matrix Profile is computed, the center of the Motif Set is defined as the subsequence with the minimum distance to another non-overlapping subsequence. A full scan of the time-series subsequences is performed, and non-overlapping subsequences that are at a distance of less than $R$ from the center are identified as occurrences of the corresponding Motif set.

### PanMP 

PanMP aims to generalize the Matrix Profile approach to detect patterns at varying time scales without requiring prior knowledge of the Motif size. To achieve this, the PanMatrixProfile—a matrix that contains Matrix Profiles for a range of window lengths in a time series—is computed. Based on distance and regardless of window size, the best non-overlapping Motif Pairs are then iteratively selected. The Motif sets are constructed from these selected Motif Pairs in the same way as in STOMP. Note that if the range of window sizes is restricted to a single value, this method functions identically to STOMP.

### VALMOD 

VALMOD has a similar goal to PanMP but employs a slightly different approach. It leverages pruning techniques to compute the Matrix Profile over a range of window lengths, $\ell$. Motif Pairs are iteratively selected based on distance normalized by the square root of the window length. Motif sets are then built from these top Motif Pairs by identifying non-overlapping subsequences within a distance $< R$ from one of the two centers. 

### $k$-Motiflets 

Unlike most other algorithms in our benchmark that require the user to set a radius parameter $R$, the k-Motiflets method aims to discover motifs without needing this parameter. Instead, the user specifies the desired number of occurrences $k$ for the target motif. With $k$ defined, the method identifies the set of $k$ non-overlapping subsequences with minimal extent, where extent is the maximum pairwise distance among elements in the set.


### PEPA

This method extracts the motifs through three computational steps: (i) the time series is transformed into a graph with nodes representing subsequences and edges weighted by the distance between subsequences; (ii) persistent homology is applied to detect significant clusters of nodes, isolating them from nodes that correspond to irrelevant parts of the time series; and (iii) a post-processing step merges temporally adjacent subsequences within each cluster to form variable length motif sets. Note also that this method utilizes the LT-Normalized Euclidean distance, a distance measure invariant to linear trends.

### A-PEPA 

A variant of PEPA that does not require the user to define the exact number of motif sets and estimates it automatically.

### Grammarviz 

Grammarviz uses grammar induction methods for motif detection. In practice, the time series is discretized using SAX, and grammar induction techniques, such as Sequitur or RE-PAIR, are applied to the discretized series to identify grammar rules. The most frequent and representative grammar rules are selected, and occurrences of the various motifs are then extracted.

### MDL-Clust

The MDL-CLust method claims to perform clustering of subsequences. However, since clustering time series subsequences is generally ineffective, the authors propose disregarding data that does not fit into any cluster and avoiding overlapping subsequences. Thus, the output of MDL-CLust can be fully interpreted as motif sets. 
More specifically, the method utilizes the MDL principle to form clusters. In each iteration, we can either create a new cluster (by selecting the first two members using a classic PairMotif algorithm), add a subsequence to an existing cluster, or merge two clusters. We select the operation that most effectively reduces the description length. The algorithm terminates when no usable data remains or further reduction in the time series description length is no longer possible.

### LoCoMotif 

The LoCoMotif method addresses the challenge of variable length by searching for time-warped motifs at potentially different time scales within a time series. The process begins with the LoCo step, where the Self-Similarity Matrix of the time series is utilized to construct paths based on a principle similar to Dynamic Time Warping (DTW). The paths with the highest accumulated similarity in this matrix are identified. In the second step, these subpaths are grouped to create candidate Motifs. The method then assesses the encoding capacity of these candidates using a quality score that combines the similarity between occurrences with the overall coverage of the Motif set.

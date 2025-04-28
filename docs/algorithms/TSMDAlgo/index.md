# Motif Discovery Algorithms in TSMD

In order to address the research questions enumerated in the previous section, we have to carefully select algorithms from different families to best represent the diversity of Motif Discovery techniques. In total, we selected 11 Motif Discovery algorithms.

The following motivations drive our selection of Motif Discovery methods: 
1. Our collection of methods should have at least one representative from each of the main families of methods we presented earlier. 
2. Priority is given to methods that have represented a great advance in the field.
3. Our collection should contain recent approaches tackling a large panel of challenges.
4. We finally favor algorithms for which implementation was proposed, or the code description was detailed enough.

These criteria led us to choose the following methods: 

| Methods               | family | Parameters | Complexity (Worst Case) |
|-----------------|----------------------------|----------------------------------------|--------------------------------------------------------|
| SetFinder       |  Frequency                 | $K,w,R$                                | $O(n^3)$                                               |
| LatentMotif     |  Frequency                 | $K,w,R$                                | $O(wn)$                                                |
| STOMP           |  Similarity                | $K,w,r$                                | $O(n^2)$                                               |
| VALMOD          |  Similarity                | $K,w_{\min},w_{\max},r$                | $O((w_{\max} - w_{\min})n^2)$                          |
| PanMP           |  Similarity                | $K, w_{\min},w_{\max}, r$              | $O((w_{\max} - w_{\min})n^2)$                          |
| $k$-Motiflets   |  Similarity                | $k_{\max},w_{\min},w_{\max}$           | $O(k_{\max}n^2 + nk_{\max}^2)$                         |
| PEPA            |  Similarity                | $w_{\min},K$                           | $O(Kn^2)$                                              |
| A-PEPA          |  Similarity                | $w_{\min}$                             | $O(Kn^2)$                                              |
| GrammarViz      |  Encoding                  | $K,w$                                  | $O(wn^2)$                                              |
| MDL-Clust       |  Encoding                  | $w_{\min}, w_{\max}$                   | $O(n^3/w_{min} + (w_{max} - w_{min})n^2 )^*$           |
| LoCoMotif       |  Encoding                  | $K,w_{\min},w_{\max}$                  | $O(n^2\frac{w_{\max} - w_{\min}}{w_{\min}})$           |

We describe each algorithm in the sections below and provide code snippets on how to use them. In all the following sections, we a synthetic time series as an example. The latter is generated as follows:

```python
from tsmd.tools.synthetic_signal import SignalGenerator

generator=SignalGenerator(n_motifs=2, motif_length=200, motif_amplitude=3, motif_fundamental=3, sparsity=0.5, sparsity_fluctuation=0.5)
signal,labels= generator.generate()
generator.plot()
```
![Synthetic signal](../../../assets/methodExample/signal_example.png "Synthetic signal")




```{toctree}
:maxdepth: 2


Frequency
Similarity
Encoding

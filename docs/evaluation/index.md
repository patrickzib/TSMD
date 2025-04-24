# Experimental Evaluation

## Parameters Settings 

The methods share several commons parameters. These parameters are complex to set in practice and can strongly impact performances.In order to perform a fair comparison between all methods in our benchmarks, we set the values of these parameters to their optimal values (based on the exact characteristics of the time series in our benchmark). Overall,the
parameters are the following: 

- **The number of patterns $K$ :** We set this parameter to the exact number of patterns in the time series.
- **The maximum number of occurences $k_{\max} :$** We set this parameter to the maximum number
of occurrences of all Motifs.
- **The radius $R$ :** This parameter has to be estimated for real time series. In practice, for all the occurences of a motif (the set of occurences is noted $M$), we compute $R_k = \max_{S_i,S_j\in M} \text{dist}(S_i,S_j)/2$. We use $\bar{R}=\frac{1}{K}\sum_{i=1}^KR_K$ as the radius parameter.
- **The radius ratio $r$ :** We take $r=3$ as the default value. 
- **Window length $w_{\text{len}}$ :** We take the average length of occurences of all motifs.
- **Minimum/Maximum length ($w_{\text{min}}/w_{\text{max}}$) :** We set this parameters to the minimum and maximum length of all occurences of all motifs.

## Evaluation Measures

We evaluate performance with range based-precision, recall and f1-score metrics. We procede to an optimal pairing between predicted and true motifs thanks to the Hungarian matching algorithm. Then, the precision, recall, and f1-score computation rely on the optimal pairings and a threshold $\tau \in [0,1]$ that controls the overlapping ratio Any metric’s score is the average of the individual metric score between paired motif sets; the averaging can be macro or weighted. For precision(resp.recall), a motif occurrence is counted as a true positive if the ratio between the overlap length and the predicted(resp.real) occurrence length is greater than the threshold $\tau$. In our case this threshold is set to 50%.

## Research Questions 

The results of our experimental evaluation are summarized here. For more details, see the paper.

```{toctree}
:maxdepth: 3

RQ1
RQ2
RQ3
RQ4
RQ5
RQ6
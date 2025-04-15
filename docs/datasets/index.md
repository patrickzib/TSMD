# Datasets in TSMD

## Download the datasets

You can download the datasets [here](https://kiwi.cmla.ens-cachan.fr/index.php/s/MwbqcKBdp2ZGzTx).

## Datasets statistics

Overall, our benchmark considers both real time series collection and a synthetic generator to evaluate specific parameters and characteristics. In total, we have the following datasets: 

| Dataset                 | # TS | TS len. | # motifs | # motifs per TS  | ratio motif | avg. Motif len. | intra Motif len. (std) | inter Motif len.(std) |
|-------------------------|------|---------|----------|------------------|-------------|-----------------|------------------------|------------------------|
| arm-CODA                | 64   | 8,050   | 7        | 5                | 0.65        | 520             | 22                     | 88         |
| mitdb                   | 100  | 20,000  | 10       | 1.6              | 0.99        | 281             | 36                     | 10         |
| mitdb1                  | 100  | 20,000  | 1        | 1                | 0.98        | 320             | 12                     | 0          |
| ptt-ppg                 | 100  | 20,000  | 1        | 1                | 0.98        | 324             | 15                     | 0          |
| REFIT                   | 100  | 210,870 | 3        | 2.2              | 0.08        | 410             | 13                     | 34         |
| SIGN                    | 50   | 172,780 | 3        | 3                | 0.10        | 74              | 34                     | 3          |
| JIGSAWMaster            | 23   | 10,300  | 8        | 3.8              | 0.66        | 156             | 38                     | 66         |
| JIGSAWSlave             | 32   | 10,160  | 9        | 3.9              | 0.65        | 146             | 35                     | 60         |

```{toctree}
:maxdepth: 2

JIGSAW
MITDB
MITDB1
PTT-PPG
REFIT
SIGN
armCODA
SyntheticGenerator

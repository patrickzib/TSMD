# Time series Data for Motif Discovery

## Real labeled time series datasets

You can download the datasets here: TBD

### arm-CODA 

It is a dataset of 240 multivariate time series collected using 34 Cartesian Optoelectronic Dynamic Anthropometers (CODA) placed on the upper limbs of 16 healthy subjects, each of whom performed 15 predefined movements. Each sensor records its position in 3D space. To construct the dataset, we kept the left forearm sensor of ID 29 and 5 of the predefined movements. The occurrences of the five movements were randomly placed along the time axis for each subject, sensor, and dimension. Gaussian noise with a signal-to-noise ratio of 0.01 is added to all time series. This resulted in a dataset of 64 univariate time series.

### mitdb1 

The MIT-BIH Arrhythmia Database contains 48 half-hour recordings of two-channel ambulatory electrocardiograms (ECGs) sampled at 360Hz. Cardiologists annotated the heartbeats according to 19 categories. We divide all recordings into a time series of 1 minute and keep only the first channel. We selected time series of healthy subjects that contains only normal heartbeats and randomly selected 100 time series.

### mitdb: 

We randomly selected 100 one-minute time series from the MIT-BIH dataset (healthy subjects or not). Each time series has 1 to 4 motifs (normal heartbeats and different types of arrhythmia), each with several occurrences.

### ptt-ppg 

Pule-Transit-Time photoplethysmogram (PPG) dataset consists of time series recorded with multiple sensors (sampled at 500Hz) from healthy subjects performing physical activities. The annotated motifs are heartbeats. We randomly select 100 40-second-long signals from the first channel of the PPG during the “run” activity.

### REFIT: 

This dataset provides aggregate and individual appliance load curves at 8-second sampling intervals from 20 houses. We selected 10 houses and aggregated recordings of the appliances available: dishwasher, washing machine, and tumble dryer. The recordings were down-sampled to 32-second intervals and divided into time series of one week. We kept 10 time series for each house in which the appliances were not used simultaneously. It resulted in a 100 univariate time series dataset with a maximum of 3 different motifs.

### SIGN: 

This dataset is built from samples of Auslan (Australian Sign Language) signs. 95 signs were collected from five signers, totaling 6650 sign samples. Based on this, we generate a long time series by injecting several words (concatenation of signs). The different injected signs are the motifs. Every word is separated with flat sequences (i.e., without any motifs). In total, we generate 50 different time series.

### JIGSAW 

The time series of this dataset are recorded from the DaVinci Surgical System. Each time series contains 76 dimensions. Each dimension corresponds to a sensor
(with an acquisition rate of 30 Hz). The sensors are divided into two groups: patient-side manipulators (**JIGSAWSlave**), and master tool manipulators (**JIGSAWMaster**). The recorded time series corresponds to surgeons performing a suture that can be decomposed into 11 gestures. Each gesture corresponds to a motif that can be repeated multiple times within the same time series. Overall, we selected 23 time series (from different sensors) for JIGSAWMaster and 32 time series for JIGSAWSlave.

## Synthetic generator

This section presents the synthetic time series generator used to perform the experiments.

For a given number of motifs $K$, the generator constructs one representative per motif. Given an average length $l_i$, and a fundamental frequency (set to 4Hz in our case), a motif representative is generated as the sum of the sine function of the $l_i$ first harmonics, with the phases and the amplitudes uniformly sampled over $[−\pi, \pi]$ and $[−1, 1]$. The $k_i$ occurrences of motif $i$ are then constructed by temporally distorting the initial representative. In practice, we use a parameter called \textit{length fluctuation} defined as the maximum variability of the occurrence's length to the average length. For example, a ratio of 0.1 means that we resample the occurrences of the motif so they have lengths varying up to $\pm 10 \%$ from the average length. The occurrences of all motifs are then randomly concatenated and spaced according to sparsity parameters. Finally, white Gaussian noise of standard deviation $\sigma$, and a random walk (to model local linear trends) are added to the signal.

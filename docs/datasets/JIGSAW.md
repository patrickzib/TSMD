# JIGSAW

The time series of this dataset [Gao et al. 2014] are recorded from the DaVinci Surgical System. Each time series contains 76 dimensions. Each dimension corresponds to a sensor
(with an acquisition rate of 30 Hz). The sensors are divided into two groups: patient-side manipulators (**JIGSAWSlave**), and master tool manipulators (**JIGSAWMaster**). The recorded time series corresponds to surgeons performing a suture that can be decomposed into 11 gestures. Each gesture corresponds to a motif that can be repeated multiple times within the same time series. Overall, we selected 23 time series (from different sensors) for JIGSAWMaster and 32 time series for JIGSAWSlave.



## Example of Time series

### JIGSAW Slave (snippet)

![JIGSAW (Slave) Example](../../assets/tsExample/JIGSAWSlave.png "JIGSAW (Slave) Example")

### JIGSAW Master (snippet)

![JIGSAW (Master) Example](../../assets/tsExample/JIGSAWMaster.png "JIGSAW (Master) Example")

## Meta-data summary

### JIGSAW Slave

- number of motifs: 9
- mean number of motifs per time series: 3.9
- min number of motifs per time series: 3
- max number of motifs per time series: 5

### JIGSAW Master

- number of motifs: 8
- mean number of motifs per time series: 3.9
- min number of motifs per time series: 3
- max number of motifs per time series: 4


## Reference

[Gao et al. 2014] Yixin Gao, S. Vedula, Carol E. Reiley, N. Ahmidi, B. Varadarajan, Henry C. Lin, L. Tao, L. Zappella, B. Béjar, D. Yuh, C. C. Chen, R. Vidal, S. Khudanpur, and Gregory Hager. 2014. JHU-ISI Gesture and Skill Assessment Working Set (JIGSAWS) : A Surgical Activity Dataset for Human Motion Modeling

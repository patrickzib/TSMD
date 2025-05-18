import os
import time

initial_path=os.getcwd()
dataset_list=['mitdb']
# 'arm-CODA','mitdb','mitdb1','ptt-ppg','REFIT','SIGNRoll','JIGSAWSMaster','JIGSAWSSlave'
os.chdir(initial_path+'/../..')
import experiments.benchmark_experiment as exp
from tsmd.competitors.motiflets import Motiflets
data_paths_list= ['/Users/bzcschae/workspace/TSMD/data/processed_data/'+ dataset + '/' for dataset in dataset_list]
results_paths_list = ['/Users/bzcschae/workspace/TSMD/results/RQ1/' + dataset + '/' for dataset in dataset_list]
os.chdir(initial_path)

start = time.time()
algorithms=[Motiflets]
for data_path,results_path in zip(data_paths_list,results_paths_list):
    exp1=exp.Experiment(algorithms)
    exp1.run_experiment(data_path,results_path=results_path)
    break

end = time.time()
print(f"Elapsed time: {end - start} seconds")
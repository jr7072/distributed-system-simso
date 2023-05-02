from simso.configuration import Configuration
from simso.configuration.HPCConfig import HPCConfiguration
from simso.configuration.ClusterConfiguration import ClusterConfig
from simso.core.Task import TaskInfo
from simso.core.HPC import HPC
from SimPy.Simulation import Simulation
from simso.generator.task_generator import gen_periods_uniform
import sys
import time

def generate_hpc_config(num_clusters, cluster_size, cores, cycles_per_ms=2100000, partition_algorithm="worst_fit"):

    high_performance_computer_config = HPCConfiguration(name="HPC1")
    high_performance_computer_config.partition_algorithm = partition_algorithm
    high_performance_computer_config.cycles_per_ms = cycles_per_ms

    global_node_index = 0
    for cluster_index in range(num_clusters):

        cluster_config = ClusterConfig(cluster_name=f"Cluster {cluster_index}")

        for _ in range(cluster_size):

            new_node = Configuration(node_name=f"Node {global_node_index}", cluster=cluster_config.cluster_name)

            new_node.name = f"Node {global_node_index}"
            new_node.scheduler_info.clas = "simso.schedulers.EDF" # global edf scheduler for each node

            for core_index in range(cores):

                new_node.add_processor(name=f"Core {core_index}", identifier=core_index)

            cluster_config.add_node(new_node)
            global_node_index += 1
        
        high_performance_computer_config.add_cluster(cluster_config)

    return high_performance_computer_config

def generate_tasks(hpc_config, num_tasks, num_task_set):

    task_metadata = gen_periods_uniform(num_tasks, num_task_set, 1000, 1000)


    for task_index, task_data in enumerate(task_metadata[0]):

        period = task_data
        deadline = 1000

        hpc_config.add_task(name=f"task {task_index}", identifier=task_index,
                                task_type='Cluster', period=period, deadline=deadline, wcet=300)

    return hpc_config

if __name__ == '__main__':

    num_clusters = int(sys.argv[1])
    cluster_size = int(sys.argv[2])
    cores = int(sys.argv[3])
    partition_algorithm = sys.argv[4]
    num_tasks = int(sys.argv[5])

    print('TIME', 'EVENT', 'TASK', 'CLUSTER', 'NODE', 'CORE')
    
    configuration = generate_hpc_config(num_clusters, cluster_size, cores,
                                            partition_algorithm=partition_algorithm)

    sim = Simulation()

    generate_tasks(configuration, num_tasks, 1)
    
    high_performance_computer = HPC(configuration, sim)
    sim.initialize()

    sim.activate(high_performance_computer, high_performance_computer.start_hpc())

    start_time = time.time()
    sim.simulate(until=60000 * configuration.cycles_per_ms)
    print(f"simulation took {(time.time() - start_time) / 60} minutes")
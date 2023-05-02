from simso.configuration import Configuration
from simso.configuration.HPCConfig import HPCConfiguration
from simso.configuration.ClusterConfiguration import ClusterConfig
from simso.core.Task import TaskInfo
from simso.core.HPC import HPC
from SimPy.Simulation import Simulation
from simso.generator.task_generator import gen_periods_uniform

def generate_hpc_config(num_clusters, cluster_size, cores, cycles_per_ms=1000000, partition_algorithm="worst_fit"):

    high_performance_computer_config = HPCConfiguration(name="HPC1")
    high_performance_computer_config.partition_algorithm = partition_algorithm
    high_performance_computer_config.cycles_per_ms = cycles_per_ms

    global_node_index = 0
    for cluster_index in range(num_clusters):

        cluster_config = ClusterConfig(cluster_name=f"Cluster {cluster_index}")

        for _ in range(cluster_size):

            new_node = Configuration(node_name=f"Node {global_node_index}")

            new_node.name = f"Node {global_node_index}"
            new_node.scheduler_info.clas = "simso.schedulers.EDF" # global edf scheduler for each node

            for core_index in range(cores):

                new_node.add_processor(name=f"Core {core_index}", identifier=core_index)

            cluster_config.add_node(new_node)
            global_node_index += 1
        
        high_performance_computer_config.add_cluster(cluster_config)

    return high_performance_computer_config

def generate_tasks(hpc_config, num_tasks, num_task_set, min_period, max_period):

    task_metadata = gen_periods_uniform(num_tasks, num_task_set, min_period, max_period)

    for task_index, task_data in enumerate(task_metadata):

        period = task_data[0]
        deadline = 20

        hpc_config.add_task(name=f"task {task_index}", identifier=task_index,
                                    task_type='Cluster', period=period,
                                    deadline=deadline)

    return hpc_config

if __name__ == '__main__':
    
    configuration = generate_hpc_config(4, 4, 64)

    sim = Simulation()

    print(generate_tasks(configuration, 1, 1, 10, 16).task_info_list)
    
    high_performance_computer = HPC(configuration, sim)
    sim.initialize()

    sim.activate(high_performance_computer, high_performance_computer.start_hpc())

    sim.simulate(until=1000)

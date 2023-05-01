from SimPy.Simulation import Process, Monitor, waituntil
from simso.core.Cluster import Cluster
from simso.core.ClusterTask import ClusterGenerator
from simso.core.HPCTaskManager import HPCTaskManager
from simso.core.HPCEvent import HPCEvent, HPCTaskReleaseEvent, \
    HPCTaskAssignEvent, HPCTaskFailedAssignEvent

from collections import deque


class HPC(Process):

    def __init__(self, hpc_configuration, sim):
        
        self.hpc_name = hpc_configuration.name
        Process.__init__(self, name=self.hpc_name, sim=sim)
        self.monitor = Monitor(name="Monitor" + self.hpc_name, sim=sim)

        self.num_clusters = hpc_configuration.num_clusters
        self.cluster_info = hpc_configuration.cluster_info
        self.partition_algorithm = hpc_configuration.partition_algorithm

        if self.partition_algorithm not in {'next_fit', 'worst_fit'}:
            raise ValueError("Invalid partition algorithm")
        
        self.task_list = []

        for task_info in hpc_configuration.task_info_list:
            task_manager = HPCTaskManager(task_info, sim)
            self.task_list.append(task_manager)

        self.cluster_list = []

        for cluster_config in self.cluster_list:
            self.cluster_list.append(Cluster(cluster_config, sim))
        
        self.last_cluster = None
        self.evts = deque([])
    
    def release_task(self, task_info):
        '''
            Release a task to the HPC
        '''

        self.evts.append((HPCEvent.TASK_RELEASE, task_info))

    def next_fit(self, task_info):

        if not self.last_cluster:
            self.last_cluster = self.cluster_list[0]

        last_cluster_index = self.cluster_list.index(self.last_cluster)
        current_cluster_index = (last_cluster_index + 1) % self.num_clusters

        while last_cluster_index != current_cluster_index:
            
            current_cluster_util = sum([x.util for x in self
                                            .cluster_list[current_cluster_index]
                                            .node_list])

            if current_cluster_util + task_info.wcet / task_info.period <= 1:
                
                self.last_cluster = self.cluster_list[current_cluster_index]
                cluster_generator = ClusterGenerator(self.last_cluster,
                                                        self.sim, task_info)
                
                return cluster_generator

            current_cluster_index = (current_cluster_index + 1) % \
                                        self.num_clusters
        
        return None # task failed to be assigned

    def worst_fit(self, task_info):

        min_util = 1
        min_cluster = None

        for cluster in self.cluster_list:

            cluster_util = sum([x.util for x in cluster.node_list])

            if cluster_util < min_util:
                min_util = cluster_util
                min_cluster = cluster
        
        if not min_cluster:
            return None # task failed to be assigned

        if min_util + (task_info.wcet / task_info.period) <= 1:

            cluster_generator = ClusterGenerator(min_cluster, self.sim,
                                                    task_info)
            return cluster_generator 

        return None # task failed to be assigned

    def assign_task(self, task_info):

        partition_algos = {
            'next_fit': self.next_fit,
            'worst_fit': self.worst_fit
        }

        cluster_generator = partition_algos[self.partition_algorithm](task_info)

        return cluster_generator
    
    def start_hpc(self):


        for cluster in self.cluster_list:
            self.sim.activate(cluster, cluster.start_cluster()) # start up the clusters
        
        for task_manager in self.task_list:
            self.sim.activate(task_manager, task_manager.activate_tasks()) # start up the task managers
        
        while True:

            if not self.evts:
                yield waituntil, self, lambda: self.evts
            
            evt = self.evts.popleft()

            if evt[0] == HPCEvent.TASK_RELEASE:

                task_info = evt[1]
                self.monitor.observe(HPCTaskReleaseEvent(task_info))
                task_generator = self.assign_task(task_info)
     

                if task_generator:
                    self.monitor.observe(HPCTaskAssignEvent(task_generator.cluster))
                    task_generator.cluster.add_task(task_generator)

                if not task_generator:
                    self.monitor.observe(HPCTaskFailedAssignEvent(task_info))
from SimPy.Simulation import Process, Monitor, waituntil, hold
from simso.core.Node import Node
from simso.core.ClusterEvent import ClusterEvent, ClusterFailedSchedule,\
    ClusterPassSchedule, ClusterScheduleTask, ClusterNewTask
from simso.core.ClusterTask import ClusterGenerator
from simso.core.Task import Task
from collections import deque
import sys

class Cluster(Process):

    '''
        Cluster class that will hold Node objects and decide which node
        should schedule the tasks. THIS
    '''

    def __init__(self, cluster_configuration, sim):

        self.cluster_name = cluster_configuration.cluster_name

        Process.__init__(self, name=self.cluster_name, sim=sim)

        self.cycles_per_ms = cluster_configuration.cycles_per_ms
        self.monitor = Monitor(name="Monitor" + self.cluster_name, sim=sim)
        self.node_config_list = cluster_configuration.node_config_list
        self.node_list = []

        for node_config in self.node_config_list:
            self.core_count = len(node_config.proc_info_list)
            self.node_list.append(Node(node_config, sim))
        
        self.node_count = len(self.node_list)

        self.evts = deque([])
        self.cluster_threshold = self.node_count * self.core_count
        self.cluster_utilization = 0
    
    def add_task(self, task_generator):
        '''
            Add a task to the cluster
        '''

        self.evts.append((ClusterEvent.NEW_TASK, task_generator))

    def claim_reschedule(self, task_generator):
        '''
            Claim the schedule of the task generator and add it to the queue
        '''

        self.evts.append((ClusterEvent.SCHEDULE_TASK, task_generator))
         
    def schedule_task(self, task_generator):
        '''
            look through all the nodes and find the one with the lowest utilization
            create the task if possible if none
            return none if no node can schedule the task
        '''

        lowest_utilization = sys.maxsize
        lowest_utilization_node = None
        task_info = task_generator.task_info
        task_util = task_info.wcet / task_info.period

        for node in self.node_list:

            if node.util < lowest_utilization:
                lowest_utilization = node.util
                lowest_utilization_node = node
        
        if task_util + lowest_utilization > lowest_utilization_node.cores:
            return None
        
        lowest_utilization_node.util += task_util
        
        return Task(node=lowest_utilization_node,
                        sim=self.sim, task_info=task_info)

    def start_cluster(self):

        for node in self.node_list:
            print(f"activating node {node.name}")
            self.sim.activate(node, node.start_node())

        while True:

            if not self.evts:

                yield waituntil, self, lambda: self.evts
            
            evt = self.evts.popleft()

            if evt[0] == ClusterEvent.NEW_TASK:
                
                self.monitor.observe(ClusterNewTask(self.cluster_name))

                task_generator = evt[1]
                self.sim.activate(task_generator, task_generator.start_generator())
        
            if evt[0] == ClusterEvent.SCHEDULE_TASK:
                
                self.monitor.observe(ClusterScheduleTask(self.cluster_name))
                
                task_generator = evt[1]
                task = self.schedule_task(task_generator)

                if task:
                    self.monitor.observe(ClusterPassSchedule(self.cluster_name))
                    task._node.new_task(task)
                else:
                    self.monitor.observe(ClusterFailedSchedule(self.cluster_name))
            




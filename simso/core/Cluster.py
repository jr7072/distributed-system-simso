from SimPy.Simulation import Process, Monitor, waituntil, hold
from simso.core.Node import Node
from simso.core.HPCEvent import HPCEvent
from simso.core.ClusterEvent import ClusterEvent, ClusterFailedSchedule,\
    ClusterPassSchedule, ClusterScheduleTask, ClusterNewTask
from simso.core.ClusterTask import ClusterGenerator
from simso.core.NodeEvent import NodeEvent
from collections import deque

class Cluster(Process):

    '''
        Cluster class that will hold Node objects and decide which node
        should schedule the tasks. THIS
    '''

    def __init__(self, cluster_configuration, sim):

        self.cluster_name = cluster_configuration.cluster_name

        Process.__init(self, name=self.cluster_name, sim=sim)

        self.monitor = Monitor(name="Monitor" + self.cluster_name, sim=sim)
        self.node_config_list = cluster_configuration.node_config_list
        self.node_list = []

        for node_config in self.node_config_list:
            self.node_list.append(Node(node_config, sim))

        self.task_generator_list = []
        self.evts = deque([])
        self.cluster_utilization = 0
    
    def schedule_task(self, task_generator):
        pass

    def start_cluster(self):

        while True:

            if not self.evts():

                yield waituntil, self, lambda: self.evts
            
            evt = self.evts.popleft()

            if evt[0] == HPCEvent.NEW_TASK:
                
                self.sim.monitor.observe(ClusterNewTask(self.cluster_name))

                task_generator = evt[1]
                self.task_generator_list.append(task)
                self.sim.activate(task, task.start_generator())
        

            if evt[0] == ClusterEvent.SCHEDULE_TASK:
                
                self.sim.monitor.observe(ClusterScheduleTask(self.cluster_name))
                
                task_generator = evt[1]
                task = self.schedule_task(task_generator)

                if task:
                    self.sim.monitor.observe(ClusterPassSchedule(self.cluster_name))
                    task.node.evts.append((NodeEvent.NEW_TASK, task))
                else:
                    self.sim.monitor.observe(ClusterFailedSchedule(self.cluster_name))
            




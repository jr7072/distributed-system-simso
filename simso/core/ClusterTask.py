from simso.core.Task import TaskInfo
from SimPy.Simulation import Process

class ClusterGenerator(Process):

    def __init__(self, task_info, sim):
        
        self.task_info = task_info
        self.name = self.task_info.name
        self.sim = sim
    
        Process.__init__(self, name=self.name, sim=self.sim)


    def start_generator():

        pass

        
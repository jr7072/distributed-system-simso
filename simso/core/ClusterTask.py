from simso.core.Task import TaskInfo
from SimPy.Simulation import Process, hold

class ClusterGenerator(Process):

    def __init__(self, cluster, sim, task_info):
        
        self.task_info = task_info
        print(self.task_info)
        self.cluster = cluster
        self.name = task_info.name
        self.sim = sim
    
        Process.__init__(self, name=self.name, sim=self.sim)


    def start_generator(self):

        while True: 

            self.cluster.claim_reschedule(self)

            yield hold, self, int(self.task_info.period * self.cluster.cycles_per_ms) # sleep till its time for reschedule


        
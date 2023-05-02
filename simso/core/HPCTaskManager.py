from SimPy.Simulation import Process, hold

class HPCTaskManager(Process):

    def __init__(self, task_info, hpc, sim):

        self.task_info = task_info
        self.hpc = hpc
        self.sim = sim

        Process.__init__(self, name=self.task_info.name, sim=self.sim)
    

    def activate_task(self):

        yield hold, self, int(self.task_info.activation_date *
                                self.hpc.cycles_per_ms)
        
        self.hpc.release_task(self.task_info)
from SimPy.Simulation import Process, hold

class HPCTaskManager(Process):

    def __init__(self, task_info, hpc, sim):

        self.task_info = task_info
        self.hpc = hpc
        self.sim = sim

        Process.__init__(self, name=self.task_info.name, sim=self.sim)
    

    def activate_task(self):

        yield self, hold, int(self.task_info.activation_date *
                                self.sim.cycles_per_ms)
        
        self.hpc.release_task(self.task_info)
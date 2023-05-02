from simso.core.Task import TaskInfo
import os

class HPCConfiguration:

    def __init__(self, name):
        
        self.name = name
        self.cluster_info = []
        self.partition_algorithm = 'worst_fit'
        self.task_info_list = []
        self.cycles_per_ms = 1000000
        self.cur_dir = os.curdir
    
    def add_cluster(self, cluster_config):
        self.cluster_info.append(cluster_config)
    
    def add_task(self, name, identifier, task_type="Periodic",
                 abort_on_miss=True, period=10, activation_date=0,
                 n_instr=0, mix=0.5, stack_file="", wcet=0, acet=0,
                 et_stddev=0, deadline=10, base_cpi=1.0, followed_by=None,
                 list_activation_dates=[], preemption_cost=0, data=None):

        task = TaskInfo(name, identifier, task_type, abort_on_miss, period,
                        activation_date, n_instr, mix,
                        (stack_file, self.cur_dir), wcet, acet, et_stddev,
                        deadline, base_cpi, followed_by, list_activation_dates,
                        preemption_cost, data)
        
        self.task_info_list.append(task)




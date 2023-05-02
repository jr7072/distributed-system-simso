# coding=utf-8

from SimPy.Simulation import Simulation, Process, Monitor, hold, waituntil
from simso.core.Processor import Processor
from collections import deque
from simso.core.Task import Task
from simso.core.Timer import Timer
from simso.core.etm import execution_time_models
from simso.core.Logger import Logger
from simso.core.results import Results
from simso.core.NodeEvent import NodeEvent, NodeNewTaskEvent, NodeTaskTerminateEvent


class Node(Process):
    """
    Main class for the simulation. It instantiate the various components
    required by the simulation and run it.
    """

    def __init__(self, configuration, sim: Simulation, callback=None):
        """
        Args:
            - `callback`: A callback can be specified. This function will be \
                called to report the advance of the simulation (useful for a \
                progression bar).
            - `configuration`: The :class:`configuration \
                <simso.configuration.Configuration>` of the simulation.

        Methods:
        """

        self.name = configuration.node_name
        Process.__init__(self, name=self.name, sim=sim)

        proc_info_list = configuration.proc_info_list

        self.sim = sim
        self.util = 0
        self._duration = configuration.duration 
        self._cycles_per_ms = configuration.cycles_per_ms
        self.scheduler = configuration.scheduler_info.instantiate(self, sim)
       

        self.evts = deque([])

        try:
            self._etm = execution_time_models[configuration.etm](
                self, len(proc_info_list)
            )
        except KeyError:
            print("Unknowned Execution Time Model.", configuration.etm)

        # Init the processor class. This will in particular reinit the
        # identifiers to 0.
        Processor.init()

        # Initialization of the caches
        for cache in configuration.caches_list:
            cache.init()

        self._processors = []
        for proc_info in proc_info_list:
            proc = Processor(self, sim, proc_info)
            proc.caches = proc_info.caches
            self._processors.append(proc)
        
        self.cores = len(self._processors)

        # XXX: too specific.
        self.penalty_preemption = configuration.penalty_preemption
        self.penalty_migration = configuration.penalty_migration

        self._etm.init()
        
        self._callback = callback
        self.scheduler.task_list = []
        self.scheduler.processors = self._processors
        self.results = None

    def now_ms(self):
        return float(self.now()) / self._cycles_per_ms

    @property
    def logs(self):
        """
        All the logs from the :class:`Logger <simso.core.Logger.Logger>`.
        """
        return self._logger.logs

    @property
    def logger(self):
        return self._logger

    @property
    def cycles_per_ms(self):
        """
        Number of cycles per milliseconds. A cycle is the internal unit used
        by SimSo. However, the tasks are defined using milliseconds.
        """
        return self._cycles_per_ms

    @property
    def etm(self):
        """
        Execution Time Model
        """
        return self._etm

    @property
    def processors(self):
        """
        List of all the processors.
        """
        return self._processors

    @property
    def task_list(self):
        """
        List of all the tasks.
        """
        return self._task_list

    @property
    def duration(self):
        """
        Duration of the simulation.
        """
        return self._duration

    def _on_tick(self):
        if self._callback:
            self._callback(self.now())

    def new_task(self, task):

        self.evts.append((NodeEvent.NEW_TASK, task))

    def start_node(self):
        
        """ Simulate a Node """
        self.scheduler.init()

        for cpu in self._processors:
            self.sim.activate(cpu, cpu.run())

        while True:

            if not self.evts:
                yield waituntil, self, lambda: self.evts# let the processors and tasks run

            evt = self.evts.popleft()

            if evt[0] == NodeEvent.NEW_TASK:
                
                task = evt[1]
                self.sim.monitor.observe(NodeNewTaskEvent(self.node_name))
                self.scheduler.add_task(task)
                self.sim.activate(task, task.run())
             

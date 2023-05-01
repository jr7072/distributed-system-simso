from simso.configuration import Configuration
from simso.core import Node
from simso.schedulers import EDF
from SimPy.Simulation import Simulation

def test_node():

    configuration = Configuration("node_1")
    configuration.duration = 100

    configuration.add_processor(name="core 1", identifier=1, speed=1)

    configuration.scheduler_info.clas = 'simso.schedulers.EDF'

    sim = Simulation()

    node = Node(configuration, sim)

    sim.initialize()
    sim.activate(node, node.start_node())
    sim.simulate(until=100)


if __name__ == '__main__':
    
    test_node()
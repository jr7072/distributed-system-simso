

class ClusterConfig:

    def __init__(self, cluster_name):

        self.cluster_name = cluster_name
        self.node_config_list = []
        self.cycles_per_ms = 1000000
    
    def add_node(self, node_config):
        self.node_config_list.append(node_config)
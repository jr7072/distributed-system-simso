

class HPCConfiguration:

    def __init__(self, name):
        
        self.name = name
        self.cluster_config_list = []
    
    def add_cluster(self, cluster_config):
        self.cluster_config_list.append(cluster_config)



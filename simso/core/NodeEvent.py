class NodeEvent(object):

    NEW_TASK = 1

    def __init__(self, event, args=None):
        self.event = event

class NodeNewTaskEvent(NodeEvent):
    
    def __init__(self, node):
        NodeEvent.__init__(self, NodeEvent.NEW_TASK, node)

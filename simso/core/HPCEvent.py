
class HPCEvent(object):

    NEW_TASK = 1

    def __init__(self, event, args=None):
        self.event = event


class HPCNewTaskEvent(HPCEvent):
    
    def __init__(self, node):
        HPCEvent.__init__(self, HPCEvent.NEW_TASK, node)

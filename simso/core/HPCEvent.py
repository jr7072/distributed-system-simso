
class HPCEvent(object):

    TASK_RELEASE = 1
    TASK_ASSIGN = 2
    TASK_FAILED_ASSIGN = 3

    def __init__(self, event, args=None):
        self.event = event


class HPCTaskReleaseEvent(HPCEvent):
    
    def __init__(self, task):
        HPCEvent.__init__(self, HPCEvent.TASK_RELEASE, task)


class HPCTaskAssignEvent(HPCEvent):
    
    def __init__(self, cluster):
        HPCEvent.__init__(self, HPCEvent.TASK_ASSIGN, cluster)
    

class HPCTaskFailedAssignEvent(HPCEvent):
    
    def __init__(self, task):
        HPCEvent.__init__(self, HPCEvent.TASK_FAILED_ASSIGN, task)

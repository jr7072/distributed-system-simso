

class ClusterEvent(object):

    NEW_TASK = 1
    SCHEDULE_TASK = 2
    FAILED_SCHEDULE = 3
    PASS_SCHEDULE = 4

    def __init__(self, event, args=None):
        self.event = event
        self.args = args


class ClusterNewTask(ClusterEvent):
         
        def __init__(self, task):
            ClusterEvent.__init__(self, ClusterEvent.NEW_TASK, task)


class ClusterFailedSchedule(ClusterEvent):

    def __init__(self, task):
        ClusterEvent.__init__(self, ClusterEvent.FAILED_SCHEDULE, task)


class ClusterPassSchedule(ClusterEvent):

    def __init__(self, task):
        ClusterEvent.__init__(self, ClusterEvent.PASS_SCHEDULE, task)


class ClusterScheduleTask(ClusterEvent):
    
        def __init__(self, task):
            ClusterEvent.__init__(self, ClusterEvent.SCHEDULE_TASK, task)
import time

from sparts.vservice import VService
from sparts.tasks.periodic import PeriodicTask
from sparts.tasks.queue import QueueTask


class CommandReceiver(QueueTask):
    def initTask(self):
        super(QTask, self).initTask()

    def interpret(self, command, context):
        if command
            return
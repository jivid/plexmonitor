# write a queue task that does two things: echo and stat
# echo will take an argument and print that out
# and then write two periodic tasks that alternate
# calling echo and stat on the queue task
# that would be a pretty comprehensive exercise

from sparts.vservice import VService
from sparts.tasks.periodic import PeriodicTask
from sparts.tasks.queue import QueueTask

import time


class QTask(QueueTask):
    def initTask(self):
        super(QTask, self).initTask()

    def execute(self, item, context):
        if item["item"] == "echo":
            print(item["message"])

        elif item["item"] == "stat":
            print(time.strftime('%l:%M%p %Z on %b %d, %Y'))

        elif "item" not in item.keys():
            raise ("payload did not have 'item' ")


class SubmitEcho(PeriodicTask):
    # defined in seconds
    INTERVAL = 1

    def initTask(self):
        super(SubmitEcho, self).initTask()
        self.QueueTask = self.service.requireTask("QTask")

    def execute(self, context=None):
        # context is the queue task instance
        data = {"item": "echo", "message": "default string"}
        self.QueueTask.submit(data)


class SubmitStat(PeriodicTask):
    # defined in seconds
    INTERVAL = 1.4

    def initTask(self):
        super(SubmitStat, self).initTask()
        self.QueueTask = self.service.requireTask("QTask")

    def execute(self, context=None):
        data = {"item": "stat"}
        self.QueueTask.submit(data)


class TestService(VService):
    TASKS = [SubmitEcho, SubmitStat, QTask]

if __name__ == '__main__':
    TestService.initFromCLI()

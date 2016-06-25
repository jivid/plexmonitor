# So your service is one class
# All your tasks are one class each
# In your service class you just have a TASKS class variable listing which
# tasks need to be run
# There's some sample tasks in sparts repo too, take a look

# Like make a couple of tasks, one periodic maybe, and one queue task
# Send some stuff to the queue periodically and just print out what the
# queue got

from sparts.vservice import VService
from sparts.vtask import VTask


class TaskOne(VTask):
    # need to define this, as LOOPLESS is defined as False by default
    LOOPLESS = True
    def initTask(self) -> None:
        print("hello, I am task one")


class TaskTwo(VTask):
#     LOOPLESS = True
    def initTask(self) -> None:
        super(TaskTwo, self).initTask()

    def _runloop(self):
        print("hello, I am task two")


# by convention we define this TASKS list as a queue of tasks
class TestService(VService):
    TASKS = [TaskOne, TaskTwo]

if __name__ == '__main__':
    TestService.initFromCLI()

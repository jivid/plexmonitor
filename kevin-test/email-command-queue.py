from sparts.tasks.queue import QueueTask


class EmailCommandQueue(QueueTask):
    def initTask(self):
        super(EmailCommandQueue, self).initTask()

    def execute(self, item, context):
        type = "command"
        if item[type] == "status":
            print(item[])

        elif item[type] == "logs":
            print(item[])

        elif item[type] == "fix":
            print(item[])

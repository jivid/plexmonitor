from sparts.tasks.periodic import PeriodicTask

from plexmonitor.lib.email import Inbox


class EmailTask(PeriodicTask):
    """ Periodic task to read the email inbox and scan for new commands.
    To prevent against potential DOS, the task will only look at one email
    per iteration, the most recent one. If the most recent mail has already
    been processed, the iteration will be a no-op.
    """

    INTERVAL = 10.0

    def initTask(self) -> None:
        super(EmailTask, self).initTask()
        self.inbox = Inbox()
        self.inbox.connect()
        self.last_mail_id = None  # type: str

    def execute(self) -> None:
        last_unread = self.inbox.get_last_unread_mail_id()
        last_processed = self.last_mail_id

        if last_processed is not None and\
                int(last_unread) <= int(last_processed):
            self.logger.info("Nothing to fetch")
            return

        self.logger.info("Going to fetch mail ID {}".format(last_unread))
        mail = self.inbox.fetch(last_unread)  # type: email.message.Message
        self.last_mail_id = last_unread

        cmd = mail.get('Subject')
        self.logger.info("Got email with subject {}".format(cmd))

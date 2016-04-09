import logging
import sys
from functools import partial

from sparts.vservice import VService
from sparts.compat import captureWarnings

from plexmonitor.tasks.email_task import EmailTask


class PlexMonitorService(VService):
    TASKS = [
        EmailTask,
    ]

    def initLogging(self) -> None:
        fmt = "{asctime} [{levelname}] [{name}] {message}"
        config_logging = partial(logging.basicConfig,
                                 format=fmt,
                                 level=self.loglevel,
                                 style='{')
        if self.logfile:
            config_logging(filename=self.logfile)
        else:
            config_logging(stream=sys.stderr)

        captureWarnings(True)


PlexMonitorService.initFromCLI()

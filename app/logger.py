from collections import deque
from datetime import datetime
import json
import logging
from logging import config


class ReasonerLogEntryFormatter(logging.Formatter):
    """Format to match Reasoner API LogEntry"""

    def format(self, record):
        log_entry = {}

        # If given a string use that as the message
        if isinstance(record.msg, str):
            log_entry["message"] = record.msg

        # If given a dict, just use that as the log entry
        # Make sure everything is serializeable
        if isinstance(record.msg, dict):
            log_entry |= record.msg

        # Add timestamp
        iso_timestamp = datetime.utcfromtimestamp(record.created).isoformat()
        log_entry["timestamp"] = iso_timestamp

        # Add level
        log_entry["level"] = record.levelname

        return log_entry


class QueryLogHandler(logging.Handler):
    """Log Handler."""

    def __init__(self, log_queue):
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    def emit(self, record):
        # put newer messages in front
        self.log_queue.appendleft(self.format(record))

    def contents(self):
        """Get stored logs from handler."""
        return self.log_queue


# Create unique logger for each query
# https://stackoverflow.com/a/37967421
class QueryLogger(object):
    """Query-specific logger."""

    def __init__(self, maxlen=None):
        self._log_queue = deque(maxlen=maxlen)
        self._log_handler = QueryLogHandler(self._log_queue)
        self._log_handler.setFormatter(ReasonerLogEntryFormatter())

    @property
    def log_handler(self):
        return self._log_handler


def get_logger(qid, log_level):
    log_handler = QueryLogger().log_handler
    logger = logging.getLogger(f"appraiser.{qid}")
    level_number = logging._nameToLevel[log_level]
    logger.setLevel(level_number)
    logger.addHandler(log_handler)
    return logger


def setup_logger():
    with open("logging_setup.json", "r") as f:
        logging_config = json.load(f)

    config.dictConfig(logging_config)

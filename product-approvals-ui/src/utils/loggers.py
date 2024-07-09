import inspect
import logging
import os
import sys
from typing import Optional

import json_log_formatter

# DO NOT CHANGE LOGGING FORMAT
LOG_FORMAT: str = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
# REQUIRED FOR DATADOG COMPATIBILITY


class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        extra = super().json_record(message, extra, record)
        extra["level"] = record.levelname
        extra["name"] = record.name
        extra["lineno"] = record.lineno
        extra["pathname"] = record.pathname
        return extra


def make_json_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """Create a JSON logger. This allows us to pass arbitrary key/value data in log messages.
    It also puts stack traces in a single log message instead of spreading them across multiple log messages.
    """
    if name is None or not isinstance(name, str) or len(name) == 0:
        raise ValueError("Name must be a non-empty string.")

    logger = logging.getLogger(name)
    if any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        # logger already initialized
        return logger

    stream_handler = logging.StreamHandler()
    in_kubernetes = os.getenv("KUBERNETES_SERVICE_HOST")
    if in_kubernetes:
        stream_handler.setFormatter(CustomJSONFormatter())
    else:
        # Reading JSON logs in your terminal is kinda hard, and you can't make use of the structured data
        # benefits in your terminal anyway. So just fall back to the standard log format.
        stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(stream_handler)
    logger.setLevel(log_level)

    # Something is creating an extra handler
    logger.propagate = (
        False  # Don't need to set to False as long as you don't also call logging.basicConfig()
    )

    # Want to make sure that unhandled exceptions get logged using the JSON logger. Otherwise,
    # users will have to remember to wrap their main functions with:
    #
    # try:
    #     main()
    # except Exception:
    #     logger.exception("blah")
    #
    # See: https://stackoverflow.com/a/16993115/1729558
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception
    return logger


def make_logger(name: str, log_level: int = -1) -> logging.Logger:
    if log_level == -1:
        log_level = logging.DEBUG
    logger = make_json_logger(name, log_level)
    return logger


def _filename_wo_ext(filename: str) -> str:
    """Gets the filename, without the file extension, if present."""
    return os.path.split(filename)[1].split(".", 1)[0]


def logger_name(*, fallback_name: Optional[str] = None) -> str:
    """Returns the __name__ from where the calling function is defined or its filename if it is "__main__".

    Normally, __name__ is the fully qualified Python name of the module. However, if execution starts at
    the module, then it's __name__ attribute is "__main__". In this scenario, we obtain the module's filename.

    The returned string is as close to a unique Python name for the caller's defining module.

    NOTE: If :param:`fallback_name` is provided and is not-None and non-empty, then, in the event that
          the logger name cannot be inferred from the calling __main__ module, this value will be used
          instead of raising a ValueError.
    """
    # Get the module where the calling function is defined.
    # https://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
    stack = inspect.stack()
    calling_frame = stack[1]
    calling_module = inspect.getmodule(calling_frame[0])
    if calling_module is None:
        raise ValueError(
            f"Cannot obtain module from calling function. Tried to use calling frame {calling_frame}"
        )
    # we try to use this module's name
    name = calling_module.__name__
    if name == "__main__":
        # unless logger_name was called from an executing script,
        # in which case we use it's file name

        if hasattr(calling_module, "__file__"):
            return _filename_wo_ext(calling_module.__file__)  # type: ignore
        if fallback_name is not None:
            fallback_name = fallback_name.strip()
            if len(fallback_name) > 0:
                return fallback_name
        raise ValueError("Cannot determine calling module's name from its __file__ attribute!")
    return name

# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import functools

try:
    import squish
except ImportError:
    import squishtest as squish

import test


class LogLevel:
    DEBUG = 10
    LOG = 20
    WARNING = 30
    FAIL = 40
    FATAL = 50

    _nameToLevel = {
        "FATAL": FATAL,
        "FAIL": FAIL,
        "WARN": WARNING,
        "WARNING": WARNING,
        "LOG": LOG,
        "DEBUG": DEBUG,
    }


def __translate_Level(level) -> int:
    """Translates the given log level to valid LogLevel

    Args:
        level (int|str): log level to translate
    """
    if isinstance(level, int):
        rv = level
    elif isinstance(level, str):
        if level not in LogLevel._nameToLevel:
            raise ValueError(f"Unknown LogLevel: {level}")
        rv = LogLevel._nameToLevel[level]
    else:
        raise TypeError(f"LogLevel is not an integer or a valid string: {level}")
    return rv


def set_level(level) -> None:
    """Sets the Squish logging level, Level must be an int or a str.

    Args:
        level (int|str): log level to set

    Examples:
       >>> set_level(report.LogLevel.WARNING)
       >>> set_level("FAIL")
    """
    global LOGLEVEL
    LOGLEVEL = __translate_Level(level)


set_level(LogLevel.LOG)

_test_log = test.log
_test_warning = test.warning
_test_fail = test.fail
_test_fatal = test.fatal


def __is_level_enabled(level: LogLevel) -> bool:
    """Checks the given log level against the currently set LOGLEVEL

    Args:
        level (LogLevel): log level to check

    Returns:
        bool: True if level is equal to or higher than LOGLEVEL, False otherwise
    """
    return LOGLEVEL <= level


def debug(msg: str, details: str = "") -> None:
    """Adds a DEBUG-level log entry with the given message and details to a test report.

    This function adds a log message to Squish's test report at the DEBUG log level,
    which allows for detailed debugging information to be recorded.
    The log message will include the given message and details provided as arguments.
    The message will be prefixed with the string 'DEBUG: ' to indicate its log level.

    The log message will only be visible if the LOGLEVEL is set to DEBUG.
    Otherwise, it will be ignored and not included in the test report.

    Args:
        msg (str): The message to include in the log entry.
        details (str): Optional additional details to include in the log entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.DEBUG):
        test.fixateResultContext(1)
        try:
            _test_log(f"[DEBUG] {msg}", details)
        finally:
            test.restoreResultContext()


def log(msg: str, details: str = "") -> None:
    """Adds a log entry with the given message and details to a test report.

    This function adds a log message to Squish's test report at the LOG log level
    or lower, depending on the current log level setting.
    The log message will include the given message and details provided as arguments.

    The log message will only be visible if the LOGLEVEL is set to LOG or lower.
    Otherwise, it will be ignored and not included in the test report.

    Args:
        msg (str): The message to include in the log entry.
        details (str): Optional additional details to include in the log entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.LOG):
        test.fixateResultContext(1)
        try:
            _test_log(msg, details)
        finally:
            test.restoreResultContext()


def warning(msg: str, details: str = "") -> None:
    """Adds a warning entry with the given message and details to a test report.

    This function adds a warning message to Squish's test report at the WARNING
    log level or lower, depending on the current log level setting.
    The warning message will include the given message and details provided
    as arguments.

    The warning message will only be visible if the LOGLEVEL is set to WARNING or lower.
    Otherwise, it will be ignored and not included in the test report.

    Args:
        msg (str): The message to include in the warning entry.
        details (str): Optional additional details to include in the warning entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.WARNING):
        test.fixateResultContext(1)
        try:
            _test_warning(msg, details)
        finally:
            test.restoreResultContext()


def fail(msg: str, details: str = "") -> None:
    """Adds a fail entry with the given message and details to a test report.

    This function adds a fail message to Squish's test report at the FAIL log level
    or lower, depending on the current log level setting.
    The fail message will include the given message and details provided as arguments.

    The fail message will only be visible if the LOGLEVEL is set to FAIL or lower.
    Otherwise, it will be ignored and not included in the test report.

    Args:
        msg (str): The message to include in the fail entry.
        details (str): Optional additional details to include in the fail entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.FAIL):
        test.fixateResultContext(1)
        try:
            _test_fail(msg, details)
        finally:
            test.restoreResultContext()


def fatal(msg: str, details: str = "") -> None:
    """Adds a fatal entry with the given message and details to a test report,
    then aborts the test case execution.

    This function adds a fatal message to Squish's test report at the FATAL log level
    or lower, depending on the current log level setting.
    The fatal message will include the given message and details provided as arguments.

    The fatal message will only be visible if the LOGLEVEL is set to FATAL or lower.
    Otherwise, it will be ignored and not included in the test report.

    After adding the fatal message, the function aborts the test case execution.

    Args:
        msg (str): The message to include in the fatal entry.
        details (str): Optional additional details to include in the fatal entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.FATAL):
        test.fixateResultContext(1)
        try:
            squish.testSettings.throwOnFailure = True
            _test_fatal(msg, details)
        finally:
            test.restoreResultContext()


def enable_loglevel_in_test_module() -> None:
    """Adds support for log levels to the Squish 'test' module.

    !!! warning
        This function uses monkey pathching
        https://en.wikipedia.org/wiki/Monkey_patch

    This function overwrites some of the existing functions in the 'test' module
    to support logging at different log levels.
    Furthermore, it enhances the functionality of the 'test' module by adding
    a new test.debug(...) function.

    By default, the 'test' module does not support LOGLEVEL at all.
    However, this function adds support for setting the log level to a higher
    or lower level, depending on the needs of the developer.

    After calling this function, the following 'test' module's functions will support
    LOGLEVEL report setting:

        - test.debug(...)
        - test.log(...)
        - test.warning(...)
        - test.fail(...)
        - test.fatal(...)

    Returns:
        None
    """
    test.debug = debug
    test.log = log
    test.warning = warning
    test.fail = fail
    test.fatal = fatal


class section:
    """Allows using Squish's sections as context managers and function decorators
    https://doc.qt.io/squish/squish-api.html#test-startsection-function
    """

    def __init__(self, title, description=""):
        """
        Args:
            title (str): Section title
            description (str): Optional additional description of the section

        Examples:
            ```python
            with section("Add new person"):
                squish.type(squish.waitForObject(names.forename_edit), "Bob")
                squish.mouseClick(squish.waitForObject(names.ok_button))
            ```
        """
        self.title = title
        self.description = description

    def __call__(self, func):
        """Executed when section is used as a decorator"""

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            test.fixateResultContext(1)
            test.startSection(self.title, self.description)
            test.restoreResultContext()
            try:
                result = func(*args, **kwargs)
            finally:
                test.endSection()
            return result

        return wrapped

    def __enter__(self):
        """Executed when section is used as a context manager"""
        test.fixateResultContext(1)
        test.startSection(self.title, self.description)
        test.restoreResultContext()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Executed after section is used as a context manager"""
        test.endSection()

# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from contextlib import contextmanager

import squish
import test


class LogLevel:
    DEBUG = 10
    LOG = 20
    WARNING = 30
    FAIL = 40
    FATAL = 50


LOGLEVEL = LogLevel.LOG


def __is_level_enabled(level: LogLevel) -> bool:
    """Checks the given log level against the currently set LOGLEVEL

    Args:
        level (LogLevel): log level to check

    Returns:
        bool: True if level is higher then LOGLEVEL, False otherwise
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
    - msg (str): The message to include in the log entry.
    - details (str): Optional additional details to include in the log entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.DEBUG):
        test.fixateResultContext(1)
        try:
            test.log(f"[DEBUG] {msg}", details)
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
    - msg (str): The message to include in the log entry.
    - details (str): Optional additional details to include in the log entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.LOG):
        test.fixateResultContext(1)
        try:
            test.log(msg, details)
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
    - msg (str): The message to include in the warning entry.
    - details (str): Optional additional details to include in the warning entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.WARNING):
        test.fixateResultContext(1)
        try:
            test.warning(msg, details)
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
    - msg (str): The message to include in the fail entry.
    - details (str): Optional additional details to include in the fail entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.FAIL):
        test.fixateResultContext(1)
        try:
            test.fail(msg, details)
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
    - msg (str): The message to include in the fatal entry.
    - details (str): Optional additional details to include in the fatal entry.

    Returns:
        None
    """
    if __is_level_enabled(LogLevel.FATAL):
        test.fixateResultContext(1)
        try:
            squish.testSettings.throwOnFailure = True
            test.fatal(msg, details)
        finally:
            test.restoreResultContext()


def enable_loglevel_in_test_module():
    """Adds support for log levels to the Squish 'test' module.

    DISCLAIMER: This function uses monkeypathching
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


@contextmanager
def section(title: str, description: str = "") -> None:
    """Allows using Squish's sections as context managers

    https://doc.qt.io/squish/squish-api.html#test-startsection-function
    Args:
        title (str): Section title
        description (str): Optional additional description of the section
    Examples:
        with section("Add new person"):
            squish.type(squish.waitForObject(names.forename_edit), "Bob")
            squish.mouseClick(squish.waitForObject(names.ok_button))
    """

    test.fixateResultContext(1)
    test.startSection(title, description)
    test.restoreResultContext()
    try:
        yield
    except Exception:
        raise
    finally:
        test.endSection()

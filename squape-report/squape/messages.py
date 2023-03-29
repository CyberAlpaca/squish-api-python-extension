# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import sys
from contextlib import contextmanager

import test
import squish


class LogLevel():
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
    """Adds a DEBUG entry to Squish's test report with the given message and detailes.
    The message is in fact a LOG message with a DEBUG prefix. The message will be
    visible only if the LOGLEVEL is set to DEBUG

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if __is_level_enabled(LogLevel.DEBUG):
        test.fixateResultContext(1)
        try:
            test.log(f"[DEBUG] {msg}", details)
        finally:
            test.restoreResultContext()


def log(msg: str, details: str = "") -> None:
    """Adds a LOG entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to LOG or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if __is_level_enabled(LogLevel.LOG):
        test.fixateResultContext(1)
        try:
            test.log(msg, details)
        finally:
            test.restoreResultContext()


def warning(msg: str, details: str = "") -> None:
    """Adds a WARNING entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to WARNING or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if __is_level_enabled(LogLevel.WARNING):
        test.fixateResultContext(1)
        try:
            test.warning(msg, details)
        finally:
            test.restoreResultContext()


def fail(msg: str, details: str = "") -> None:
    """Adds a FAIL entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to FAIL or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if __is_level_enabled(LogLevel.FAIL):
        test.fixateResultContext(1)
        try:
            test.fail(msg, details)
        finally:
            test.restoreResultContext()


def fatal(msg: str, details: str = "") -> None:
    """Adds a FATAL entry to Squish's test report with the given message and detailes
    then interrupts the test execution.
    The message will be visible only if the LOGLEVEL is set to FATAL or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if __is_level_enabled(LogLevel.FATAL):
        test.fixateResultContext(1)
        try:
            squish.testSettings.throwOnFailure = True
            test.fatal(msg, details)
        finally:
            test.restoreResultContext()


@contextmanager
def section(title: str, description: str = "") -> None:
    """Allows using sections as context managers

    https://doc.qt.io/squish/squish-api.html#test-startsection-function
    Args:
        title (str): the section title
        description (str): the section description
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

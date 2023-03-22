# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from contextlib import contextmanager
from enum import Enum

import test


class LogLevel(Enum):
    DEBUG = 0
    LOG = 1
    WARNING = 2
    FAIL = 3
    FATAL = 4


LOGLEVEL = LogLevel.LOG


def debug(msg: str, details: str = "") -> None:
    """Adds a DEBUG entry to Squish's test report with the given message and detailes.
    The message is in fact a LOG message with a DEBUG prefix. The message will be
    visible only if the LOGLEVEL is set to DEBUG

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if LOGLEVEL == LogLevel.DEBUG:
        test.fixateResultContext(2)
        test.log(f"[DEBUG] {msg}", details)
        test.restoreResultContext()


def log(msg: str, details: str = "") -> None:
    """Adds a LOG entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to LOG or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if LOGLEVEL <= LogLevel.LOG:
        test.fixateResultContext(2)
        test.log(msg, details)
        test.restoreResultContext()


def warning(msg: str, details: str = "") -> None:
    """Adds a WARNING entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to WARNING or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if LOGLEVEL <= LogLevel.WARNING:
        test.fixateResultContext(2)
        test.warning(msg, details)
        test.restoreResultContext()


def fail(msg: str, details: str = "") -> None:
    """Adds a FAIL entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to FAIL or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if LOGLEVEL <= LogLevel.FAIL:
        test.fixateResultContext(2)
        test.fail(msg, details)
        test.restoreResultContext()


def fatal(msg: str, details: str = "") -> None:
    """Adds a FATAL entry to Squish's test report with the given message and detailes.
    The message will be visible only if the LOGLEVEL is set to FATAL or lower

    Args:
        msg (str): Message
        detail (str, optional): Details of the message. Defaults to "".
    """
    if LOGLEVEL <= LogLevel.FATAL:
        test.fixateResultContext(2)
        test.fatal(msg, details)
        test.restoreResultContext()


test.debug = debug
test.log = log
test.warning = warning
test.fail = fail
test.fatal = fatal


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

    test.fixateResultContext(2)
    test.startSection(title, description)
    test.restoreResultContext()
    try:
        yield
    except Exception:
        raise
    finally:
        test.endSection()

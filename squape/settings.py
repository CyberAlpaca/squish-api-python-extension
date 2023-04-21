# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from contextlib import contextmanager
from squape.internal.exceptions import SquishCapability

import squish

@contextmanager
def _ctx_settings(setting_name, value):
    """
     A context manager that temporarily sets a Squish testSettings to a given value.

    Args:
        setting_name (str): The name of the Squish testSettings to set.
        value (Any): The value to set the Squish test setting to.

    Raises:
        SquishCapability: If the Squish version does not support the given test setting.

    """
    try:
        current_value = getattr(squish.testSettings, setting_name)
        setattr(squish.testSettings, setting_name, value)
    except AttributeError as _:
        raise SquishCapability(
            f"Your Squish version does not support test setting {setting_name}"
        )

    try:
        yield
    except Exception:
        raise
    finally:
        setattr(squish.testSettings, setting_name, current_value)


@contextmanager
def logScreenshotOnPass(enabled: bool) -> None:
    """Allows using logScreenshotOnPass test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonpass

    Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on PASS test result.
    """
    with _ctx_settings("logScreenshotOnPass", enabled) as c:
        yield [c]


@contextmanager
def logScreenshotOnFail(enabled: bool) -> None:
    """Allows using logScreenshotOnFail test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonfail

    Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on FAIL test result.
    """

    with _ctx_settings("logScreenshotOnFail", enabled) as c:
        yield [c]


@contextmanager
def logScreenshotOnWarning(enabled: bool) -> None:
    """Allows using logScreenshotOnWarning test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonwarning

     Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on warning log entry.

    """
    with _ctx_settings("logScreenshotOnWarning", enabled) as c:
        yield [c]


@contextmanager
def logScreenshotOnError(enabled: bool) -> None:
    """Allows using logScreenshotOnError test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonerror

    Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on script error.

    """
    current_value = squish.testSettings.logScreenshotOnError
    squish.testSettings.logScreenshotOnError = enabled
    yield
    squish.testSettings.logScreenshotOnError = current_value


@contextmanager
def silentVerifications(enabled: bool) -> None:
    """Allows using silentVerifications test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-silentverifications

    Args:
        enabled (bool): Whether silent verifications are enabled.

    """
    with _ctx_settings("silentVerifications", enabled) as c:
        yield [c]


@contextmanager
def imageSearchTolerant(enabled: bool) -> None:
    """Allows using imageSearchTolerant test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagesearchtolerant

    Args:
        enabled (bool): Whether image search with tolerance is enabled.
    """
    with _ctx_settings("imageSearchTolerant", enabled) as c:
        yield [c]


@contextmanager
def imageSearchThreshold(threshold: float) -> None:
    """Allows using imageSearchThreshold test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchthreshold

    Args:
        threshold (float): the threshold for image search.
    """
    with _ctx_settings("imageSearchThreshold", threshold) as c:
        yield [c]


@contextmanager
def imageSearchMultiscale(enabled: bool) -> None:
    """Allows using imageSearchMultiscale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagesearchmultiscale

    Args:
        enabled (bool): Whether multi-scale image search is enabled.

    """
    with _ctx_settings("imageSearchMultiscale", enabled) as c:
        yield [c]


@contextmanager
def imageSearchMinScale(min_scale: float) -> None:
    """Allows using imageSearchMinScale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchminscale

    Args:
        min_scale (float): A float value indicating the minimum scale for image search.
    """
    with _ctx_settings("imageSearchMinScale", min_scale) as c:
        yield [c]


@contextmanager
def imageSearchMaxScale(max_scale: float) -> None:
    """Allows using imageSearchMaxScale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchmaxscale

    Args:
        max_scale (float): A float value indicating the maximum scale for image search.
    """
    with _ctx_settings("imageSearchMaxScale", max_scale) as c:
        yield [c]


@contextmanager
def waitForObjectTimeout(timeout_ms: int) -> None:
    """Allows using waitForObjectTimeout test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#integer-testsettings-waitforobjecttimeout

    Args:
        timeout_ms (int): A integer value indicating the timeout in ms.
    """
    with _ctx_settings("waitForObjectTimeout", timeout_ms) as c:
        yield [c]


@contextmanager
def objectNotFoundDebugging(enabled: bool) -> None:
    """Allows using objectNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-objectnotfounddebugging

    Args:
        enabled (bool): Whether to enable debugging when object is not found.

    """
    with _ctx_settings("objectNotFoundDebugging", enabled) as c:
        yield [c]


@contextmanager
def imageNotFoundDebugging(enabled: bool) -> None:
    """Allows using imageNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagenotfounddebugging

     Args:
        enabled (bool): Whether to enable debugging when image is not found.
    """
    with _ctx_settings("imageNotFoundDebugging", enabled) as c:
        yield [c]


@contextmanager
def textNotFoundDebugging(enabled: bool) -> None:
    """Allows using textNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-textnotfounddebugging

    Args:
        enabled (bool): Whether to enable debugging when a OCR Text is not found.

    """
    with _ctx_settings("textNotFoundDebugging", enabled) as c:
        yield [c]


@contextmanager
def defaultOcrLanguage(language: str) -> None:
    """Allows using defaultOcrLanguage test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-defaultocrlanguage

    Args:
        language (str): string text representing the Language to be used
        for OCR Text search

    """
    with _ctx_settings("defaultOcrLanguage", language) as c:
        yield [c]


@contextmanager
def breakOnFailure(enabled: bool) -> None:
    """Allows using breakOnFailure test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-breakonfailure

    Args:
        enabled (bool): Whether to enable the debugger to stop
        on every failed verification

    """
    with _ctx_settings("breakOnFailure", enabled) as c:
        yield [c]


@contextmanager
def throwOnFailure(enabled: bool) -> None:
    """Allows using throwOnFailure test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-throwonfailure

    Args:
        enabled (bool): Whether to enable to raise a script error
        on every failed verification

    """
    with _ctx_settings("throwOnFailure", enabled) as c:
        yield [c]


@contextmanager
def retryDuration(duration_ms: int) -> None:
    """Allows using retryDuration test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#integer-testsettings-retryduration

    Args:
        duration_ms (int): The duration in milliseconds after which
        the verification fails

    """
    with _ctx_settings("retryDuration", duration_ms) as c:
        yield [c]

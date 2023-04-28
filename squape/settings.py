# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from contextlib import contextmanager

import squish
import test
from squape.internal.exceptions import SquishCapabilityError


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
        test.log(
            f"Setting value of '{setting_name}' setting from {current_value} to {value}"
        )
        setattr(squish.testSettings, setting_name, value)
    except AttributeError:
        raise SquishCapabilityError(
            f"Your Squish version does not support test setting {setting_name}"
        )

    try:
        yield
    except Exception:
        raise
    finally:
        test.log(
            f"Setting value of '{setting_name}' setting from {value} to {current_value}"
        )
        setattr(squish.testSettings, setting_name, current_value)


@contextmanager
def logScreenshotOnPass(enabled: bool = True) -> None:
    """Allows using logScreenshotOnPass test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonpass

    Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on PASS test result. Defaulting to True.

    Example:
        with logScreenshotOnPass():
            # code with verifications
    """
    with _ctx_settings("logScreenshotOnPass", enabled):
        yield


@contextmanager
def logScreenshotOnFail(enabled: bool = True) -> None:
    """Allows using logScreenshotOnFail test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonfail

    Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on FAIL test result. Defaulting to True.

    Example:
        with logScreenshotOnFail():
            # code with verifications
    """

    with _ctx_settings("logScreenshotOnFail", enabled):
        yield


@contextmanager
def logScreenshotOnWarning(enabled: bool = True) -> None:
    """Allows using logScreenshotOnWarning test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-logscreenshotonwarning

     Args:
        enabled (bool): A boolean value indicating whether to enable logging
        of screenshots on warning log entry. Defaulting to True.

    Example:
        with logScreenshotOnWarning():
            # code where warning messages might happen
    """
    with _ctx_settings("logScreenshotOnWarning", enabled):
        yield


@contextmanager
def silentVerifications(enabled: bool = True) -> None:
    """Allows using silentVerifications test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-silentverifications

    Args:
        enabled (bool): Whether silent verifications are enabled. Defaulting to True

    Example:
        with silentVerifications():
            # code with test.vp statements
    """
    with _ctx_settings("silentVerifications", enabled):
        yield


@contextmanager
def imageSearchTolerant(enabled: bool = True) -> None:
    """Allows using imageSearchTolerant test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagesearchtolerant

    Args:
        enabled (bool): Whether image search with tolerance is enabled.
        Defaulting to True.

    Example:
        with imageSearchTolerant(), imageSearchThreshold(95):
            test.imagePresent()

    """
    with _ctx_settings("imageSearchTolerant", enabled):
        yield


@contextmanager
def imageSearchThreshold(threshold: float) -> None:
    """Allows using imageSearchThreshold test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchthreshold

    Args:
        threshold (float): the threshold for image search.

    Example:
        with imageSearchTolerant(), imageSearchThreshold(95):
            test.imagePresent("image.png")
    """
    with _ctx_settings("imageSearchThreshold", threshold):
        yield


@contextmanager
def imageSearchMultiscale(enabled: bool = True) -> None:
    """Allows using imageSearchMultiscale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagesearchmultiscale

    Args:
        enabled (bool): Whether multi-scale image search is enabled. Defaulting to True

    Example:
        with imageSearchMultiscale(), imageSearchMaxScale(150):
            test.imagePresent("image1.png")
            test.imagePresent("image2.png")

    """
    with _ctx_settings("imageSearchMultiscale", enabled):
        yield


@contextmanager
def imageSearchMinScale(min_scale: float) -> None:
    """Allows using imageSearchMinScale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchminscale

    Args:
        min_scale (float): A float value indicating the minimum scale for image search.

    Example:
        with imageSearchMultiscale(), imageSearchMinScale(75):
            test.imagePresent("image1.png")
            test.imagePresent("image2.png")
    """
    with _ctx_settings("imageSearchMinScale", min_scale):
        yield


@contextmanager
def imageSearchMaxScale(max_scale: float) -> None:
    """Allows using imageSearchMaxScale test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#number-testsettings-imagesearchmaxscale

    Args:
        max_scale (float): A float value indicating the maximum scale for image search.

    Example:
        with imageSearchMultiscale(), imageSearchMaxScale(150):
            test.imagePresent("image1.png")
            test.imagePresent("image2.png")
    """
    with _ctx_settings("imageSearchMaxScale", max_scale):
        yield


@contextmanager
def waitForObjectTimeout(timeout_ms: int) -> None:
    """Allows using waitForObjectTimeout test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#integer-testsettings-waitforobjecttimeout

    Args:
        timeout_ms (int): A integer value indicating the timeout in ms.

    Example:
        with waitForObjectTimeout(500):
            waitForObject(names.obj1)
            waitForObject(names.obj2)
    """
    with _ctx_settings("waitForObjectTimeout", timeout_ms):
        yield


@contextmanager
def objectNotFoundDebugging(enabled: bool) -> None:
    """Allows using objectNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-objectnotfounddebugging

    Args:
        enabled (bool): Whether to enable debugging when object is not found.

    Example:
        with objectNotFoundDebugging(False):
            waitForObject(names.obj1)
            waitForObject(names.obj2)
    """
    with _ctx_settings("objectNotFoundDebugging", enabled):
        yield


@contextmanager
def imageNotFoundDebugging(enabled: bool) -> None:
    """Allows using imageNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-imagenotfounddebugging

     Args:
        enabled (bool): Whether to enable debugging when image is not found.

    Example:
        with imageNotFoundDebugging(False):
            waitForImage("image1.png")
            waitForImage("image2.png")
    """
    with _ctx_settings("imageNotFoundDebugging", enabled):
        yield


@contextmanager
def textNotFoundDebugging(enabled: bool) -> None:
    """Allows using textNotFoundDebugging test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-textnotfounddebugging

    Args:
        enabled (bool): Whether to enable debugging when a OCR Text is not found.

    Example:
        with textNotFoundDebugging(False):
            waitForOcrText("Frog")
            waitForOcrText("Alpaca")
    """
    with _ctx_settings("textNotFoundDebugging", enabled):
        yield


@contextmanager
def defaultOcrLanguage(language: str) -> None:
    """Allows using defaultOcrLanguage test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-defaultocrlanguage

    Args:
        language (str): string text representing the Language to be used
        for OCR Text search

    Example:
        with defaultOcrLanguage("Polish"):
            waitForOcrText("Dom")
            waitForOcrText("Miasto")
    """
    with _ctx_settings("defaultOcrLanguage", language):
        yield


@contextmanager
def breakOnFailure(enabled: bool = True) -> None:
    """Allows using breakOnFailure test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-breakonfailure

    Args:
        enabled (bool): Whether to enable the debugger to stop
        on every failed verification

    Example:
        with breakOnFailure():
            # code with verifications
    """
    with _ctx_settings("breakOnFailure", enabled):
        yield


@contextmanager
def throwOnFailure(enabled: bool) -> None:
    """Allows using throwOnFailure test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#bool-testsettings-throwonfailure

    Args:
        enabled (bool): Whether to enable to raise a script error
        on every failed verification

    Example:
    with throwOnFailure():
        # code with verifications

    """
    with _ctx_settings("throwOnFailure", enabled):
        yield


@contextmanager
def retryDuration(duration_ms: int) -> None:
    """Allows using retryDuration test setting as context managers.
    https://doc.qt.io/squish/squish-api.html#integer-testsettings-retryduration

    Args:
        duration_ms (int): The duration in milliseconds after which
        the verification fails

    Example:
        with retryDuration(5000):
            test.vp("VP1")

    """
    with _ctx_settings("retryDuration", duration_ms):
        yield

# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import test
from contextlib import contextmanager


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

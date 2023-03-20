# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import test

import squish


def vph_property(
    object_name: any, property_name: str, expected_value: any, msg: str
) -> None:
    """The function verifies the property of the given object.
    It highlights the verified object to make it standing out.

    Args:
        object_name (any): symbolic name, real name, or object reference
        property_name (str): name of the property to verify
        expected_value (any): expected value of the verified property
        msg (str): verification message
    Returns:
        None
    """

    obj = squish.waitForObjectExists(object_name)
    property_value = getattr(obj, property_name)
    squish.highlightObject(obj, 200, False)
    test.compare(property_value, expected_value, msg)
    squish.snooze(0.2)

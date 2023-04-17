# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import squish
import test


def vph_property(
    object_name: any, property_name: str, expected_value: any, msg: str
) -> bool:
    """ "Highlights the object then verifies its property.
    The object remains highlighted during verification to make it easier to identify
    on potential screenshots.

    Args:
        object_name (any): symbolic name, real name, or object reference
        property_name (str): name of the property to verify
        expected_value (any): expected value of the verified property
        msg (str): verification message
    Returns:
        bool: True if verification is positive, False otherwise
    """

    obj = squish.waitForObjectExists(object_name)
    property_value = getattr(obj, property_name)
    squish.highlightObject(obj, 200, False)
    result = test.compare(property_value, expected_value, msg)
    squish.snooze(0.2)
    return result
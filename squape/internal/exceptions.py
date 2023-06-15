# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.


class SquishCapabilityError(Exception):
    """
    Indicate that squape functionality cannot be used
    because it is not supported by Squish version in use.
    """

    def __init__(self, message):
        super().__init__(message)


class SquishserverError(Exception):
    """
    Indicate that squishserver was unable to complete the operation.
    """

    def __init__(self, message):
        super().__init__(message)


class EnvironmentError(Exception):
    """
    Indicate that the runtime environment is not set correctly.
    Example would be unset environment variable.
    """

    def __init__(self, message):
        super().__init__(message)

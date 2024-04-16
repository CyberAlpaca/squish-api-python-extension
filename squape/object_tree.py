# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import math
import time
import types

try:
    import squish
except ImportError:
    import squishtest as squish

import object
from settings import objectNotFoundDebugging


def children(object_or_name: any, selector: dict) -> tuple:
    """
    Finds direct children of the given object.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

        selector (dict): The selector is a dictionary of key-value pairs,
            where a key is a property of an object, and value is expected value.
            An object will pass verification
            if the object's property value matches the selector value.
            Selectors may include functions.
            The passed functions must accept exactly one argument.

    Returns:
        Children objects that met the selector criteria.

    Examples:
        ```python
        children(object_or_name, {'type' : QToolButton, 'height': 50})
        children(object_or_name, {'type' : 'Button', 'visible' : True})
        children(object_or_name, {'type' : 'QToolButton', 'height' : lambda x: x > 25})

        def height_filter_function(height: int) -> bool:
            return height > 30 and height < 120
        children(
            object_or_name,
            {'type' : 'QToolButton', 'height' : height_filter_function}
        )
        ```
    """
    object_reference = _get_object_reference(object_or_name)
    children = object.children(object_reference)
    return tuple(filter(lambda x: _is_matching(x, selector), children))


def find(object_or_name: any, selector: dict = None, max_depth: int = None) -> tuple:
    """
    Finds descendants of the given object.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

        selector (dict, optional): The selector is a dictionary of key-value pairs,
            where a key is a property of an object, and value is expected value.
            An object will pass verification
            if the object's property value matches the selector value.
            Selectors may include functions.
            The passed functions must accept exactly one argument.
            Defaults to {}, which means all objects pass the verification.

        max_depth (int): defines maximum depth in the object structure that should be
            while looking for children.
            Defaults to None, which mean there is no depth limit.

    Returns:
        Descendants of the given object that met the selector criteria.

    Examples:
        ```python
        find(object_or_name)
        find(object_or_name, {'type' : 'ToolBar'})
        find(object_or_name, max_depth=5)
        find(object_or_name, {'visible' : True}, max_depth=3)
        find(
            object_or_name,
            {'type' : 'QToolButton', 'height' : lambda x: x > 25},
            max_depth=5
        )

        def height_filter_function(height: int) -> bool:
            return height > 30 and height < 120
        find(
            object_or_name,
            {'type' : 'QToolButton', 'height' : height_filter_function}
        )
        ```
    """
    if max_depth is None:
        max_depth = math.inf
    if max_depth <= 0:
        return ()
    if selector is None:
        selector = {}

    object_reference = _get_object_reference(object_or_name)
    children = ()

    for child in object.children(object_reference):
        if _is_matching(child, selector):
            children += (child,)
        children += find(child, selector, max_depth - 1)

    return children


def find_ancestor(object_or_name: any, selector: dict):
    """
    Find the first object's ancestor that matches the selector.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

        selector (dict): The selector is a dictionary of key-value pairs,
            where a key is a property of an object, and value is expected value.
            An object will pass verification
            if the object's property value matches the selector value.
            Selectors may include functions.
            The passed functions must accept exactly one argument.

    Returns:
        (Squish object / None): The ancestor object that matches the selector.

    Examples:
        ```python
        find_ancestor(object_or_name)
        find_ancestor(object_or_name, {'type' : 'MyContainerType'})
        find_ancestor(
            object_or_name,
            {'type' : 'QToolButton', 'height' : lambda x: x > 25}
        )

        def height_filter_function(height: int) -> bool:
            return height > 30 and height < 120
        find_ancestor(
            object_or_name,
            {'type' : 'QToolButton', 'height' : height_filter_function}
        )
        ```
    """
    object_reference = _get_object_reference(object_or_name)
    parent = object.parent(object_reference)

    if parent is None:
        return None

    if _is_matching(object.parent(object_reference), selector):
        return parent

    return find_ancestor(parent, selector)


def siblings(object_or_name: any, selector: dict = None) -> tuple:
    """
    Find the object's siblings.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

        selector (dict, optional): The selector is a dictionary of key-value pairs,
            where a key is a property of an object, and value is expected value.
            An object will pass verification
            if the object's property value matches the selector value.
            Selectors may include functions.
            The passed functions must accept exactly one argument.
            Defaults to {}, which means all objects pass the verification.

    Returns:
        Siblings of the given object that met the selector criteria.

    Examples:
        ```python
        siblings(object)
        siblings(object, {'enabled' : True})
        siblings(object_or_name, {'type' : 'QToolButton', 'height' : lambda x: x > 25})

        def height_filter_function(height: int) -> bool:
            return height > 30 and height < 120
        siblings(
            object_or_name,
            {'type' : 'QToolButton', 'height' : height_filter_function}
        )
        ```
    """
    if selector is None:
        selector = {}
    object_reference = _get_object_reference(object_or_name)
    parent = object.parent(object_reference)

    if parent is None:
        return None
    else:
        siblings = list(object.children(parent))
        siblings.remove(object_reference)
        return tuple(filter(lambda x: _is_matching(x, selector), siblings))


def _is_matching(object_or_name: any, selector: dict) -> bool:
    """
    Checks if the properties of the given object match the provided selector.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

        selector (dict, optional): The selector is a dictionary of key-value pairs,
            where a key is a property of an object, and value is expected value.
            An object will pass verification
            if the object's property value matches the selector value.
            Selectors may include functions.
            The passed functions must accept exactly one argument.
            Defaults to {}, which means all objects pass the verification.

    Returns:
        True if the object matches the selector, False otherwise.
    """
    if selector == {}:
        return True

    object_reference = _get_object_reference(object_or_name)

    for key, expected_value in selector.items():
        if key == "type":
            # Type verification
            actual_type = squish.className(object_reference).rsplit("_QMLTYPE_", 1)[0]
            if actual_type != expected_value:
                return False
        elif not hasattr(object_reference, key):
            # Object does not have given attribute
            return False
        else:
            # object has given attribute
            attr = getattr(object_reference, key)
            if isinstance(expected_value, types.FunctionType):
                # The key is a lambda function
                lambda_function = expected_value
                lambda_result = lambda_function(attr)
                if not isinstance(lambda_result, bool):
                    raise RuntimeError(
                        f"The lambda function assossiated with a key '{key}' \
                        returned non-boolean result: \
                        {lambda_result} ({type(lambda_result)})"
                    )
                if not lambda_result:
                    return False

            elif attr != expected_value:
                return False
    return True


def _get_object_reference(object_or_name: any) -> any:
    """
    Get the object reference for the given symbolic, real names or object reference.

    Args:
        object_or_name (any): symbolic name, real name, or object reference.

    Returns:
        (Squish object): Object reference from the given object_or_name.
    """
    if isinstance(object_or_name, dict):
        # Symbolic name
        return squish.waitForObjectExists(object_or_name)
    return object_or_name


@objectNotFoundDebugging(False)
def _wait_for_any_object(
    lookup_function, object_names: list, timeout: int, retry_delay: float
):
    lookup_errors = set()
    start_time = time.time()

    while True:
        for obj_name in object_names:
            try:
                return lookup_function(obj_name, 0)

            except LookupError as e:
                lookup_errors.add(str(e))

        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            break

        squish.snooze(retry_delay)

    raise LookupError(f"Objects not found: {lookup_errors}")


def wait_for_any_object(
    object_names: list,
    timeout=squish.testSettings.waitForObjectTimeout / 1000,
    retry_delay: float = 0.5,
):
    """
    Wait for any accessible object from the provided object names list to become
    available (exists, visible, enabled) within a specified timeout.

    Args:
        object_names (list): A list of names of the objects to wait for.
        timeout (int, optional): The maximum time in seconds to wait for
            any object to become available.
            Defaults to squish.testSettings.waitForObjectTimeout/1000.
        retry_delay (float, optional): The time in seconds to wait before
        retrying the Squish lookup function. Defaults to 0.5.

    Returns:
        object: The first object that becomes available within the specified timeout.

    Raises:
        LookupError: If none of the objects become available within
            the specified timeout.
    """
    return _wait_for_any_object(
        squish.waitForObject, object_names, timeout, retry_delay=retry_delay
    )


def wait_for_any_object_exists(
    object_names: list,
    timeout=squish.testSettings.waitForObjectTimeout / 1000,
    retry_delay: float = 0.5,
):
    """
    Wait for object from the provided object names list to become
    available (exists) within a specified timeout.

    Args:
        object_names (list): A list of names of the objects to wait for.
        timeout (int, optional): The maximum time in seconds to wait for
            any object to become available.
            Defaults to squish.testSettings.waitForObjectTimeout/1000.
        retry_delay (float, optional): The time in seconds to wait before
            retrying the Squish lookup function. Defaults to 0.5.

    Returns:
        object: The first object that becomes available within the specified timeout.

    Raises:
        LookupError: If none of the objects become available within
            the specified timeout.
    """
    return _wait_for_any_object(
        squish.waitForObjectExists, object_names, timeout, retry_delay=retry_delay
    )

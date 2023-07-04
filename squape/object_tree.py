# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import math

import object
import squish


def children(object_name: any, selector: dict = None) -> tuple:
    """Filter the direct children of the specified object by the specified selector

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: children objects that met the selector criteria

    Examples:
        >>> children(object_name, {'type' : Button, 'visible' : True})
    """
    if selector is None:
        selector = {}
    object_reference = _get_object_reference(object_name)
    children = object.children(object_reference)
    return tuple(filter(lambda x: _is_matching(x, selector), children))


def find(object_name: any, selector: dict = None, max_depth: int = None) -> tuple:
    """Recursively filter all the children of the specified object
    by the specified selector

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.
        max_depth (int): defines maximum depth in the object structure that should be
        while looking for children.
        Defaults to None, which mean there is no depth limit.

    Returns:
        tuple: the result of search among the object tree.

    Examples:
        ```
        find(object)
        find(object, {'type' : ToolBar})
        find(object, max_depth=5)
        find(object, {'visible' : True}, max_depth=3)
        ```
    """
    if max_depth is None:
        max_depth = math.inf
    if max_depth <= 0:
        return ()
    if selector is None:
        selector = {}

    object_reference = _get_object_reference(object_name)
    children = ()

    for child in object.children(object_reference):
        if _is_matching(child, selector):
            children += (child,)
        children += find(child, selector, max_depth - 1)

    return children


def find_ancestor(object_name: any, selector: dict = None):
    """Find the first object's ancestor that matches the selector.

    Args:
        object_name (any): symbolic name, real name, or object reference to the ancestor
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        Squish object / None: The ancestor object that matches the selector.
        None if such an ancestor does not exist.

    Examples:
        >>> find_ancestor(object_name : any, {'type' : 'MyContainerType'})
    """
    if selector is None:
        selector = {}

    object_reference = _get_object_reference(object_name)
    parent = object.parent(object_reference)

    if parent is None:
        return None

    if _is_matching(object.parent(object_reference), selector):
        return parent

    return find_ancestor(parent, selector)


def siblings(object_name: any, selector: dict = None):
    """Find all the siblings (direct children of the parent) objects
    for a given object, that match the selector.

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: the result of search among the object tree.

    Examples:
        ```
        siblings(object)
        siblings(object, {'enabled' : True})
        ```
    """
    if selector is None:
        selector = {}
    object_reference = _get_object_reference(object_name)
    parent = object.parent(object_reference)

    if parent is None:
        return None
    else:
        siblings = list(object.children(parent))
        siblings.remove(object_reference)
        return tuple(filter(lambda x: _is_matching(x, selector), siblings))


def _is_matching(object_name: any, selector: dict) -> bool:
    """Checks if the properties of the given object match the provided selector.

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        bool: True if object matches selector, False otherwise.
    """
    if selector == {}:
        return True

    object_reference = _get_object_reference(object_name)

    for key, expected_value in selector.items():
        if key == "type":
            if squish.className(object_reference) != expected_value:
                return False
        elif (
            not hasattr(object_reference, key)
            or getattr(object_reference, key) != expected_value
        ):
            return False
    return True


def _get_object_reference(object_name: any) -> any:
    """Get the object reference for the given symbolic, real names or object reference

    Args:
        object_name (any): symbolic name, real name, or object reference

    Returns:
        object_reference: Object reference from the given object_name
    """
    if isinstance(object_name, dict):
        # Symbolic name
        return squish.waitForObjectExists(object_name)
    return object_name

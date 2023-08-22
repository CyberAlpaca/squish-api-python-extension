# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import object


def children(obj, selector: dict = None) -> tuple:
    """Filter the direct children of the specified object by the specified selector

    Args:
        obj (Squish object): A base object for this verification.
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: the result of search among the object tree.
    """
    if selector is None:
        selector = {}
    children = object.children(obj)
    return tuple(filter(lambda x: _filter_by_selector(x, selector), children))


def find(obj, selector: dict = None, _depth=0) -> tuple:
    """Recursively filter all the underlaying children
    of the specified object  by the specified selector

    Args:
        obj (Squish object): A base object for this verification.
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: the result of search among the object tree.
    """
    if selector is None:
        selector = {}
    children = list(object.children(obj))

    for child in children:
        children.extend(
            [
                find(grandchild, _depth=_depth + 1)
                for grandchild in object.children(child)
            ]
        )

    if _depth == 0:
        filtered_children = filter(lambda x: _filter_by_selector(x, selector), children)
        return tuple(filtered_children)
    else:
        return children


def find_parent(obj, selector: dict = None):
    """Find the first parent that matches the selector,
    among all the parent objects up to the root.

    Args:
        obj (Squish object): A base object for this verification.
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        Squish object / None: The parent object that matches the selector.
        None if such a parent does not exist.
    """
    if selector is None:
        selector = {}
    if object.parent(obj) is None:
        return None
    elif _filter_by_selector(object.parent(obj), selector):
        return object.parent(obj)
    else:
        return find_parent(object.parent(obj), selector)


def siblings(obj, selector: dict = None):
    """Find all the siblings (direct children of the parent) object
    for a given object, that match the selector.

    Args:
        obj (Squish object): A base object for this verification.
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: the result of search among the object tree.
    """
    if selector is None:
        selector = {}
    parent = object.parent(obj)

    if parent is None:
        return None
    else:
        return tuple(filter(lambda x: _filter_by_selector(x, object.children(parent))))


def _filter_by_selector(obj, selector: dict) -> bool:
    """Verifies if the given object properties match with the given selector.

    Args:
        obj (Squish object): A base object for this verification.
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        bool: True if object passes the verification, False otherwise.
    """
    if selector == {}:
        return True
    else:
        for key, expected_value in selector.items():
            if not hasattr(obj, key) or getattr(obj, key) != expected_value:
                return False
            return True

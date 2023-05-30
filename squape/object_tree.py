# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Cyber Alpaca
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import math

import object

import squish


def children(object_name : any, selector: dict = None) -> tuple:
    """Filter the direct children of the specified object by the specified selector

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: children objects that met the selector criteria

    Examples:
        children(object_name, {'type' : Button, 'visible' : True})
    """
    if selector is None:
        selector = {}
    children = object.children(object_name)
    return tuple(filter(lambda x: _filter_by_selector(x, selector), children))


def find(object_name : any, selector: dict = None, max_depth=None, _depth=0) -> tuple:
    """Recursively filter all the underlaying children
    of the specified object  by the specified selector

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        tuple: the result of search among the object tree.

    Examples:
        find(object)
        find(object, {'type' : ToolBar})
        find(object, max_depth=5)
        find(object, {'visible' : True}, max_depth=3)
    """
    if max_depth is None:
        max_depth = math.inf
    if _depth >= max_depth:
        return []
    if selector is None:
        selector = {}
    children = list(object.children(object_name))
    children_count = len(children)

    for index, child in enumerate(children):
        if index == children_count:
            break
        children.extend(find(child, max_depth=max_depth, _depth=_depth + 1))

    if _depth == 0:
        filtered_children = filter(lambda x: _filter_by_selector(x, selector), children)
        return tuple(filtered_children)
    else:
        return children


def find_parent(object_name : any, selector: dict = None):
    """Find the first parent that matches the selector,
    among all the parent objects up to the root.

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        Squish object / None: The parent object that matches the selector.
        None if such a parent does not exist.

    Examples:
        find_parent(object_name : any, {'type' : 'MyContainerType'})
    """
    if selector is None:
        selector = {}

    if object.parent(object_name) is None:
        return None
    
    if _filter_by_selector(object.parent(object_name), selector):
        return object.parent(object_name)
        
    return find_parent(object.parent(object_name), selector)


def siblings(object_name : any, selector: dict = None):
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
        siblings(object)
        siblings(object, {'enabled' : True})
    """
    if selector is None:
        selector = {}
    parent = object.parent(object_name)

    if parent is None:
        return None
    else:
        siblings = list(object.children(parent))
        siblings.remove(object_name)
        return tuple(filter(lambda x: _filter_by_selector(x, selector), siblings))


def _filter_by_selector(object_name : any, selector: dict) -> bool:
    """Verifies if the given object properties match with the given selector.

    Args:
        object_name (any): symbolic name, real name, or object reference to the parent
        selector (dict, optional): The selector is a dictionary of properties,
        that must match for objects to be included into the result.
        Defaults to {}, which means all objects pass the verification.

    Returns:
        bool: True if object passes the verification, False otherwise.
    """
    if selector == {}:
        return True

    for key, expected_value in selector.items():
        if key == "type":
            if squish.className(object_name) != expected_value:
                return False
        elif not hasattr(object_name, key) or getattr(object_name, key) != expected_value:
            return False
    return True

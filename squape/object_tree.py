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
    object_reference = _get_object_reference(object_name)
    children = object.children(object_reference)
    return tuple(filter(lambda x: _is_matches_selector(x, selector), children))


def find(object_name : any, selector: dict = None, max_depth=None) -> tuple:
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
    if max_depth < 0:
        return []
    if selector is None:
        selector = {}
    
    object_reference = _get_object_reference(object_name)
    children = list(object.children(object_reference))
    children_count = len(children)

    for index, child in enumerate(children):
        if index == children_count:
            break
        children.extend(find(child, max_depth=max_depth-1))

    if max_depth == 0:
        filtered_children = filter(lambda x: _is_matches_selector(x, selector), children)
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

    object_reference = _get_object_reference(object_name)

    if object.parent(object_reference) is None:
        return None
    
    if _is_matches_selector(object.parent(object_reference), selector):
        return object.parent(object_reference)
        
    return find_parent(object.parent(object_reference), selector)


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
    object_reference = _get_object_reference(object_name)
    parent = object.parent(object_reference)

    if parent is None:
        return None
    else:
        siblings = list(object.children(parent))
        siblings.remove(object_reference)
        return tuple(filter(lambda x: _is_matches_selector(x, selector), siblings))


def _is_matches_selector(object_name : any, selector: dict) -> bool:
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

    object_reference = _get_object_reference(object_name)

    for key, expected_value in selector.items():
        if key == "type":
            if squish.className(object_reference) != expected_value:
                return False
        elif not hasattr(object_reference, key) or getattr(object_reference, key) != expected_value:
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
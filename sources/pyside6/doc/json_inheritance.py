# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

import json
import os
import sys
from pathlib import Path


"""Helpers for determining base classes by reading a JSON
    file written by shiboken's doc generator."""


TEST_DRIVER_USAGE = """Usage: json_inheritance.py class_name json_file

Example:
python json_inheritance.py PySide6.QtWidgets.QWizard ~/inheritance.json
"""


ENV_VAR = "INHERITANCE_FILE"


def strip_module(class_name):
    return class_name[8:] if class_name.startswith("PySide") else class_name


def get_inheritance_entries_recursion(json_dict, class_name):
    """Get all edges of the inheritance graph of class_name."""
    result = []
    bases_entry = json_dict.get(class_name)
    bases = bases_entry if bases_entry else []
    node_name = strip_module(class_name)
    base_list = [strip_module(b) for b in bases]
    result.append((node_name, class_name, base_list))
    for b in bases:
        nested_bases = get_inheritance_entries_recursion(json_dict, b)
        if nested_bases:
            result.extend(nested_bases)
    return result


def _get_inheritance_entries_from_json(json_file, class_names):
    """Get all edges of the inheritance graph of class_name
       from the JSON file generated by shiboken."""
    result = []
    try:
        with Path(json_file).open("r") as f:
            json_dict = json.load(f)
            for c in class_names:
                result.extend(get_inheritance_entries_recursion(json_dict, c))
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error reading {json_file}: {e}")
        raise
    return result


def is_inheritance_from_json_enabled():
    return os.environ.get(ENV_VAR)


def get_inheritance_entries_from_json(class_names):
    json_file = os.environ[ENV_VAR]
    return _get_inheritance_entries_from_json(json_file, class_names)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(TEST_DRIVER_USAGE)
        sys.exit(-1)
    class_name = sys.argv[1]
    json_file = sys.argv[2]
    for e in _get_inheritance_entries_from_json(json_file, [class_name]):
        print(e)

#!/usr/bin/env python
"""
This script tests all valid examples and alerts for badness

"""

import os
import pathlib
import json
from jsonschema import validate


def test_alerts():
    """Test that all alerts are valid json"""

    fullFolder = os.path.join(pathlib.Path(__file__).parent.absolute(), "alerts")

    files = [f for f in os.listdir(fullFolder) if os.path.isfile(os.path.join(fullFolder, f))]
    for file in files:
        if file == ".gitignore":
            break

        fileAbs = os.path.join(fullFolder, file)
        print("Checking alerts/{0}".format(file))
        checkFile(fileAbs)

def test_examples():
    """Test that all example alerts are valid json"""

    fullFolder = os.path.join(pathlib.Path(__file__).parent.absolute(), "examples")

    files = [f for f in os.listdir(fullFolder) if os.path.isfile(os.path.join(fullFolder, f))]
    for file in files:
        # Ignore bad examples
        if "BAD" in file:
            break

        fileAbs = os.path.join(fullFolder, file)
        print("Checking alerts/{0}".format(file))
        checkFile(fileAbs)

def checkFile(fileAbs):
    data = None

    # check is json
    assert fileAbs.endswith(".json")
    with open(fileAbs) as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            print("Bad json")
            assert False

    # check schema is valid
    with open("alert.schema.json") as alertSchemaFile:
        try:
            validate(instance=data, schema=json.load(alertSchemaFile))
        except json.decoder.JSONDecodeError:
            print("Bad schema")
            assert False
    
    # check fields
    assert "dateRaised" in data
    try:
        tmp = int(data["dateRaised"])
    except (ValueError, TypeError):
        print("Bad field: dateRaised")
        assert False

    assert "affectedFirmware" in data and isinstance(data["affectedFirmware"], list) and len(data["affectedFirmware"]) > 0
    assert "hardwareLimited" in data and isinstance(data["hardwareLimited"], list)
    assert "description" in data and isinstance(data["description"], str)
    assert "mitigation" in data and isinstance(data["mitigation"], str)
    assert "fixCommit" in data and isinstance(data["fixCommit"], list)
    assert "dateResolved" in data
    if data["dateResolved"] != None:
        try:
            tmp = int(data["dateResolved"])
        except (ValueError, TypeError):
            print("Bad field: dateResolved")
            assert False
    assert "linkedIssue" in data and (data["linkedIssue"] == None or isinstance(data["linkedIssue"], str))
    assert "linkedInfo" in data and isinstance(data["linkedInfo"], list)
    assert "linkedPR" in data and (data["linkedPR"] == None or isinstance(data["linkedPR"], str))
    assert "versionFrom" in data and isinstance(data["versionFrom"], dict)
    assert "versionFixed" in data and isinstance(data["versionFixed"], dict)
    assert "criticality" in data and isinstance(data["criticality"], int)


#!/usr/bin/env python
"""
This script parses all files in the top level active, archive and examples folders for valid json

"""

import os
import pathlib
import json

if __name__ == "__main__":
    folders = ["alerts", "examples"]
    numprocessed = 0

    for folder in folders:
        fullFolder = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", folder)

        files = [f for f in os.listdir(fullFolder) if os.path.isfile(os.path.join(fullFolder, f))]
        for file in files:
            fileAbs = os.path.join(fullFolder, file)
            print("Checking {1}/{0}".format(file, folder))
            isOK = True
            data = None

            # check is json
            if not fileAbs.endswith(".json"):
                print("Bad file extension")
                isOK = False
            else:
                with open(fileAbs) as json_file:
                    try:
                        data = json.load(json_file)
                    except json.decoder.JSONDecodeError:
                        print("Bad json")
                        isOK = False

            # check fields
            if isOK and data:
                if not "dateRaised" in data:
                    print("Bad field: dateRaised")
                    isOK = False
                else:
                    try:
                        tmp = int(data["dateRaised"])
                    except (ValueError, TypeError):
                        print("Bad field: dateRaised")
                        isOK = False

                if not ("affectedFirmware" in data and isinstance(data["affectedFirmware"], list) and len(data["affectedFirmware"]) > 0):
                    print("Bad field: affectedFirmware")
                    isOK = False 
                
                if not ("hardwareLimited" in data and isinstance(data["hardwareLimited"], list)):
                    print("Bad field: hardwareLimited")
                    isOK = False

                if not ("description" in data and isinstance(data["description"], str)):
                    print("Bad field: description")
                    isOK = False

                if not ("mitigation" in data and isinstance(data["mitigation"], str)):
                    print("Bad field: mitigation")
                    isOK = False

                if not ("fixCommit" in data and isinstance(data["fixCommit"], list)):
                    print("Bad field: fixCommit")
                    isOK = False

                if not "dateResolved" in data:
                    print("Bad field: dateResolved")
                    isOK = False
                elif data["dateResolved"] != None:
                    try:
                        tmp = int(data["dateResolved"])
                    except (ValueError, TypeError):
                        print("Bad field: dateResolved")
                        isOK = False

                if not ("linkedIssue" in data and (data["linkedIssue"] == None or isinstance(data["linkedIssue"], str))):
                    print("Bad field: linkedIssue")
                    isOK = False

                if not ("linkedInfo" in data and isinstance(data["linkedInfo"], list)):
                    print("Bad field: linkedInfo")
                    isOK = False

                if not ("linkedPR" in data and (data["linkedPR"] == None or isinstance(data["linkedPR"], str))):
                    print("Bad field: linkedPR")
                    isOK = False

                if not ("versionFrom" in data and isinstance(data["versionFrom"], dict)):
                    print("Bad field: versionFrom")
                    isOK = False

                if not ("versionFixed" in data and isinstance(data["versionFixed"], dict)):
                    print("Bad field: versionFixed")
                    isOK = False

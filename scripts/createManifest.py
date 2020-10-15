#!/usr/bin/env python
"""
This script creates a manifest of user alerts

"""

import os
import pathlib
import json
import argparse
import subprocess

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Manifest generator for ArduPilot user alerts')

    # Add the arguments
    parser.add_argument('-outputFile', action="store", dest="output", default="examplemanifest", help="Output manifest file")
    parser.add_argument('-inputFolder', action="store", dest="input", default="examples", help="Input folder of alerts")
    parser.add_argument('-format', action="store", dest="format", choices=['json', 'js'], default="json", help="Output format")
    
    args = parser.parse_args()

    inFolder = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", args.input)
    OutFile = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "output", args.output)
    manifestData = {}
    numAlerts = 0

    # create output dir if required
    pathlib.Path(os.path.dirname(OutFile)).mkdir(parents=True, exist_ok=True)

    files = [f for f in os.listdir(inFolder) if os.path.isfile(os.path.join(inFolder, f))]
    for file in files:
        fileAbs = os.path.join(inFolder, file)
        print("Checking {0}".format(file))
        data = None

        if fileAbs.endswith(".json") and "BAD" not in file:
            # get last modified date
            dateMod = subprocess.check_output(["git", "log", "-1", "--date=iso-strict", "--pretty=%cI", fileAbs]).decode("utf-8").strip()
            with open(fileAbs) as json_file:
                try:
                    data = json.load(json_file)
                    data["lastmodified"] = dateMod
                    manifestData[file] = data
                    print("Included {0}".format(file))
                    numAlerts += 1
                except json.decoder.JSONDecodeError:
                    print("Bad json")
    # and save
    if args.format == "json":
        with open(OutFile + ".json", 'w') as outfileHandle:
            json.dump(manifestData, outfileHandle)
        print("Saved {0} user alerts to {1}".format(numAlerts, OutFile + ".json"))
    else:
        # and a js file
        with open(OutFile + ".js", 'w') as outfileHandle:
            outfileHandle.write("var userAlerts = " + json.dumps(manifestData) + ";")
        print("Saved {0} user alerts to {1}".format(numAlerts, OutFile + ".js"))


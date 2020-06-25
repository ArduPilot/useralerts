#!/usr/bin/env python
"""
This script creates a manifest of user alerts

"""

import os
import pathlib
import json
import argparse

if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description='Manifest generator for ArduPilot user alerts')

    # Add the arguments
    parser.add_argument('-outputFile', action="store", dest="output", default="exampleManifest.json", help="Output manifest file")
    parser.add_argument('-inputFolder', action="store", dest="input", default="examples", help="Input folder of alerts")
    
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
            with open(fileAbs) as json_file:
                try:
                    data = json.load(json_file)
                    manifestData[file] = data
                    print("Included {0}".format(file))
                    numAlerts += 1
                except json.decoder.JSONDecodeError:
                    print("Bad json")
    # and save
    with open(OutFile, 'w') as outfileHandle:
        json.dump(manifestData, outfileHandle)
    print("Saved {0} user alerts to {1}".format(numAlerts, OutFile))


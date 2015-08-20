#!/usr/bin/env python3

__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath('src'))

import IntelProcessor
import Util
import time

def main(argv):
    if (len(argv) <= 0):
        Util.printErr("You have not specified any json filename.")
        Util.printErr("Write something like this: python3 formatProcessor.py <input filename> [output filename]")
        return

    Util.printProcess('Reading JSON')
    jsonData = Util.readJSONFile(argv[0])
    print(jsonData['count'], 'data will be processed.')

    fileOut = None
    if len(argv) > 1:
        fileOut = argv[1]
    else:
        fileOut = input('Save CSV filename: ')

    Util.printProcess('Converting to CSV...')

    startTime = time.time()
    IntelProcessor.mapToCSV(jsonData, fileOut)
    print('Success! {:f} secs'.format(time.time() - startTime))

main(sys.argv[1:])
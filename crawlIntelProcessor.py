#!/usr/bin/env python3

__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath('src'))

import CrawlUtil
import json
import re
import requests
import time
import threading
from queue import Queue
from pprint import pprint
import copy

PROCESSOR_API_URL = "https://www.kimonolabs.com/api/cd7sg4yq?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN"
PROCESSOR_EXPECTED_LIMIT = 100000

def mergeResult(urls):
    s = requests.Session()
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))

    responses = []
    for url in urls:
        print("[PROCESSING] ", url)
        dat = CrawlUtil.getJSON(s, url)
        if dat['results'] == {}:
            break
        responses.append(dat)

    merged = {}
    for response in responses:
        merged = mergeDict(merged, response)

    return merged

def mergeDict(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergeDict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key] = a[key] + b[key]
            elif a[key] != b[key]:
                a[key] = b[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def process(phoneUrl, num, numTotal):
    startTime = time.time()

    s = requests.Session()
    s.mount("http://", requests.adapters.HTTPAdapter(max_retries=10))
    s.mount("https://", requests.adapters.HTTPAdapter(max_retries=10))

    phoneAPIUrl = "https://www.kimonolabs.com/api/7ltn7gno?apikey=b8BQTunaAccOVZAG9lpyTg1HLy4hkKXN&kimmodify=1"

    resp = CrawlUtil.postJSON('https://ws.kimonolabs.com/ws/updateapi/', {'apiid': '7ltn7gno', 'updateObj': {'targeturl' : phoneUrl}})
    if resp['success']:
        resp = CrawlUtil.postJSON('https://ws.kimonolabs.com/ws/startcrawl/', {'apiid': '7ltn7gno'})
        if resp['success']:
            resp = CrawlUtil.getJSON(s, 'https://ws.kimonolabs.com/ws/crawlstats/?apiid=7ltn7gno')
            while (resp['isCrawling'] != False):
                var = None
                resp = CrawlUtil.getJSON(s, 'https://ws.kimonolabs.com/ws/crawlstats/?apiid=7ltn7gno')

            phoneJson = CrawlUtil.getJSON(s, phoneAPIUrl)
            phoneResult = phoneJson['results']

            deviceName = phoneResult['main']['device_name']

            if not os.path.exists('results'):
                os.makedirs('results')

            f = open('results/' + deviceName.replace("/", "-", 100) + '.json', 'w')
            res = json.dump(phoneResult, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()

            print('[PROCESSED] {:s} ({:d}/{:d}) in {:f} secs'.format(deviceName, num, numTotal, (time.time() - startTime)))

def reformatRawData(r):
    arrData = []
    for dataTitle in r['results']['main']:
        obj = {}
        obj['Name'] = re.sub(r'\n', '', dataTitle['title'])
        for dataContent in r['results']['data']:
            if (dataTitle['url'] == dataContent['url']):
                if isinstance(dataContent['info'], str):
                    obj[dataContent['category1']] = dataContent['info']
                else:
                    obj[dataContent['category1']] = dataContent['info']['text']

        arrData.append(obj)

    r['results'] = arrData
    r['count'] = len(r['results'])
    return r

def main(argv):
    merged = None
    if ('-p' in argv):
        urls = []
        offset = 0

        while offset < PROCESSOR_EXPECTED_LIMIT:
            urls.append(PROCESSOR_API_URL + "&kimoffset=" + str(offset))
            offset = offset + 2500

        merged = mergeResult(urls)

        f = open('processors/' + 'raw-data.json', 'w')
        f.write(json.dumps(merged, indent=4))
        f.close()
    else:
        f = open('processors/' + 'raw-data.json', 'r')
        merged = json.load(f)

    reformatted = reformatRawData(merged)

    f = open('processors/' + 'formatted-data.json', 'w')
    f.write(json.dumps(reformatted, indent=4))
    f.close()

main(sys.argv[1:])

__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'util')))

import re
import Util

def createIndexMap():
    indexMap = []
    indexMap.append('name_300')
    indexMap.append('description')
    indexMap.append('release_date')
    indexMap.append('general_brand')
    indexMap.append('general_series')
    indexMap.append('general_socket-type')
    indexMap.append('processor_core')
    indexMap.append('processor_threads')
    indexMap.append('processor_clock-speed')
    indexMap.append('processor_cache')
    indexMap.append('processor_lithography')
    indexMap.append('processor_max-thermal-design-power-tdp')
    indexMap.append('memory_max-size')
    indexMap.append('memory_type')
    indexMap.append('memory_speed')
    indexMap.append('memory_channels')
    indexMap.append('graphics_processor-graphics')
    indexMap.append('graphics_base-frequency')
    indexMap.append('graphics_max-dynamic-frequency')
    indexMap.append('expansion_pci-express-revision')
    indexMap.append('identifier')
    indexMap.append('picture')
    indexMap.append('action')
    return indexMap

def getSeries(name, processorNumber):
    procNum = Util.sanitizeString(processorNumber)
    tipe = ''
    if ' ' in procNum:
        tipe = procNum.split(' ')[0]
        procNum = procNum.split(' ')[1]

    if procNum != '':
        name = name.replace(procNum + ' ', '')

    san = Util.sanitizeString(name)
    if 'Intel ' in san and ' Processor' in san:
        return re.findall('Intel (.*) Processor', Util.sanitizeString(name))[0]
    elif 'Intel ' in san and ' Coprocessor' in san:
        return re.findall('Intel (.*) Coprocessor', Util.sanitizeString(name))[0]
    elif 'Intel ' not in san and ' Processor' in san:
        return re.findall('(.*) Processor', Util.sanitizeString(name))[0]
    elif 'Intel ' in san and ' SoC' in san:
        return re.findall('Intel (.*) SoC', Util.sanitizeString(name))[0] + ' SoC'
    elif 'Intel ' in san and ' Controller' in san:
        return re.findall('Intel (.*) Controller', Util.sanitizeString(name))[0] + ' Controller'
    else:
        Util.printErr(name)

def getBrand(name):
    return Util.sanitizeString(name.split(' ')[0])

def getCache(name):
    splittedName = Util.sanitizeString(name).split(' ')

    strCacheIdx = None
    if 'Cache' in name:
        strCacheIdx = splittedName.index('Cache')
    elif 'cache' in name:
        strCacheIdx = splittedName.index('cache')
    else:
        return ''

    return splittedName[strCacheIdx - 1]

def getClockSpeed(data):
    baseFreq = Util.returnEmptyIfNone(data, 'Processor Base Frequency')
    turboFreq = Util.returnEmptyIfNone(data, 'Max Turbo Frequency')
    if turboFreq == '':
        return baseFreq
    elif baseFreq == '':
        return turboFreq + ' Turbo'
    else:
        return baseFreq + ' (' + turboFreq + ' Turbo)'

def getProcessorGraphics(pg):
    if pg == 'None':
        return ''
    else:
        return pg

def getMemoryTypes(mt):
    mt = Util.sanitizeStringWithSpace(mt)
    if ' ' in mt:
        memTypes = []
        memSpeed = []
        splittedMt = mt.split(' ')
        for tok in splittedMt:
            if 'D' in tok:
                memTypes.append(tok)
            else:
                try:
                    if int(tok):
                        memSpeed.append(tok)
                except ValueError:
                    a = None

        return ('/'.join(memTypes), '/'.join(memSpeed) + ' MHz')
    else:
        return (mt,'')

def getMemorySpeed(mt):
    if ' ' in mt:
        return mt.split(' ')[1]
    else:
        return ''

def getDescription(data):
    r = ''
    for key, value in data.items():
        if value == 'Yes':
            r = r + Util.sanitizeString(key) + '\n'

    return r

def mapJSON(data):
    r = {}
    r['name_300'] = Util.returnEmptyIfNone(data, 'Name')
    r['description'] = getDescription(data)
    r['release_date'] = Util.getCurrentDate() 
    r['general_brand'] = getBrand(r['name_300'])
    r['general_series'] = getSeries(r['name_300'], Util.returnEmptyIfNone(data, 'Processor Number'))
    r['general_socket-type'] = Util.returnEmptyIfNone(data, 'Sockets Supported')
    r['processor_core'] = Util.returnEmptyIfNone(data, '# of Cores')
    r['processor_threads'] = Util.returnEmptyIfNone(data, '# of Threads')
    r['processor_clock-speed'] = getClockSpeed(data)
    r['processor_cache'] = getCache(r['name_300'])
    r['processor_lithography'] = Util.returnEmptyIfNone(data, 'Lithography')
    r['processor_max-thermal-design-power-tdp'] = Util.returnEmptyIfNone(data, 'TDP') 
    r['memory_max-size'] = Util.returnEmptyIfNone(data, 'Max Memory Size (dependent on memory type)')
    r['memory_type'] = getMemoryTypes(Util.returnEmptyIfNone(data, 'Memory Types'))[0]
    r['memory_speed'] = getMemoryTypes(Util.returnEmptyIfNone(data, 'Memory Types'))[1]
    r['memory_channels'] = Util.returnEmptyIfNone(data, 'Max # of Memory Channels')
    r['graphics_processor-graphics'] = getProcessorGraphics(Util.returnEmptyIfNone(data, u'Processor Graphics \u2021'))
    r['graphics_base-frequency'] = Util.returnEmptyIfNone(data, 'Graphics Base Frequency')
    r['graphics_max-dynamic-frequency'] = Util.returnEmptyIfNone(data, 'Graphics Max Dynamic Frequency')
    r['expansion_pci-express-revision'] = Util.returnEmptyIfNone(data,  'PCI Express Revision')
    r['identifier'] = ''
    r['picture'] = ''
    r['action'] = ''

    return r


def mapToCSV(formattedJSON, filename):
    indexMap = createIndexMap()
    f = open(filename, 'w')
    f.write('"' + '","'.join(indexMap) + '"\n')
    for (jsonData) in formattedJSON['results']:
        resultMap = mapJSON(jsonData)
        f.write(Util.mapToCSVLine(indexMap, resultMap) + '\n')
    f.close()

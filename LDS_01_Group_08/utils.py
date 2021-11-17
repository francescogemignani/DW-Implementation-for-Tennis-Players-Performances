import csv


def isEmpty(elem):
    return not elem

def getCSVlength(fileIn):
    with open(fileIn,mode='r') as fileIn:
        return sum( 1 for _ in fileIn)

def cast(value,type):
    if type is float:
        return float(value)
    elif type is int:
        return round(float(value))
    elif type is str:
        return str(value)
    else:
        raise TypeError(f"Attention! Unknown type {type}")

def print4length(pathIn, col, threshold, delimiter=','):
    f = open(pathIn, mode="r")
    csvIn = csv.reader(f, delimiter=delimiter)
    for row in csvIn:
        if len(row[col]) < threshold:
            print(row)
    f.close()

def printCSV(pathIn, mode='r', delimiter=',', length=5):
    f = open(pathIn, mode=mode)
    csvIn = csv.reader(f, delimiter=delimiter)
    c = 0
    for row in csvIn:
        if c < length:
            print(row)
        else:
            break
        c += 1
    f.close()

def approxInt(value):
    return int(round(value))

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def isInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def makeDict(pathIn,key,value):
    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")
    d = {}
    for row in csvIn:
        d[row[key]] = row[value]
    return d

def scopeStrLength(serie,threshold = 10):
    unique_vals = list(serie.unique())
    print("Show all element with length less or equal to %d:\n" % threshold)
    for val in unique_vals:
        if len(val) <= threshold:
            print(val)
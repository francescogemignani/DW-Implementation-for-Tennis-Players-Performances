import csv

def print4length(pathIn, col, threshold, delimiter=','):
    f = open(pathIn, mode="r")
    csvIn = csv.reader(f, delimiter=delimiter)
    for row in csvIn:
        if len(row[col]) < threshold:
            print(row)
    f.close()

def printCSV(pathIn, mode = 'r', delimiter=',', length=5):
    f = open(pathIn, mode=mode)
    csvIn = csv.reader(f, delimiter=delimiter)
    c = 0
    for row in csvIn:
        if c <length:
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


#filt4length("./tmp/player.csv",'sex',1)
#printCSV("./tmp/match.csv")

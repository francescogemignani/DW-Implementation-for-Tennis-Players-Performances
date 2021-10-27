import csv
from math import ceil
from constant import *
from utils import *

def openFiles(pathIn, pathsOutList):
    global fileIn, fileOutList

    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")

    fileOutList, csvOutList = [],[]
    for pathOut in pathsOutList:
        fileOut =open(pathOut, mode='w', newline='')
        fileOutList.append(fileOut)
        csvOutList.append(csv.writer(fileOut,delimiter=","))
    return [csvIn,csvOutList]

def closeFiles():
    fileIn.close()
    for fileOut in fileOutList:
        fileOut.close()

def country_dict(pathIn):
    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")

    locDict = {}
    for row in csvIn:
        locDict[row['country_code']] = [row['continent'], row['country_name']]
    fileIn.close()
    return locDict

def players_gender_dict(pathIn,gender='M'):
    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")
    nameSexDict = {}
    for row in csvIn:
        name = row['name'] + " " + row['surname']
        nameSexDict[name] = gender
    fileIn.close()
    return nameSexDict

def all_players_s_sex(pathMalePlayers, pathFemalePlayers):
    male_dict = players_gender_dict(pathMalePlayers)
    females_dict = players_gender_dict(pathFemalePlayers, gender='F')
    male_dict.update(females_dict)
    return male_dict

def win_or_los(rowIn,attr,key):
    if rowIn[attr] == key:
        return W_PLAYER_TABLE_FEATS
    else:
        return L_PLAYER_TABLE_FEATS

def genKeyValues(row):
    match_keyVal = str(row['match_num']) + "-" + row['tourney_id']
    tourn_keyVal = str(row['tourney_id'])
    date_keyVal = str(row['tourney_date'])
    player_keyVal = [int(row['winner_id']),int(row['loser_id'])]
    country_keyVal = [str(row['winner_ioc']),str(row['loser_ioc'])]
    return [match_keyVal,tourn_keyVal,date_keyVal,player_keyVal,country_keyVal]


def getUniqueKey(keyValue,keySet):
    uniqueKeys = []

    if isinstance(keyValue,str):
        if keyValue not in keySet:
            keySet.add(keyValue)
            uniqueKeys.append(keyValue)

    if isinstance(keyValue,list):
        for key in keyValue:
            if key not in keySet:
                keySet.add(key)
                uniqueKeys.append(key)
    return uniqueKeys


def getUniqueKeys(keyVals,keySets):
    uniqueKeyVals = []
    for i in range(NTABS):
        uniqueKeyVals.append(getUniqueKey(keyVals[i], keySets[i]))
    return uniqueKeyVals


def appendByType(rowIn,feat,rowOut):
    val = rowIn[feat]
    type = MATCH_TOURN_CAST_TYPES[feat]
    if type == 'float':
        try:
            rowOut.append(float(val))
        except ValueError:
            rowOut.append("")
    elif type == 'int':
        try:
            rowOut.append(int(float(val)))
        except ValueError:
            rowOut.append("")
    else:
        rowOut.append(val)

def makeMatchRow(rowIn, csvOut, keyVal):
    if isEmpty(keyVal):
        return

    rowOut = []
    for feat in MATCH_TABLE_FEATS:
        if feat == 'match_id':
            rowOut.append(keyVal[0])
        else:
            appendByType(rowIn,feat,rowOut)
    csvOut.writerow(rowOut)


def makeTournamentRow(rowIn, csvOut, keyVal):
    if isEmpty(keyVal):
        return

    rowOut = []
    for feat in TOURNAMENT_TABLE_FEATS:
        if feat == 'tourney_id':
            rowOut.append(keyVal[0])
        elif feat == "date_id":
            appendByType(rowIn,"tourney_date",rowOut)
    csvOut.writerow(rowOut)


def makeDateRow(csvOut,keyVal):
    if isEmpty(keyVal):
        return

    rowOut = []
    keyVal = keyVal[0]
    for feat in DATE_TABLE_FEATS:
        if feat == 'date_id':
            rowOut.append(int(keyVal))
        elif feat == 'day':
            rowOut.append(int(keyVal[6:8]))
        elif feat == 'month':
            rowOut.append(int(keyVal[4:6]))
        elif feat == 'year':
            rowOut.append(int(keyVal[0:4]))
        elif feat == 'quarter':
            rowOut.append(ceil(int(keyVal[4:6])/3))
        else:
            raise KeyError("Attention: the key format must be yyyymmdd: %s" % keyVal)
    csvOut.writerow(rowOut)





def makePlayerSingleRow(rowIn, csvOut, keyVal, sexDict):
    # Verifico se la chiave rappresenta il vincitore o lo sconfitto. Prendo il rispettivo dizionario
    wl = win_or_los(rowIn,'winner_id',keyVal)

    rowOut = []
    for feat in PLAYER_TABLE_FEATS:
        if feat == 'player_id':
            rowOut.append(keyVal)
        elif feat == 'year_of_birth':
            try:
                currYear = int((rowIn['tourney_id'])[0:4])
                agePlayer = int(float(rowIn[wl['year_of_birth']]))
                rowOut.append(currYear - agePlayer)
            except ValueError:
                rowOut.append("")
        elif feat == 'sex':
            wlName = rowIn[wl['name']]
            try:
                wlSex = sexDict[wlName]
            except KeyError:
                wlSex = ""
            rowOut.append(wlSex)
        else:
            rowOut.append(rowIn[wl[feat]])
    csvOut.writerow(rowOut)


def makePlayerRow(rowIn, csvOut, keyVal, sexDict):
    nkey = len(keyVal)
    if nkey == 0:
        return
    elif nkey == 1:
        makePlayerSingleRow(rowIn, csvOut, keyVal[0], sexDict)
    elif nkey == 2:
        makePlayerSingleRow(rowIn, csvOut, keyVal[0], sexDict)
        makePlayerSingleRow(rowIn, csvOut, keyVal[1], sexDict)
    else:
        raise Exception("Attention! There are at most 2 keys for each line")

def makeGeoSingleRow(csvOut, keyVal, locDict):
    rowOut = []

    for feat in GEO_TABLE_FEATS:
        if feat == 'country_ioc':
            ### CHIEDERE SE UN PAESE NON E' NEL DIZIONARIO LO INSERISCO NELLA GEO TABLE?
            rowOut.append(keyVal)
        elif feat == 'continent':
            try:
                cont = locDict[keyVal][CONT]
            except KeyError:
                cont = ""
            rowOut.append(cont)
        else:
            try:
                lan = locDict[keyVal][LANG]
            except KeyError:
                lan = ""
            rowOut.append(lan)
    csvOut.writerow(rowOut)

def makeGeoRow(csvOut, keyVal, locDict):
    nkey = len(keyVal)

    if nkey == 0:
        return
    elif nkey == 1:
        makeGeoSingleRow(csvOut, keyVal[0],locDict)
    elif nkey == 2:
        makeGeoSingleRow(csvOut, keyVal[0],locDict)
        makeGeoSingleRow(csvOut, keyVal[1],locDict)
    else:
        raise Exception("Attention! There are at most 2 keys for each line")

def makeAllRows(rowIn, csvOutList, uniqueKeyVals, keySets, sexDict,locDict):
    makeMatchRow(rowIn, csvOutList[MATCH], uniqueKeyVals[MATCH])
    makeTournamentRow(rowIn, csvOutList[TOURNAMENT], uniqueKeyVals[TOURNAMENT])
    makeDateRow(csvOutList[DATE], uniqueKeyVals[DATE])
    makePlayerRow(rowIn, csvOutList[PLAYER], uniqueKeyVals[PLAYER], sexDict)
    makeGeoRow(csvOutList[GEO], uniqueKeyVals[GEO], locDict)


def splitFactSchema(fileIn, fileOutList):
    csvList = openFiles(fileIn,fileOutList)
    csvIn, csvOutList = csvList[0], csvList[1]

    #Write the attributes
    i=0
    for csvOut in csvOutList:
        csvOut.writerow(ALL_TABLES_FEATS[i])
        i+=1

    # Make a keyset for each table to guarantee the unicity of the primary keys
    keySets = [set() for _ in range(NTABS)]

    # Make the dict with players name and gender
    sexDict = all_players_s_sex(PATH_MALE_PLAYERS,PATH_FEMALE_PLAYERS)
    locDict = country_dict(PATH_GEO)

    # For each fact row:
    for rowIn in csvIn:

        # 1. Extract the key value for all tables
        keyVals = genKeyValues(rowIn)

        # 2. For each table check that key values are unique. Therefore, for every table, I only push the keys which
        # are not present. Otherwise the key is not inserted.
        uniqueKeyVals = getUniqueKeys(keyVals,keySets)

        # 3. Build and push all table rows
        makeAllRows(rowIn, csvOutList, uniqueKeyVals, keySets, sexDict, locDict)

    closeFiles()









splitFactSchema(PATH_TENNIS, ALL_TABS)
#splitFactSchema(PATH_TENNIS,PATH_TOURNAMENT_CSV,TOURNAMENT_TABLE_FEATS,TOURNAMENT_KEY)
#splitFactSchema(PATH_TENNIS, PATH_DATE_CSV, DATE_TABLE_FEATS, DATE_KEY)


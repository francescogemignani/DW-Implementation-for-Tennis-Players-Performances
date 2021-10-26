import csv
from math import ceil
from constant import *

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


def getKeyValues(row):
    match_keyVal = str(row['match_num']) + "-" + row['tourney_id']
    tourn_keyVal = row['tourney_id']
    date_keyVal = row['tourney_date']
    player_keyVal = (row['winner_id'],row['loser_id'])
    country_keyVal = (row['winner_ioc'],row['loser_ioc'])
    return (match_keyVal,tourn_keyVal,date_keyVal,player_keyVal,country_keyVal)


def getUniqueKey(keyValue,keySet):
    if isinstance(keyValue,str) and keyValue not in keySet:
        return keyValue

    if isinstance(keyValue,tuple) and len(keyValue) == 2:
        if keyValue[0] == keyValue[1] and keyValue[0] not in keySet:
            return [keyValue[0]]

    mask = []
    if isinstance(keyValue,tuple) and len(keyValue) == 2:
        for i in range(2):
            mask.append(keyValue[i] not in keySet)
        return [val for mask, val in zip(mask,keyValue) if mask]


def getUniqueKeys(keyVals,keySets):
    uniqueKeyVals = []
    for i in range(NTABS):
        uniqueKey = getUniqueKey(keyVals[i], keySets[i])
        uniqueKeyVals.append(uniqueKey)
    return uniqueKeyVals

def isEmpty(l):
    return not l


def makeMatchRow(rowIn, csvOut, keyVal, keyset):
    if isEmpty(keyVal):
        return

    rowOut = []
    keyset.add(keyVal)
    for feat in MATCH_TABLE_FEATS:
        if feat == 'match_id':
            rowOut.append(keyVal)
        else:
            rowOut.append(rowIn[feat])
    csvOut.writerow(rowOut)


def makeTournamentRow(rowIn, csvOut, keyVal, keyset):
    if isEmpty(keyVal):
        return

    rowOut = []
    keyset.add(keyVal)
    for feat in TOURNAMENT_TABLE_FEATS:
        if feat == 'tourney_id':
            rowOut.append(keyVal)
        elif feat == 'date_id':
            rowOut.append(rowIn['tourney_date'])
        else:
            rowOut.append(rowIn[feat])
    csvOut.writerow(rowOut)

def makeDateRow(csvOut,keyVal,keyset):
    if isEmpty(keyVal):
        return

    rowOut = []
    keyset.add(keyVal)
    for feat in DATE_TABLE_FEATS:
        if feat == 'date_id':
            rowOut.append(keyVal)
        elif feat == 'day':
            rowOut.append(keyVal[6:8])
        elif feat == 'month':
            rowOut.append(keyVal[4:6])
        elif feat == 'year':
            rowOut.append(keyVal[0:4])
        elif feat == 'quarter':
            rowOut.append(ceil(int(keyVal[4:6])/3))
        else:
            raise KeyError("Attention: the key format must be yyyymmdd: %s" % keyVal)
    csvOut.writerow(rowOut)

def players_gender_dict(pathIn,gender='M'):
    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")
    nameSexDict = {}
    for row in csvIn:
        name = row['name'] + " " + row['surname']
        nameSexDict[name] = gender
    fileIn.close()
    return nameSexDict

def country_dict(pathIn):
    fileIn = open(pathIn, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")

    locDict = {}
    for row in csvIn:
        locDict[row['country_code']] = [row['continent'], row['country_name']]
    fileIn.close()
    return locDict


def all_players_s_sex(pathMalePlayers, pathFemalePlayers):
    male_dict = players_gender_dict(pathMalePlayers)
    females_dict = players_gender_dict(pathFemalePlayers, gender='F')
    male_dict.update(females_dict)
    return male_dict

def win_or_los(rowIn,attr,key):
    if rowIn[attr] == key:
        return WIN
    else:
        return LOS

def makePlayerSingleRow(rowIn,csvOut,keyVal,keySet,d_sex):
    # Verifico se la chiave rappresenta il vincitore o lo sconfitto e prendo il rispettivo dizionario. Quest'ultimo
    # mappa le features di player.csv con quelle di tennis.csv (winnero o loser)
    wl = win_or_los(rowIn,'winner_id',keyVal)
    wlRefTab = D_WL[wl]

    rowOut = []
    keySet.add(keyVal)
    for feat in PLAYER_TABLE_FEATS:
        if feat == 'player_id':
            rowOut.append(keyVal)
        elif feat == 'year_of_birth':
            try:
                currYear = int((rowIn['tourney_id'])[0:4])
                agePlayer = round(float(rowIn[wlRefTab['year_of_birth']]))
                rowOut.append(currYear - agePlayer)
            except ValueError:
                rowOut.append("")
        elif feat == 'sex':
            wlName = rowIn[wlRefTab['name']]
            try:
                wlSex = d_sex[wlName]
            except KeyError:
                wlSex = ""
            rowOut.append(wlSex)
        else:
            wlFeat = wlRefTab[feat]
            rowOut.append(rowIn[wlFeat])
    csvOut.writerow(rowOut)


def makePlayerRow(rowIn,csvOut,keyValList,keySet,d_sex):
    nkey = len(keyValList)
    if nkey == 0:
        pass
    elif nkey == 1:
        makePlayerSingleRow(rowIn,csvOut,keyValList[0],keySet,d_sex)
    elif nkey == 2:
        makePlayerSingleRow(rowIn,csvOut,keyValList[0],keySet,d_sex)
        makePlayerSingleRow(rowIn, csvOut, keyValList[1], keySet, d_sex)
    else:
        raise Exception("Attention! There are at most 2 keys for each line")

def makeGeoSingleRow(rowIn,csvOut,keyVal,keySet,d_loc):
    rowOut = []
    keySet.add(keyVal)
    for feat in GEO_TABLE_FEATS:
        if feat == 'country_ioc':
            rowOut.append(keyVal)
        elif feat == 'continent':
            try:
                cont = d_loc[keyVal][CONTINENT]
            except KeyError:
                cont = ""
            rowOut.append(cont)
        else:
            try:
                lan = d_loc[keyVal][LANG]
            except KeyError:
                lan = ""
            rowOut.append(lan)
    csvOut.writerow(rowOut)

def makeGeoRow(rowIn,csvOut,keyValList,keySet,d_loc):
    nkey = len(keyValList)
    if nkey == 0:
        pass
    elif nkey == 1:
        makeGeoSingleRow(rowIn,csvOut,keyValList[0],keySet,d_loc)
    elif nkey == 2:
        makeGeoSingleRow(rowIn,csvOut,keyValList[0],keySet,d_loc)
        makeGeoSingleRow(rowIn, csvOut, keyValList[1], keySet, d_loc)
    else:
        raise Exception("Attention! There are at most 2 keys for each line")

def makeAllRows(rowIn, csvOutList, uniqueKeyVals, keySets, d_sex,d_loc):
    makeMatchRow(rowIn, csvOutList[MATCH], uniqueKeyVals[MATCH], keySets[MATCH])
    makeTournamentRow(rowIn, csvOutList[TOURNAMENT], uniqueKeyVals[TOURNAMENT], keySets[TOURNAMENT])
    makeDateRow(csvOutList[DATE], uniqueKeyVals[DATE], keySets[DATE])
    makePlayerRow(rowIn, csvOutList[PLAYER], uniqueKeyVals[PLAYER], keySets[PLAYER], d_sex)
    makeGeoRow(rowIn, csvOutList[GEO], uniqueKeyVals[GEO], keySets[GEO], d_loc)


def splitFactSchema(fileIn, fileOutList):
    csvList = openFiles(fileIn,fileOutList)
    csvIn, csvOutList = csvList[0], csvList[1]

    #Write the attributes
    i=0
    for csvOut in csvOutList:
        csvOut.writerow(TABLES_FEATS_LIST[i])
        i+=1

    # Make a keyset for each table to guarantee the unicity of the keys
    keySets = [set() for _ in range(NTABS)]

    # Make the dict with players name and gender
    d_sex= all_players_s_sex(PATH_MALE_PLAYERS,PATH_FEMALE_PLAYERS)
    d_loc = country_dict(PATH_GEO)

    # For each fact row:
    for rowIn in csvIn:

        # 1. Extract the key value for all tables
        keyVals = getKeyValues(rowIn)

        # 2. For each table check that key values are unique. Therefore, for every table, I only push the keys which
        # are not present. Otherwise the key is not inserted.
        uniqueKeyVals = getUniqueKeys(keyVals,keySets)
        kk = uniqueKeyVals[GEO]

        # 3. Build and push all table rows
        makeAllRows(rowIn, csvOutList,uniqueKeyVals,keySets,d_sex,d_loc)

    closeFiles()









splitFactSchema(PATH_TENNIS_CSV,ALL_TABLES_PATH)
#splitFactSchema(PATH_TENNIS_CSV,PATH_TOURNAMENT_CSV,TOURNAMENT_TABLE_FEATS,TOURNAMENT_KEY)
#splitFactSchema(PATH_TENNIS_CSV, PATH_DATE_CSV, DATE_TABLE_FEATS, DATE_KEY)


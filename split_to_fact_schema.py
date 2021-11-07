import csv
from math import ceil
from utils import *
from constants import *

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

def country_dict(pathCountry,pathLang):
    dLang = makeDict(pathLang, key="country_name",value="lang_name")
    fileIn = open(pathCountry, mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")

    d = {}
    for row in csvIn:
        continent = row['continent']
        try:
            language = dLang[row['country_name']]
        except KeyError:
            language = ""
        d[row['country_code']] = [continent,language]
    return d

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

def getUniqueKeys(keyList,keySet):
    i, keys = 0, []
    for k in keyList:
        if k not in keySet:
            keySet.add(k)
            keys.append((k,i))
        i+=1
    return keys

def makeMatchRow(rowIn, csvOut, keySet):
    keyValue = str(rowIn['match_num']) + "-" + str(rowIn['tourney_id']) + '-' + str(rowIn['tourney_level'])
    if keyValue in keySet:
        return

    keySet.add(keyValue)
    rowOut = []
    for feat,type in MATCH_FEAT_TYPE.items():
        if feat == 'match_id':
            #rowOut.append(cast(keyValue,type))
            rowOut.append(keyValue)
        else:
            try:
                #rowOut.append(cast(rowIn[feat],type))
                rowOut.append(rowIn[feat])
            except ValueError:
                rowOut.append("")
    csvOut.writerow(rowOut)

def makeTournamentRow(rowIn, csvOut, keySet):
    keyValue = str(rowIn['tourney_id']) + '-' + str(rowIn['tourney_level'])
    if keyValue in keySet:
        return

    keySet.add(keyValue)
    rowOut = []
    for feat,type in TOURN_FEAT_TYPE.items():
        if feat == 'tourney_id':
            rowOut.append(cast(keyValue,type))
        elif feat == "date_id":
            try:
                rowOut.append(cast(rowIn["tourney_date"],type))
            except ValueError:
                rowOut.append("")
        else:
            try:
                rowOut.append(cast(rowIn[feat],type))
            except ValueError:
                rowOut.append("")
    csvOut.writerow(rowOut)

def makeDateRow(rowIn, csvOut, keySet):
    keyValue = str(rowIn['tourney_date'])
    if keyValue in keySet:
        return

    keySet.add(keyValue)
    rowOut = []
    for feat,type in DATE_FEAT_TYPE.items():
        if feat == 'date_id':
            rowOut.append(cast(keyValue,type))
        elif feat == 'day':
            rowOut.append(cast(keyValue[6:8],type))
        elif feat == 'month':
            rowOut.append(cast(keyValue[4:6],type))
        elif feat == 'year':
            rowOut.append(cast(keyValue[0:4],type))
        else:
            q = int(keyValue[4:6])/3
            rowOut.append(ceil(q))
    csvOut.writerow(rowOut)

def makePlayerRow(rowIn, csvOut, keyValue, sexDict):
    keyValue, keyType = keyValue[0], keyValue[1]

    if keyType == WIN:
        wlPlayer = W_PLAYER_TABLE_FEATS
    else:
        wlPlayer = L_PLAYER_TABLE_FEATS


    rowOut = []
    for feat, type in PLAYER_FEAT_TYPE.items():
        if feat == 'player_id':
            rowOut.append(cast(keyValue,type))
        elif feat == 'sex':
            wlName = rowIn[wlPlayer['name']]
            try:
                rowOut.append(cast(sexDict[wlName],type))
            except KeyError:
                rowOut.append("")
        elif feat == 'year_of_birth':
            try:
                currYear = CURR_YEAR
                agePlayer = round(float(rowIn[wlPlayer['year_of_birth']]))
                yearOfBirth = currYear - agePlayer
                rowOut.append(cast(yearOfBirth,type))
            except ValueError:
                rowOut.append("")
        else:
            try:
                rowOut.append(cast(rowIn[wlPlayer[feat]], type))
            except ValueError:
                rowOut.append("")
    csvOut.writerow(rowOut)

def makePlayerRows(rowIn, csvOut, keySet, sexDict):
    keyValue_w = rowIn['winner_id']
    keyValue_l = rowIn['loser_id']

    key2Push = getUniqueKeys([keyValue_w,keyValue_l],keySet)

    if isEmpty(key2Push):
        return
    for keyValue in key2Push:
        makePlayerRow(rowIn,csvOut,keyValue, sexDict)

def makeGeoRow(rowIn,csvOut,keyValue, locDict):
    keyValue, keyType = keyValue[0], keyValue[1]

    rowOut=[]
    for feat, type in GEO_FEAT_TYPE.items():
        if feat == 'country_ioc':
            rowOut.append(cast(keyValue,type))
        elif feat == 'continent':
            try:
                rowOut.append(cast(locDict[keyValue][CONTINENT], type))
            except KeyError:
                rowOut.append("")
        else:
            try:
                rowOut.append(cast(locDict[keyValue][LANGUAGE], type))
            except KeyError:
                rowOut.append("")
    csvOut.writerow(rowOut)

def makeGeoRows(rowIn, csvOut, keySet, locDict):
    keyValue_w = rowIn['winner_ioc']
    keyValue_l = rowIn['loser_ioc']
    key2Push = getUniqueKeys([keyValue_w,keyValue_l],keySet)

    if isEmpty(key2Push):
        return
    for keyValue in key2Push:
        makeGeoRow(rowIn,csvOut,keyValue, locDict)

def makeTabsHeaders(csvOutList):
    csvOutList[MATCH].writerow(MATCH_FEAT_TYPE.keys())
    csvOutList[TOURNAMENT].writerow(TOURN_FEAT_TYPE.keys())
    csvOutList[DATE].writerow(DATE_FEAT_TYPE.keys())
    csvOutList[PLAYER].writerow(PLAYER_FEAT_TYPE.keys())
    csvOutList[GEO].writerow(GEO_FEAT_TYPE.keys())

def makeTabsRows(rowIn,csvOutList,keySets,sexDict, locDict):
    makeMatchRow(rowIn, csvOutList[MATCH], keySets[MATCH])
    makeTournamentRow(rowIn, csvOutList[TOURNAMENT], keySets[TOURNAMENT])
    makeDateRow(rowIn, csvOutList[DATE], keySets[DATE])
    makePlayerRows(rowIn, csvOutList[PLAYER], keySets[PLAYER], sexDict)
    makeGeoRows(rowIn, csvOutList[GEO], keySets[GEO], locDict)

def split2FactSchema(pathIn,pathOutList):
    csvList = openFiles(pathIn,pathOutList)
    csvIn, csvOutList = csvList[0], csvList[1]

    # Scrivo li headers per ogni tabella
    makeTabsHeaders(csvOutList)

    # Creo un keyset per ogni tabella con il quale testare l'unicità delle chiavi primarie
    keySets = [set() for _ in range(NTABS)]

    # Creo il dizionario per derivare il sesso dei 'player'
    sexDict = all_players_s_sex(PATH_MALE_PLAYERS, PATH_FEMALE_PLAYERS)

    # Creo il dizionario per derivare il continente ed il linguaggio di un certo 'country'
    locDict = country_dict(PATH_GEO,PATH_LANG)

    # Per ogni riga di tennis.csv
    for rowIn in csvIn:
        makeTabsRows(rowIn,csvOutList,keySets,sexDict,locDict)

    closeFiles()







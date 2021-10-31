import pyodbc
import csv
from constants import *
from utils import *

def makeSQLInsertionString(tabName,colsName):
    s = "INSERT INTO "+tabName+" ("
    first = True
    for col in colsName:
        if first:
            first = False
        else:
            s+=", "
        s+=col
    s+=") VALUES("
    first = True
    for _ in range(len(colsName)):
        if first:
            first = False
        else:
            s+=","
        s+="?"
    return s+")"

def getBlock(csvIn,block):
    i, data = 0,[]
    first = True
    for row in csvIn:
        if first:
            first = False
        else:
            if i < block:
                data.append(row)
            else:
                return data
            i += 1
    return data

def tabPaging(csvIn, blockSize):
    blocks = []
    while True:
        block = getBlock(csvIn,blockSize)
        if isEmpty(block):
            return blocks
        else:
            blocks.append(block)

def insert_b_db(connection, pathIn, tabName, tabFeats, blockSize = 500):
    fileIn = open(pathIn, mode='r')
    csvIn = csv.reader(fileIn, delimiter=',')
    cursor = connection.cursor()
    sql = makeSQLInsertionString(tabName=tabName, colsName=tabFeats)

    id = 0
    for block in tabPaging(csvIn, blockSize):
        print(id)
        cursor.executemany(sql,block)
        cursor.commit()
        id+=1

    connection.commit()
    fileIn.close()
    cursor.close()

def insert_db(connection, pathIn, tabName, tabFeats, mod = 100):
    count = 0
    csv_length = getCSVlength(pathIn)
    print("Pushing data in %s table: " % tabName)

    fileIn = open(pathIn, mode='r')
    csvIn = csv.DictReader(fileIn, delimiter=',')
    sql = makeSQLInsertionString(tabName=tabName, colsName=tabFeats)
    cursor = connection.cursor()
    for row in csvIn:
        if count % mod == 0:
            print(">%d/%d.." % (count,csv_length) )
        cursor.execute(sql, [row[attr] for attr in tabFeats])
        count+=1
        print(count)
    fileIn.close()
    connection.commit()
    cursor.close()

# Set the connection
server = 'tcp:lds.di.unipi.it'
database = 'GROUP_8_DB'
username = 'Group_8'
password = 'P0T8K7Q4'
print("Connecting to %s..." % server)
connectionString =  "DRIVER={ODBC Driver 17 for SQL Server};"\
                    "SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password
cnxn = pyodbc.connect(connectionString)
print("Connected established!")
print()

insert_db(cnxn,"./tmp/date.csv","date",DATE_FEAT_TYPE.keys())
insert_db(cnxn,"./tmp/tournament.csv","tournament",TOURN_FEAT_TYPE.keys())
insert_db(cnxn,"./tmp/geography.csv","geography",GEO_FEAT_TYPE.keys())
insert_db(cnxn,"./tmp/player.csv","player",PLAYER_FEAT_TYPE.keys(),mod=100)
insert_b_db(cnxn, "./tmp/match.csv", "match", MATCH_FEAT_TYPE.keys(), blockSize=1000)


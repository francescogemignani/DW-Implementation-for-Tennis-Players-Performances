import pyodbc
import csv
from constant import *

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

def fillTable(fileIn):
    fileIn = open(fileIn, mode='r')
    csvIn = csv.DictReader(fileIn, delimiter=',')
    #estrarre tabName e colsName da fileIn
    sql = makeSQLInsertionString(tabName=None, colsName=None)
    for row in csvIn:
        cursor.execute(sql, [row[attr] for attr in colsName])
    fileIn.close()


# Set the connection
server = 'tcp:lds.di.unipi.it'
database = 'GROUP_8_DB'
username = 'Group_8'
password = 'P0T8K7Q4'
print("Connecting to %s..." % server)
connectionString =  "DRIVER={ODBC Driver 17 for SQL Server};"\
                    "SERVER="+server+";DATABASE="+database+";UID="+username+";PWD="+password
cnxn = pyodbc.connect(connectionString)
print("Connected")
cursor = cnxn.cursor()


"""
# date table
tab = "./tmp/date.csv"
fileIn = open(tab,mode='r')
csvIn = csv.DictReader(fileIn,delimiter=',')
sql = makeSQLInsertionString(tabName="date",colsName=DATE_TABLE_FEATS)
for row in csvIn:
    cursor.execute(sql, [row[attr] for attr in DATE_TABLE_FEATS])
cnxn.commit()
cursor.close()
"""

"""
# Tournament table
tab = "./tmp/tournament.csv"
fileIn = open(tab,mode='r')
csvIn = csv.DictReader(fileIn,delimiter=',')
sql = makeSQLInsertionString(tabName="tournament",colsName=TOURNAMENT_TABLE_FEATS)
for row in csvIn:
    cursor.execute(sql, [row[attr] for attr in TOURNAMENT_TABLE_FEATS])
cnxn.commit()
cursor.close()
"""

"""# Geography table
tab = "./tmp/geography.csv"
fileIn = open(tab,mode='r')
csvIn = csv.DictReader(fileIn,delimiter=',')
sql = makeSQLInsertionString(tabName="geography",colsName=GEO_TABLE_FEATS)
for row in csvIn:
    cursor.execute(sql, [row[attr] for attr in GEO_TABLE_FEATS])
cnxn.commit()
cursor.close()"""

def getCSVlength(fileIn):
    with open(fileIn,mode='r') as fileIn:
        return sum( 1 for _ in fileIn)

#Player table
path = "./tmp/player.csv"
c = 0
csvLength = getCSVlength(path)
print("Fill table 'player' with %d records" % csvLength)

fileIn = open(path,mode='r')
csvIn = csv.DictReader(fileIn,delimiter=',')
sql = makeSQLInsertionString(tabName="player",colsName=PLAYER_TABLE_FEATS)

for row in csvIn:
    ratio = c*100/csvLength
    if (ratio % 5) == 0:
        print("%d completed.." % ratio)
    cursor.execute(sql, [row[attr] for attr in PLAYER_TABLE_FEATS])
    c+=1
    print(c)

fileIn.close()

cnxn.commit()
cursor.close()

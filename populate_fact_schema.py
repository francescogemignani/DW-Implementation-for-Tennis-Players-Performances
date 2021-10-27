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



def getCSVlength(fileIn):
    with open(fileIn,mode='r') as fileIn:
        return sum( 1 for _ in fileIn)

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



def fillTable(connection, pathIn,tabName, tabFeats, mod = 100):
    count = 0
    csv_length = getCSVlength(pathIn)
    print("Pushing data in %s table: " % tabName)

    fileIn = open(pathIn, mode='r')
    csvIn = csv.DictReader(fileIn, delimiter=',')
    sql = makeSQLInsertionString(tabName=tabName, colsName=tabFeats)
    cursor = cnxn.cursor()
    for row in csvIn:
        if count % mod == 0:
            print(">%d/%d.." % (count,csv_length) )
        cursor.execute(sql, [row[attr] for attr in tabFeats])
        count+=1
        print(count)
    fileIn.close()
    cnxn.commit()
    cursor.close()


#fillTable(cnxn,"./tmp/date.csv","date",DATE_TABLE_FEATS)
#fillTable(cnxn,"./tmp/tournament.csv","tournament",TOURNAMENT_TABLE_FEATS)
#fillTable(cnxn,"./tmp/geography.csv","geography",GEO_TABLE_FEATS)
#fillTable(cnxn,"./tmp/player.csv","player",PLAYER_TABLE_FEATS,mod=100)
fillTable(cnxn,"./tmp/match.csv","match",MATCH_TABLE_FEATS,mod=1000)
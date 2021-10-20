import csv
from math import ceil

MATCH_ID = 0
DATE_ID_TOUR = 1
DATE_ID_DAT = 2

SYNT_ATTRS = { "match_id":["match_num", "tourney_id"], "date_id": "tourney_date", "day": "tourney_date",\
               "month": "tourney_date","year": "tourney_date", "quarter": "tourney_date" }

PATH = "./data/"
PATH_TENNIS_CSV = PATH+"tennis.csv"
PATH_MATCH_CSV =  PATH+"match.csv"
PATH_TOURNAMENT_CSV =  PATH+"tournament.csv"
PATH_DATE_CSV =  PATH+"date.csv"

MATCH_TABLE_FEATS = ['tourney_id','match_id','winner_id','loser_id','score','best_of','round','minutes',\
                     'w_ace','w_df','w_svpt','w_1stIn','w_1stWon','w_2ndWon','w_SvGms','w_bpSaved','w_bpFaced',\
                     'l_ace','l_df','l_svpt','l_1stIn','l_1stWon','l_2ndWon','l_SvGms','l_bpSaved','l_bpFaced',\
                     'winner_rank','winner_rank_points','loser_rank','loser_rank_points']

TOURNAMENT_TABLE_FEATS = ['tourney_id','date_id','tourney_name','surface','draw_size','tourney_level',\
                          'tourney_spectators','tourney_revenue']

DATE_TABLE_FEATS = ['date_id','day','month','year','quarter']


def splitFact(fileIn,fileOut,cols,opt):
    fileIn = open(fileIn,mode="r")
    csvIn = csv.DictReader(fileIn, delimiter=",")
    fileOut = open(fileOut,mode="w")
    csvOut = csv.writer(fileOut, delimiter=",")

    #Write the attributes
    csvOut.writerow(cols)

    #Write data
    first = True
    for line in csvIn:
        if first:
            first = False
        else:
            values = []
            for col in cols:
                try:
                    values.append(line[col])
                except KeyError:
                    if opt == MATCH_ID:
                        matchid = str(line[SYNT_ATTRS[col][0]])+"-"+line[SYNT_ATTRS[col][1]]
                        values.append(matchid)
                    elif opt == DATE_ID_TOUR:
                        dateid = line[SYNT_ATTRS[col]]
                        values.append((dateid))
                    elif opt == DATE_ID_DAT:
                        dateid = line[SYNT_ATTRS[col]]
                        if col == 'date_id':
                            seg = dateid
                        elif col == 'day':
                            seg = dateid[6:8]
                        elif col =='month':
                            seg = dateid[4:6]
                        elif col == 'year':
                            seg = dateid[0:4]
                        else:
                            seg = ceil(int(dateid[4:6])/3)

                        values.append(seg)

                    else:
                        raise KeyError("Attention! Parameter opt = %s is not correct!" % opt)

            csvOut.writerow(values)

    fileOut.close()
    fileIn.close()


#splitFact(PATH_TENNIS_CSV,PATH_MATCH_CSV,MATCH_TABLE_FEATS,opt = MATCH_ID)
#splitFact(PATH_TENNIS_CSV,PATH_TOURNAMENT_CSV,TOURNAMENT_TABLE_FEATS,opt = DATE_ID_TOUR)
splitFact(PATH_TENNIS_CSV,PATH_DATE_CSV,DATE_TABLE_FEATS,opt = DATE_ID_DAT)
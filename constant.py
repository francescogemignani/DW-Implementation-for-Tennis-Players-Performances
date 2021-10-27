# PATHs IN
PATH_TENNIS = "./data/tennis.csv"
PATH_MALE_PLAYERS = "./data/male_players.csv"
PATH_FEMALE_PLAYERS = "./data/female_players.csv"
PATH_GEO = "./data/countries.csv"

# PATHs OUT
PATH_TAB_MATCH = "./tmp/match.csv"
PATH_TAB_TOURNAMENT = "./tmp/tournament.csv"
PATH_TAB_DATE = "./tmp/date.csv"
PATH_TAB_GEO = "./tmp/geography.csv"
PATH_TAB_PLAYER = "./tmp/player.csv"
ALL_TABS = [PATH_TAB_MATCH,PATH_TAB_TOURNAMENT,PATH_TAB_DATE,PATH_TAB_PLAYER,PATH_TAB_GEO]
NTABS = 5

# TABLE FEATURES
MATCH_TABLE_FEATS = ['match_id', 'tourney_id', 'winner_id', 'loser_id', 'score', 'best_of', 'round', 'minutes', \
                     'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', \
                     'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', \
                     'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points']
TOURNAMENT_TABLE_FEATS = ['tourney_id', 'date_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', \
                          'tourney_spectators', 'tourney_revenue']
DATE_TABLE_FEATS = ['date_id', 'day', 'month', 'year', 'quarter']
PLAYER_TABLE_FEATS = ['player_id', 'country_id', 'name', 'sex', 'hand', 'ht', 'year_of_birth']
GEO_TABLE_FEATS = ['country_ioc', 'continent', 'language']
ALL_TABLES_FEATS = [MATCH_TABLE_FEATS, TOURNAMENT_TABLE_FEATS, DATE_TABLE_FEATS, PLAYER_TABLE_FEATS, GEO_TABLE_FEATS]

# MATCH & TOURNAMENT TABLES TYPES
MATCH_TOURN_CAST_TYPES = { "tourney_id": "str", "match_id":"str", "score":"str", "round":"str", "winner_id":"int",\
         "loser_id":"int","best_of":"int", "minutes":"int",'w_ace':"int",'w_df':"int", 'w_svpt':"int", 'w_1stIn':"int",\
         'w_1stWon':"int", 'w_2ndWon':"int", 'w_SvGms':"int", 'w_bpSaved':"int", 'w_bpFaced':"int", 'l_ace':"int",\
         'l_df':"int", 'l_svpt':"int", 'l_1stIn':"int", 'l_1stWon':"int", 'l_2ndWon':"int", 'l_SvGms':"int",\
         'l_bpSaved':"int", 'l_bpFaced':"int",'winner_rank':"int", 'winner_rank_points':"int", 'loser_rank':"int",\
         'loser_rank_points':"int",'date_id':"int", 'tourney_name':'str','surface':'str', 'draw_size':'int',\
         'tourney_level':'str','tourney_spectators':"int", 'tourney_revenue':'float', 'tourney_date':'int'}

# REFERENCES TO PLAYER ATTRIBUTE NAMES (WINNER AND LOSER)
W_PLAYER_TABLE_FEATS = {'player_id': 'winner_id', 'country_id': 'winner_ioc', 'name': 'winner_name', 'hand': 'winner_hand', \
                        'ht': 'winner_ht', 'year_of_birth': 'winner_age'}

L_PLAYER_TABLE_FEATS = {'player_id': 'loser_id', 'country_id': 'loser_ioc', 'name': 'loser_name', 'hand': 'loser_hand', \
                        'ht': 'loser_ht', 'year_of_birth': 'loser_age'}

# SUPPORT
CONT,LANG = 0,1
MATCH, TOURNAMENT, DATE, PLAYER, GEO = 0, 1, 2, 3, 4













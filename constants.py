################
### PATHs IN ###
################
DIR_IN = "./data/"
PATH_TENNIS = DIR_IN+"tennis.csv"
PATH_MALE_PLAYERS = DIR_IN+"male_players.csv"
PATH_FEMALE_PLAYERS = DIR_IN+"female_players.csv"
PATH_GEO = DIR_IN+"countries.csv"
PATH_LANG = DIR_IN+"_country_list.csv"

#################
### PATHs OUT ###
#################
DIR_OUT = "./tmp/"
PATH_TAB_MATCH = DIR_OUT+"match.csv"
PATH_TAB_TOURNAMENT = DIR_OUT+"tournament.csv"
PATH_TAB_DATE = DIR_OUT+"date.csv"
PATH_TAB_GEO = DIR_OUT+"geography.csv"
PATH_TAB_PLAYER = DIR_OUT+"player.csv"
ALL_PATHS_TABS = [PATH_TAB_MATCH,PATH_TAB_TOURNAMENT,PATH_TAB_DATE,PATH_TAB_PLAYER,PATH_TAB_GEO]
NTABS = 5

######################
### TABLE FEATURES ###
######################
MATCH_FEAT_TYPE = { "tourney_id": str, "match_id":str, "winner_id":int, "loser_id":int, "score":str, "best_of":int,\
                    "round":str, "minutes":int,"w_ace":int,"w_df":int, "w_svpt":int, "w_1stIn":int, "w_1stWon":int,\
                    "w_2ndWon":int, "w_SvGms":int, "w_bpSaved":int, "w_bpFaced":int, "l_ace":int, "l_df":int,\
                    "l_svpt":int, "l_1stIn":int, "l_1stWon":int, "l_2ndWon":int, "l_SvGms":int, "l_bpSaved":int,\
                    "l_bpFaced":int, "winner_rank":int,"winner_rank_points":int,"loser_rank":int,"loser_rank_points":int}

TOURN_FEAT_TYPE = {"tourney_id":str, "date_id":int,"tourney_name":str, "surface":str, "draw_size":int, "tourney_level":str,\
                   "tourney_spectators":int, "tourney_revenue":float}

DATE_FEAT_TYPE = {"date_id":int, "day":int, "month":int, "year":int, "quarter":int}

PLAYER_FEAT_TYPE = {"player_id":int, "country_id":str, "name":str, "sex":str, "hand":str, "ht":int, "year_of_birth":int}

GEO_FEAT_TYPE = {"country_ioc":str, "continent":str, "language":str}

ALL_TABS_FEATS = [MATCH_FEAT_TYPE.keys(),TOURN_FEAT_TYPE.keys(),DATE_FEAT_TYPE.keys(),PLAYER_FEAT_TYPE.keys(),GEO_FEAT_TYPE.keys()]

###############################################################
### REFERENCES TO PLAYER ATTRIBUTE NAMES (WINNER AND LOSER) ###
###############################################################
W_PLAYER_TABLE_FEATS = {'player_id': 'winner_id', 'country_id': 'winner_ioc', 'name': 'winner_name', 'hand': 'winner_hand', \
                        'ht': 'winner_ht', 'year_of_birth': 'winner_age'}

L_PLAYER_TABLE_FEATS = {'player_id': 'loser_id', 'country_id': 'loser_ioc', 'name': 'loser_name', 'hand': 'loser_hand', \
                        'ht': 'loser_ht', 'year_of_birth': 'loser_age'}



###########
# SUPPORT #
###########
CURR_YEAR = 2021
WIN,LOS = 0,1
CONTINENT, LANGUAGE = 0,1
MATCH, TOURNAMENT, DATE, PLAYER, GEO = 0, 1, 2, 3, 4
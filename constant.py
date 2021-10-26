# Input files
PATH_TENNIS_CSV = "./data/tennis.csv"
PATH_MALE_PLAYERS = "./data/male_players.csv"
PATH_FEMALE_PLAYERS = "./data/female_players.csv"
PATH_GEO = "./data/countries.csv"

# Output files
ALL_TABLES_PATH = ["./tmp/match.csv","./tmp/tournament.csv","./tmp/date.csv","./tmp/player.csv","./tmp/geography.csv"]

# Features of fact schema tables

MATCH_TABLE_FEATS = ['match_id', 'tourney_id', 'winner_id', 'loser_id', 'score', 'best_of', 'round', 'minutes', \
                     'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced', \
                     'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced', \
                     'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points']

TOURNAMENT_TABLE_FEATS = ['tourney_id', 'date_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level', \
                          'tourney_spectators', 'tourney_revenue']

DATE_TABLE_FEATS = ['date_id', 'day', 'month', 'year', 'quarter']

PLAYER_TABLE_FEATS = ['player_id', 'country_id', 'name', 'sex', 'hand', 'ht', 'year_of_birth']

GEO_TABLE_FEATS = ['country_ioc', 'continent', 'language']

TABLES_FEATS_LIST = [MATCH_TABLE_FEATS, TOURNAMENT_TABLE_FEATS, DATE_TABLE_FEATS, PLAYER_TABLE_FEATS, GEO_TABLE_FEATS]

W_PLAYER_TABLE_FEATS = {'player_id': 'winner_id', 'country_id': 'winner_ioc', 'name': 'winner_name', 'hand': 'winner_hand', \
                        'ht': 'winner_ht', 'year_of_birth': 'winner_age'}

L_PLAYER_TABLE_FEATS = {'player_id': 'loser_id', 'country_id': 'loser_ioc', 'name': 'loser_name', 'hand': 'loser_hand', \
                        'ht': 'loser_ht', 'year_of_birth': 'loser_age'}

D_WL = [W_PLAYER_TABLE_FEATS,L_PLAYER_TABLE_FEATS]




#KEYS = ['match_id','tourney_id','date_id','player_id','country_ioc']

NTABS = 5
MATCH, TOURNAMENT, DATE, PLAYER, GEO = 0, 1, 2, 3, 4
WIN, LOS = 0,1
CONTINENT,LANG = 0,1





#IN, OUT = 0,1
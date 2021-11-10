import pandas as pd
import numpy as np
from constants import *

pd.set_option('display.max_columns', None)

match = pd.read_csv(PATH_TAB_MATCH)
tourn = pd.read_csv(PATH_TAB_TOURNAMENT)
date = pd.read_csv(PATH_TAB_DATE)
player = pd.read_csv(PATH_TAB_PLAYER)
geo = pd.read_csv(PATH_TAB_GEO)


### DATE tab
# La table non presenta ne valori anomali ne missin values. La chiave primaria contiene tutte le date dal 2016 al 2021.
# Gli altri attributi sono stati derivati dalla chiave e quindi sono regolari.
print("Data.csv file ready!")

# ### Tournament Tab
# La table contiene alcuni missing values nell'attributo 'surface', sostituiti con il valore più frequente. Inoltre,
# abbiamo controllato che gli attributi non numerici non contenesseto stringhe non regolari (ie. stringhe composte da un
# char soltanto o blank values)
tourn.fillna(value={'surface':tourn['surface'].mode()[0]}, inplace=True)
print("Tournament.csv file ready!")

### Player
# La tabella contiene diversi attributi con valori mancanti. Gli attributi a valori discreti sono stati sostituiti con
# la moda, mentre i valori numerici (year of birth) considerando la mediana. Lo scoping delle stringhe non ha rilevato
# stringhe anomale troppo corte.
player.fillna(value={'sex':player['sex'].mode()[0]}, inplace=True)
player.fillna(value={'hand':player['hand'].mode()[0]}, inplace=True)
player.fillna(value={'ht':player['ht'].mode()[0]}, inplace=True)
player.fillna(value={'year_of_birth':player['year_of_birth'].median()}, inplace=True)
htFMedian = int(player[player['sex']=='F'][['ht']].median())
player.loc[player.name == 'Kamilla Rakhimova', 'ht'] = htFMedian
print("Player.csv file ready")

### Match Tab
# La table contiene molti attributi numerici con valori mancanti, opportunamente sostituiti considerando la mediana.
# Inoltre, abbiamo selettivamente sostituito alcuni valori anomali:
#  - alcune partite hanno una durata nulla (0 minutes) nonostante lo score indichi una partita completa (non annullata
#    e nessun ritirato - RET)
#  - ht di 2cm (errori di battitura)
match.fillna(value={'score':match['score'].mode()[0]}, inplace=True)
colsToFill = match.columns[7:]
for col in colsToFill:
    match.fillna(value={col:match[col].median()}, inplace=True)
print("Match.csv file ready!")

### Geography Tab
# Abbiamo importato due ulteriori csv files per derivare i continenti e le lingue che hanno avevano un valore. Ulteriori
# valori rimanenti sono stati corretti selettivamente.

# SOSTITUZIONE DEI CONTINENTI MANCANTI

# Cancello il continente 'unknown' e lo rendo nullo
geo['continent'].replace('Unknown',np.NaN,inplace=True)

# Import il csv file di supporto con continenti aggiuntivi e faccio il merge con la geo table
cont = pd.read_csv(PATH_CONTINENT)
cont = cont[["Three_Letter_Country_Code","Continent_Name"]]
cont['Continent_Name'] = cont['Continent_Name'].replace({'North America': 'America','South America':'America'}, regex=True)
cont.drop_duplicates(subset=['Three_Letter_Country_Code'], keep='last',inplace=True)
geo=geo.merge(cont,how='left',left_on='country_ioc',right_on='Three_Letter_Country_Code')

# Aggiorno i nan values e correggo selettivamente i rimanenti
geo['continent'].fillna(geo['Continent_Name'],inplace=True)
geo['continent'].fillna('Africa',inplace=True)
del geo['Continent_Name']
del geo["Three_Letter_Country_Code"]

# SOSTITUZIONE DELLE LINGUE MANCANTI

# importo il csv di supporto e lo mergio alla table
lang = pd.read_csv(PATH_LANG_2, encoding = "ISO-8859-1")
lang = lang[["alpha3","name"]]
lang['alpha3']=lang['alpha3'].str.upper()
lang = lang[~lang['alpha3'].isna()]
lang.drop_duplicates(subset=['alpha3'], keep='last', inplace=True)
geo=geo.merge(lang,how='left',left_on='country_ioc',right_on='alpha3')

# Sostituisco le lingue mancanti prendendole dal csv importato
geo['language'].fillna(geo['name'],inplace=True)
del geo['alpha3']
del geo['name']

# Correggo manualmente le lingue residue
# Le lingue residue le correggo manualmente
geo.loc[geo.country_ioc == 'RUS', 'language'] = 'Russian'
geo.loc[geo.country_ioc == 'FRA', 'language'] = 'French'
geo.loc[geo.country_ioc == 'URU', 'language'] = 'Spanish'
geo.loc[geo.country_ioc == 'CUB', 'language'] = 'Spanish'
geo.loc[geo.country_ioc == 'CAN', 'language'] = 'English'
geo.loc[geo.country_ioc == 'USA', 'language'] = 'English'
geo.loc[geo.country_ioc == 'GBR', 'language'] = 'English'
geo.loc[(geo.continent == 'Africa') & (geo.language == ' '), 'language'] = 'Arabic'
geo.loc[(geo.continent == 'Africa') & (geo.language.isnull()),'language'] = 'Arabic'
geo.loc[(geo.language.isnull()) | (geo.language == ' '), 'language'] = 'English'
print("Geography.csv file ready!")

# Rieseguo il casting perchè abbiamo notato che la pd.read_csv modifica i tipi (da int a float) precedentemente settati
# senza l'ausilio della libreria pandas
match = match.astype(MATCH_FEAT_TYPE)
tourn = tourn.astype(TOURN_FEAT_TYPE)
date = date.astype(DATE_FEAT_TYPE)
player = player.astype(PLAYER_FEAT_TYPE)
geo = geo.astype(GEO_FEAT_TYPE)

# Esporto i csv privi di missing values pronti per essere caricati
match.to_csv(PATH_TAB_MATCH, index=False)
tourn.to_csv(PATH_TAB_TOURNAMENT, index=False)
date.to_csv(PATH_TAB_DATE, index=False)
player.to_csv(PATH_TAB_PLAYER, index=False)
geo.to_csv(PATH_TAB_GEO, index=False)
print("All csv tables are been exported!")
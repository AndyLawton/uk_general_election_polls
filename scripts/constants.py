from numpy import nan

poll_database_lcn = 'poll_database/'
feather_location = f'{poll_database_lcn}feathers/'
csv_location = f'{poll_database_lcn}csvs/'
json_location = f'{poll_database_lcn}jsons/'
excel_location = f'{poll_database_lcn}excels/'

wikipedia_links = {

    # '1945': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1945_United_Kingdom_general_election', #Will prob fail
    # '1950': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1950_United_Kingdom_general_election',
    # '1951': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1951_United_Kingdom_general_election',
    # '1955': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1955_United_Kingdom_general_election',
    # '1959': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1959_United_Kingdom_general_election', #Will prob fail
    # '1964': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1964_United_Kingdom_general_election',
    #'1966': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1966_United_Kingdom_general_election',



    '1974': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1974_United_Kingdom_general_elections',
    '1979': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1979_United_Kingdom_general_election',
    '1983': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1983_United_Kingdom_general_election',
    '1987': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1987_United_Kingdom_general_election',
    '1992': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1992_United_Kingdom_general_election',
    '1997': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_1997_United_Kingdom_general_election',
    '2001': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2001_United_Kingdom_general_election',
    '2005': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2005_United_Kingdom_general_election',
    '2010': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2010_United_Kingdom_general_election',
    '2012': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_United_Kingdom_general_election'
            '_(2010%E2%80%932012) ',
    '2015': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2015_United_Kingdom_general_election',
    '2017': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2017_United_Kingdom_general_election',
    '2019': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2019_United_Kingdom_general_election',
    'next': 'https://en.wikipedia.org/wiki/Opinion_polling_for_the_2024_United_Kingdom_general_election',
}

poll_info_columns = [
    'dates', 'year',
    'area',
    'pollster', 'pollster_client', 'client',
    'sample_size',
]
major_parties = [
    'labour',
    'conservative',
    'reform_uk',
    'liberal_democrat',
]
minor_parties = [
    'green',
    'alliance',
    'brexit_party',
    'change_uk',
    'liberal',
    'plaid_cymru',
    'scottish_national_party',
    'social_democratic_party',
    'united_kingdom_independence_party',
    'reclaim_party',
]
party_columns = major_parties + minor_parties
final_columns = [
    'others',
    'lead',
    'lead_value',
]
column_names = poll_info_columns + party_columns + final_columns

final_table_info = [
    'date_started', 'date_concluded',
    'pollster', 'client',
    'area',
    'sample_size',
]
final_column_names = final_table_info + party_columns + final_columns

replacement_values = {'?': nan, '–': nan, '—': nan, '-': nan, '*': nan, 'TBA': nan, 'Tie': 0, 'TBC': nan}

party_colors = {
    'conservative': '#0087DC',
    'labour': '#DC241F',
    'liberal_democrat': '#FAA61A',
    'alliance': '#FFD700',
    'brexit_party': '#12B6CF',
    'change_uk': '#222221',
    'green': '#6AB023',
    'liberal': '#EB7A43',
    'plaid_cymru': '#008142',
    'reform_uk': '#12B6CF',
    'scottish_national_party': '#FFFF00',
    'social_democratic_party': '#7D26CD',
    'united_kingdom_independence_party': '#70147A',
    'reclaim_party': '#012169',
}

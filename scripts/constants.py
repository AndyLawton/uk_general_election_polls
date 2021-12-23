from numpy import nan

poll_info_columns = [
    'dates', 'year',
    'area',
    'pollster', 'pollster_client', 'client',
    'sample_size',
]
major_parties = [
    'conservative',
    'labour',
    'liberal_democrat',
]
minor_parties = [
    'alliance',
    'brexit_party',
    'change_uk',
    'green',
    'liberal',
    'plaid_cymru',
    'reform_uk',
    'scottish_national_party',
    'social_democratic_party',
    'united_kingdom_independence_party',
    'reclaim_party',
]
party_columns = major_parties + minor_parties
final_columns = [
    'others',
    'lead',
]
column_names = poll_info_columns + party_columns + final_columns

final_table_info = [
    'date_started', 'date_concluded',
    'pollster', 'client',
    'area',
    'sample_size',
]
final_column_names = final_table_info + party_columns + final_columns

replacement_values = {'?': nan, '–': nan, '-': nan, '*': nan, 'TBA': nan, 'Tie': 0}



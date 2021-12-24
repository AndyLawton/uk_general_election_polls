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

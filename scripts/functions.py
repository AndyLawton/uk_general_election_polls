def others_to_json(others_field):
    from pandas import isna
    from numpy import nan
    from .renames import column_cleanup
    if isna(others_field):
        return {'others': nan}

    others_split = others_field.split(' on')

    if len(others_split) == 1:
        return {'others': others_split[0].split('%')[0].strip() + '%'}

    i = 1
    results = {}
    while len(others_split) > i:
        party_name = others_split[i - 1].split('%')[1].strip()
        if party_name in column_cleanup:
            party_name = column_cleanup[party_name]
        result = others_split[i].split('%')[0].strip()
        results[party_name] = result + '%'
        i += 1
    return results


def split_date(poll_dates, table_year):
    poll_dates = poll_dates.replace('–', '-').replace('Pre-', '').strip()
    date_parts = poll_dates.split(" ")

    # For any polls outside the correct year (2019 GE for example)
    for part in date_parts:
        if len(part) == 4 and (part.startswith('19') or part.startswith('20')):
            table_year = part
            date_parts.remove(part)

    poll_dates = ' '.join(date_parts)
    if ' ' not in poll_dates:
        # Poll dates showing month only
        start_date = end_date = f'{table_year}-{poll_dates}-1'
    else:
        if '-' not in poll_dates:
            day, month = poll_dates.split(' ')
            start_date = end_date = f'{table_year}-{month[0:3]}-{day}'
        else:
            start, end = poll_dates.split('-')
            start = start.strip()
            end = end.strip()
            day, month = end.split(' ')
            end_date = f'{table_year}-{month[0:3]}-{day}'
            if ' ' in start:
                day, month = start.split(' ')
            else:
                day = start
            start_date = f'{table_year}-{month[0:3]}-{day}'
    return start_date, end_date


def set_pollster_client(pollster, client, pollster_client):
    from pandas import isna
    from scripts.renames import pollster_cleanup

    if not isna(pollster_client):
        pollster_client_split = pollster_client.split('/')
        pollster = pollster_client_split[0]
        if len(pollster_client_split) > 1:
            client = pollster_client_split[1]

    if isna(pollster):
        pollster = 'NA'

    if '/' in pollster:
        pollster, client = pollster.split('/')
    if 'general election' in pollster.lower():
        pollster = 'General Election'
    #pollster = pollster.replace('(MRP)', '')
    #pollster = pollster.replace('(SRP)', '')
    pollster = pollster.strip()
    if 'Archive' in pollster:
        pollster = pollster.split('Archive')[0].strip()
    if pollster in pollster_cleanup:
        pollster = pollster_cleanup[pollster]
    if not isna(client):
        client = client.strip()

    return pollster, client


def format_lead(row):
    from pandas import isna
    from .constants import party_columns
    if isna(row.labour):
        return '', 0
    party_columns = list( set.intersection(set(party_columns), set(row.index)))
    largest_share = row[party_columns].max()
    if len(row[row == largest_share]) > 1:
        return 'Tie', 0
    second = sorted([a for a in row[party_columns] if not isna(a)], reverse=True)[1]
    party_name = row[row == largest_share].index[0]
    return f'{party_name:.3s}+{largest_share - second:.1f}', largest_share - second


def poll_result_cleanup(poll_result_column):
    # Removes party unknown results, imprecise results and convert to numeric
    from .constants import replacement_values
    from pandas import to_numeric
    poll_result_column = poll_result_column.str.strip('%').str.strip('<').str.strip('>')
    poll_result_column = poll_result_column.replace(replacement_values)
    return to_numeric(poll_result_column)


def poll_cleanup(poll_df):
    from .constants import column_names, party_columns, final_column_names
    from pandas import json_normalize, to_datetime, offsets
    from numpy import nan

    # Remove All Wikipedia Citations
    for column in column_names:
        poll_df[column] = poll_df[column].map(str)
        poll_df[column] = poll_df[column].str.replace(r"\[.*\]", "", regex=True)
        poll_df.loc[poll_df[column] == 'nan', column] = nan

    for party in party_columns:
        poll_df[party] = poll_result_cleanup(poll_df[party])

    # Split out other party column into individual party results
    other_parties = json_normalize(poll_df['others'].map(others_to_json))
    other_parties.index = poll_df.index
    for party in other_parties.columns:
        other_parties[party] = poll_result_cleanup(other_parties[party])

        if party not in poll_df.columns or party == 'others':
            poll_df[party] = other_parties[party]
        else:
            poll_df[party] = poll_df[party].add(other_parties[party], fill_value=0)

    # Cleanup lead (Not in use, creating own lead column)
    # poll_df['lead'] = poll_result_cleanup(poll_df['lead'])

    # Set Dates
    poll_df[['date_started', 'date_concluded']] = poll_df.apply(
        lambda x: split_date(x.dates, x.year), axis=1, result_type='expand')
    poll_df['date_started'] = to_datetime(poll_df['date_started'])
    poll_df['date_concluded'] = to_datetime(poll_df['date_concluded'])
    poll_df.drop(columns=['dates', 'year'], inplace=True)

    poll_df.loc[
        poll_df.date_concluded<poll_df.date_started,
        'date_started'] = poll_df.loc[
                                  poll_df.date_concluded<poll_df.date_started,
                                  'date_started'] - offsets.DateOffset(years=1)

    # Cleanup Pollster and Client
    poll_df[['pollster', 'client']] = poll_df.apply(
        lambda x: set_pollster_client(x.pollster, x.client, x.pollster_client), axis=1, result_type='expand')
    poll_df.drop(columns=['pollster_client'], inplace=True)

    # Removes double General Election results - from multiple wiki pages.
    poll_df.drop_duplicates(
        subset=['pollster', 'date_started', 'date_concluded', 'conservative', 'labour', 'liberal_democrat', 'green'],
        keep='last', inplace=True)

    # Replaces lead column with party+x, lead_value columns added for value calculations
    poll_df[['lead', 'lead_value']] = poll_df.apply(format_lead, axis=1, result_type='expand')

    # Sort by date and resets index
    poll_df.sort_values(by='date_concluded', ascending=False, inplace=True)
    poll_df.reset_index(drop=True, inplace=True)

    return poll_df[final_column_names]

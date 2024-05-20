#!/usr/bin/env python
# coding: utf-8

import traceback

job_name = 'Westminster Polling Summary 1.0'


def main():
    web_files_location = 'html_outputs/'
    poll_db_location = 'poll_database/'

    import getopt
    import os
    import sys
    import pandas as pd
    from shutil import copy
    from dateutil.relativedelta import relativedelta
    from scripts.downloader import fetch_all_polls
    from scripts.constants import major_parties

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:w:",
                                   ["help", "db-location", "web-location"])
    except getopt.GetoptError as err:
        print(err)
        print('main.py --db-location <folder> --web-location <folder>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == ["-h", "--help"]:
            print('main.py --db-location <folder> --web-location <folder>')
            sys.exit()
        elif opt in ["-d", "--db-location"]:
            poll_db_location = arg
        elif opt in ["-w", "--web-location"]:
            if arg != web_files_location:
                copy(f'{web_files_location}/opinion_polling.php', f'{arg}/opinion_polling.php')
                copy(f'{web_files_location}/favicon.ico', f'{arg}/favicon.ico')
            web_files_location = arg

    if not os.path.isdir(poll_db_location):
        os.mkdir(poll_db_location)
    if not os.path.isdir(web_files_location):
        os.mkdir(web_files_location)

    all_polls = fetch_all_polls(cleanup=True, refresh=False)

    all_polls.to_csv(f'{poll_db_location}/poll_database.csv', index=False)
    all_polls.to_excel(f'{poll_db_location}/poll_database.xlsx', index=False)
    all_polls.to_json(f'{poll_db_location}/poll_database.json', index=False, orient='split')

    reporting_date = 'date_started'

    most_recent_date = all_polls[reporting_date].max()
    one_year_polls = all_polls[
        all_polls[reporting_date] >= (most_recent_date + relativedelta(months=-17)).replace(day=1)].copy()

    pollsters_latest = one_year_polls.groupby('pollster').nth(0).reset_index(drop=False)

    top_five = {'Ipsos MORI': 100,
                'Opinium': 79,
                'YouGov': 77,
                'Verian': 69,
                'Number Cruncher Politics': 61,
                'Survation': 59,
                'Panelbase': 57,
                'Deltapoll': 46,
                'BMG Research': 44,
                'FocalData': 39,
                'ICM Research': 35,
                'Savanta': 34,
                'Find Out Now': 34*0.3,  # Ludicrous Local Election Polling
                'Redfield & Wilton Strategies': 34*.75,
                'Techne UK': 34*.75,
                'JL Partners Polls': 34*.75,
                'PeoplePolling': 34*0.1,  # Huge outlier without caring for fundamental polling principles
                'We Think': 34*.75,
                'More in Common': 34*.75,
                'Whitestone Insight': 34*.75,
                'Lord Ashcroft Polls': 34,
                }

    top_two = {'Ipsos MORI': 100,
               'Survation': 85,
               'Verian': 85,
               'Panelbase': 74,
               'Number Cruncher Politics': 71,
               'Opinium': 71,
               'YouGov': 67,
               'Deltapoll': 50,
               'FocalData': 42,
               'BMG Research': 39,
               'Savanta': 29,
               'ICM Research': 27,
               'Find Out Now': 34*0.3,  # Ludicrous Local Election Polling
               'Redfield & Wilton Strategies': 34*.75,
               'Techne UK': 34*.75,
               'JL Partners Polls': 34*.75,
               'PeoplePolling': 34*0.1,  # Huge outlier without caring for fundamental polling principles
               'We Think': 34*.75,
               'More in Common': 34*.75,
               'Whitestone Insight': 34*.75,
               'Lord Ashcroft Polls': 34,
               }

    recency_weights = {
        -1: 100,
        5: 100,
        14: 70,
        28: 5,
        90: 0
    }

    def get_recency_weight(poll_date, current_date, return_category=False):
        days_since_poll = (current_date - poll_date).days
        days_start_of_range = weight_start_of_range = 0
        category = 0
        for day, weight in recency_weights.items():
            category += 1
            if days_since_poll > day:
                days_start_of_range = day
                weight_start_of_range = weight
            else:
                percent_through_range = (days_since_poll - days_start_of_range)/(day - days_start_of_range)
                full_weight = weight_start_of_range - ((weight_start_of_range - weight)*percent_through_range)
                if return_category:
                    return category - 2
                else:
                    return full_weight
        if return_category:
            return category - 1
        else:
            return 0

    def get_pollster_weight(pollster):
        if pollster not in top_two:
            return 0
        top_five_score = top_five[pollster]
        top_two_score = top_two[pollster]
        pollster_w = (3*top_two_score + 2*top_five_score + 100)/6
        return pollster_w

    pollsters_latest['recency_weight'] = pollsters_latest[reporting_date].apply(get_recency_weight,
                                                                                current_date=most_recent_date)
    pollsters_latest['pollster_weight'] = pollsters_latest['pollster'].apply(get_pollster_weight)
    pollsters_latest['poll_weight'] = pollsters_latest['pollster_weight']*(pollsters_latest['recency_weight']/100)

    current_average = pd.DataFrame(columns=major_parties + ['lead'], index=['Polling Average'])
    lead_party = ''
    max_vote_share = 0
    second_vote_share = 0
    for party in major_parties:
        party_vote_share = pollsters_latest[party].dot(pollsters_latest['poll_weight'])/pollsters_latest[
            'poll_weight'].sum()
        if party_vote_share > max_vote_share:
            second_vote_share = max_vote_share
            max_vote_share = party_vote_share
            lead_party = party
        else:
            if party_vote_share > second_vote_share:
                second_vote_share = party_vote_share
        current_average.loc['Polling Average', party] = party_vote_share
        # current_average.loc['Polling Average', party] = f'{party_vote_share:.1f}%'
    # current_average.loc['Polling Average', 'lead'] = f'{lead_party:.3s}+{max_vote_share - second_vote_share:.1f}%'
    current_average.loc['Polling Average', 'lead_value'] = max_vote_share - second_vote_share

    one_year_polls['poll_month'] = one_year_polls[reporting_date].apply(lambda x: x.replace(day=1))

    pollster_monthly_summary = one_year_polls.groupby(['poll_month', 'pollster'])[major_parties].agg(['mean', 'count'])
    pollster_monthly_summary.columns = [x if i == 0 else f'count{major_parties.index(x)}' for x in major_parties for i
                                        in
                                        range(0, 2)]
    pollster_monthly_summary.drop(columns=[f'count{major_parties.index(x)}' for x in major_parties][1:], inplace=True)
    pollster_monthly_summary.rename(columns={"count0": "count"}, inplace=True)

    agg_info = {x: ['mean'] for x in major_parties}
    agg_info['count'] = ['count', 'sum']
    monthly_summary = pollster_monthly_summary.reset_index().groupby(['poll_month']).agg(agg_info)
    monthly_summary.columns = major_parties + ['pollster_count', 'poll_count']

    all_polls.loc[all_polls.date_concluded < all_polls.date_started, 'date_started'] - pd.offsets.DateOffset(years=1)

    from scripts.functions import format_lead

    monthly_summary[['lead', 'lead_value']] = monthly_summary.apply(format_lead, axis=1, result_type='expand')

    def result_to_opacity(result, range_min, range_max):
        result_range = range_max - range_min
        result_percent = (result - range_min)/result_range
        result_256 = int(result_percent*255)
        return f'{result_256:02x}'

    def add_background_colour_to_cells(df, lead_only=False):
        from scripts.constants import party_colors, major_parties
        background_df = df.copy()
        max_party_lead = background_df['lead_value'].max()

        for party in major_parties:
            color = party_colors[party]
            party_max = background_df[party].max()
            party_min = background_df[party].min() - 0.5
            if not lead_only:
                background_df[party] = background_df[party].apply(
                    lambda x: f'background-color: {color}{result_to_opacity(x, party_min, party_max)}'
                )
            else:
                background_df[party] = ''
            party_in_lead_mask = df[party] == df[major_parties].max(axis=1)
            background_df.loc[party_in_lead_mask, 'lead_value'] = df['lead_value'].apply(
                lambda x: f'background-color: {color}{result_to_opacity(x, 0, max_party_lead)}'
            )

        if reporting_date in background_df.columns:
            background_df[reporting_date] = background_df[reporting_date].apply(get_recency_weight,
                                                                                current_date=most_recent_date)
            background_df[reporting_date] = background_df[reporting_date].apply(
                lambda x: f'background-color: #A9D08E{result_to_opacity(x, 0, 100)}'
            )

        for column in background_df.columns:
            if not (column in major_parties or column in ['lead_value', reporting_date]):
                background_df[column] = ''
        return background_df

    def polls_to_html(dataframe, title, highlight_party_columns=True, precision=0):
        dataframe.index.name = 'id'
        table_id = '_'.join(title.split(' ')).lower()

        from pandas.io.formats.style import Styler
        # styler = dataframe.style
        styler = Styler(dataframe, uuid=table_id, cell_ids=True)

        styler.apply(add_background_colour_to_cells, axis=None,
                     lead_only=not (highlight_party_columns))

        styler.format({
            "pollster": lambda x: f"{x}",
            "pollster_count": lambda x: f"{x}",
            "poll_count": lambda x: f"{x}",
            "conservative": lambda x: f"{x:.{precision}f}%",
            "labour": lambda x: f"{x:.{precision}f}%",
            "liberal_democrat": lambda x: f"{x:.{precision}f}%",
            # "green": lambda x: f"{x:.{precision}f}%",
            # "reform_uk": lambda x: f"{x:.{precision}f}%",
            "lead_value": lambda x: f"{x:.{precision}f}%",
            reporting_date: lambda x: f"{x:%d-%b}",
            'poll_month': lambda x: f"{x:%b-%y}",
            'poll_weight': lambda x: f"{x:.0f}",
        })

        styler.set_table_attributes(f'id="{table_id}"')
        styler.hide_index()

        # classes = pd.DataFrame([['_'.join(x.split(' ')).lower() for x in dataframe.columns]]
        #                        , index=dataframe.index, columns=dataframe.columns)
        #
        # styler.set_td_classes(classes)

        # styler.set_caption(title)
        styler.set_properties(**{'min-width': '10px', 'font-size': '12pt', 'text-align': 'center'})

        caption_format = {'selector': 'caption',
                          'props': [('text-align', 'center'), ('font-size', '20pt'), ('color', 'black'),
                                    ('padding-bottom', '15')]}
        all_cells = {'selector': '', 'props': [('margin', '0 auto'), ('width', '100%')]}
        date_col = {'selector': '.col0', 'props': [('text-align', 'left')]}

        styles = [all_cells, date_col, caption_format]

        if 'poll_weight' in dataframe.columns:
            styles.append({'selector': '.col2', 'props': [('color', '#AAA')]})

        df_as_html = styler.set_table_styles(styles).render()

        for col in range(0, len(dataframe.columns)):
            df_as_html = df_as_html.replace(f'col{col}', dataframe.columns[col])

        df_as_html = (df_as_html
                      .replace('>poll_count', '>Polls')
                      .replace('>pollster_count', '>Pollsters')
                      .replace('>conservative', '>Conservatives')
                      .replace('>labour', '>Labour')
                      .replace('>liberal_democrat', '>Lib Dem')
                      .replace('>lead_value', '>Lead')
                      .replace(f'>{reporting_date}', '>Date')
                      .replace('>poll_month', '>Month')
                      .replace('>pollster', '>Pollster')
                      .replace('>poll_weight', '>w')
                      )
        return df_as_html

    display_columns = [reporting_date, 'pollster', 'conservative', 'labour', 'liberal_democrat',, 'lead_value']
    top_25_html = polls_to_html(all_polls[display_columns][0:25], title='Last 25 Polls')

    display_columns = ['pollster', reporting_date, 'poll_weight', 'conservative', 'labour', 'liberal_democrat',
                       'lead_value']
    df = pollsters_latest.sort_values(by='poll_weight', ascending=False)[display_columns]
    pollsters_recent = polls_to_html(df, title='Latest Polls', highlight_party_columns=False)

    display_columns = ['poll_month', 'pollster_count', 'poll_count', 'conservative', 'labour', 'liberal_democrat',
                       'lead_value']
    df = monthly_summary.reset_index()[display_columns].iloc[:0:-1]
    monthly_averages = polls_to_html(df, title='Monthly Poll Average', highlight_party_columns=True, precision=1)

    polling_average = polls_to_html(current_average[['conservative', 'labour', 'liberal_democrat', 'lead_value']],
                                    title='Polling Average', highlight_party_columns=False, precision=1)

    with open(f'{web_files_location}/top_25.html', 'w') as f:
        f.write(top_25_html)
    with open(f'{web_files_location}/pollsters_recent.html', 'w') as f:
        f.write(pollsters_recent)
    with open(f'{web_files_location}/monthly_averages.html', 'w') as f:
        f.write(monthly_averages)
    with open(f'{web_files_location}/polling_average.html', 'w') as f:
        f.write(polling_average)

    from scripts.constants import party_colors, major_parties
    import matplotlib.pyplot as plt
    from numpy import arange

    fig = plt.figure(figsize=(15, 3))
    fig.set_facecolor('white')
    ax = plt.gca()

    # monthly_summary[major_parties[:2]][1:].plot(
    #     ax=ax,
    #     ylim=[30, 45],
    #     color=party_colors,
    #     linewidth=3
    # )
    for party in major_parties[:2]:
        plt.plot_date(
            x=monthly_summary.index[1:],
            y=monthly_summary[party][1:],
            fmt='-',
            color=party_colors[party],
            linewidth=4)

        ax.fill_between(monthly_summary.index[1:], monthly_summary[party][1:],
                        monthly_summary[major_parties[:2]].min(axis=1)[1:], color=party_colors[party], alpha=0.2)
    ax.set_yticks(arange(25, 51, 5), minor=False)
    major_locator = plt.matplotlib.dates.DayLocator([1])
    major_fmt = plt.matplotlib.dates.DateFormatter('%b-%y')

    ax.xaxis.set_major_locator(major_locator)
    ax.xaxis.set_major_formatter(major_fmt)

    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, p: f'{x/100:.0%}'))

    plot_title = 'Opinion Polling Trend'
    plt.title(plot_title)

    source = 'Source: Wikipedia - Opinion polling for the next United Kingdom general election'
    plt.annotate(source, (1, 0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top', ha='right')
    fig.savefig(f'{web_files_location}/monthly_trend.png', bbox_inches='tight', pad_inches=0.2)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'ERROR {e} {traceback.format_exc()}')

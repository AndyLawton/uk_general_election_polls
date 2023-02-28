from requests import get
from bs4 import BeautifulSoup
from os.path import isfile
from pandas import read_html, read_feather, DataFrame, concat
from numpy import nan
from .constants import wikipedia_links, feather_location
from .renames import column_cleanup


def fetch_1974_oct(refresh=False):
    page_feather_location = f'{feather_location}1974_oct.feather'
    if refresh or not isfile(page_feather_location):
        page = get(wikipedia_links['1974'])
        soup = BeautifulSoup(page.content, "html.parser")
        table_html = soup.find(id='October_general_election').find_next('table')
        table = read_html(str(table_html))[0]
        table.columns = [column_cleanup[a] for a, b in table.columns]
        table['year'] = '1974'
        table.to_feather(page_feather_location)
    else:
        table = read_feather(page_feather_location)
    return table


def fetch_page(url, ge_year, refresh=False):
    page_feather_location = f'{feather_location}{ge_year}.feather'
    if refresh or not isfile(page_feather_location) or ge_year == 'next':
        page = get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        toc = soup.find_all("ul", {"class": "vector-toc-list"})[1]
        level2 = toc.find_all("li", {"class": "vector-toc-level-2"})
        level2_links = [x.find('a')['href'] for x in level2]
        years = [x.replace('#', '') for x in level2_links if len(x) == 5]
        if len(years) == 0:
            level1 = toc.find_all("li", {"class": "toclevel-1"})
            level1_links = [x.find('a')['href'] for x in level1]
            years = [x.replace('#', '') for x in level1_links if len(x) == 5]
        page_df = DataFrame()
        for year in years:
            if ge_year == '2015' and year in ['2010', '2011', '2012']:
                continue
            table_html = soup.find(id=year).find_next('table')
            table = read_html(str(table_html))[0]
            if len(table) < 20 and year not in ['2002', '2001', '1974', '1970'] and ge_year != 'next':
                break
            # Fix for merged Other cell
            if ('Others', 'Others') in table.columns:
                other_left = list(table.columns)[list(table.columns).index(('Others', 'Others')) - 1]
                contains_other_mask = table[other_left].fillna('-').str.contains('Other on')
                table.loc[contains_other_mask, other_left] = nan

                from pandas import to_numeric
                from .constants import replacement_values
                still_contains_other_mask = (
                        (table[other_left] == table[('Others', 'Others')]) &
                        (to_numeric(
                            table[other_left].str.strip('%').str.strip('<').str.strip('>').replace(
                                replacement_values)
                            , errors='coerce') > 8)
                )
                table.loc[still_contains_other_mask, other_left] = nan

            table.columns = [column_cleanup[a] for a, b in table.columns]
            table['year'] = year
            page_df = concat([page_df, table], axis=0, ignore_index=True)
        # Fix for int/string sample sizes
        if 'sample_size' in page_df.columns:
            page_df['sample_size'] = page_df['sample_size'].astype(str)
        page_df.to_feather(page_feather_location)
    else:
        page_df = read_feather(page_feather_location)
    return page_df


def fetch_tables(refresh=False):
    all_election_tables = [fetch_1974_oct(refresh=refresh)]
    for ge_year, url in wikipedia_links.items():
        all_election_tables.append(fetch_page(url, ge_year, refresh=refresh))
    return all_election_tables


def fetch_all_polls(cleanup=False, refresh=False):
    from .constants import column_names
    election_tables = fetch_tables(refresh=refresh)
    all_polls = DataFrame(columns=column_names)
    for polling_results in election_tables:
        all_polls = concat([all_polls, polling_results], axis=0, ignore_index=True)
    all_polls = all_polls[
        ~((all_polls['lead'] == all_polls['conservative']) & (all_polls['lead'] == all_polls['labour']))]

    if cleanup:
        from .functions import poll_cleanup
        return poll_cleanup(all_polls)
    else:
        return all_polls

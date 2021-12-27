import pandas as pd


def fetch_tables():
    import requests
    from bs4 import BeautifulSoup
    from numpy import nan
    from . import wiki_links as w

    election_tables = []
    page = requests.get(w.url_1974)
    soup = BeautifulSoup(page.content, "html.parser")
    election_tables.append(('1974', pd.read_html(str(soup.find(id='October_general_election').find_next('table')))[0]))
    for election in w.general_elections:
        page = requests.get(election)
        soup = BeautifulSoup(page.content, "html.parser")
        toc = soup.find(id='toc')
        level2 = toc.find_all("li", {"class": "toclevel-2"})
        level2_links = [x.find('a')['href'] for x in level2]
        years = [x.replace('#', '') for x in level2_links if len(x) == 5]
        if len(years) == 0:
            level1 = toc.find_all("li", {"class": "toclevel-1"})
            level1_links = [x.find('a')['href'] for x in level1]
            years = [x.replace('#', '') for x in level1_links if len(x) == 5]
        for year in years:
            if election == w.url_2015 and year in ['2010', '2011', '2012']:
                continue
            table = pd.read_html(str(soup.find(id=year).find_next('table')))[0]
            if len(table) < 20 and year not in ['2002', '2001', '1974', '1970']:
                break
            # Fix for merged Other cell
            if ('Others', 'Others') in table.columns:
                other_left = list(table.columns)[list(table.columns).index(('Others', 'Others')) - 1]
                contains_other_mask = table[other_left].str.contains('Other on')
                table.loc[contains_other_mask, other_left] = nan
            election_tables.append((year, table))
    return election_tables


def fetch_all_polls(cleanup=False):
    from .constants import column_names
    from .renames import column_cleanup
    election_tables = fetch_tables()
    all_polls = pd.DataFrame(columns=column_names)
    for year, polling_results in election_tables:
        table = polling_results.copy()
        table.columns = [column_cleanup[a] for a, b in table.columns]
        table['year'] = year
        all_polls = all_polls.append(table, ignore_index=True)
    all_polls = all_polls[
        ~((all_polls['lead'] == all_polls['conservative']) & (all_polls['lead'] == all_polls['labour']))]

    if cleanup:
        from .functions import poll_cleanup
        return poll_cleanup(all_polls)
    else:
        return all_polls

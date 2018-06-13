import pylast as pyl
import wikipedia as wiki
import re
import requests
import discogs_client as disc_cli
import sys
import pickle
# import transliterate

from drawer import extract_countries
from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from secret import LAST_FM_API_KEY, DISCOGS_API_KEY  # this line imports my api keys, change them to yours own

MUSIC_BRAINZ_URL = 'https://musicbrainz.org/ws/2/artist/{}?fmt=json'
LAST_FM_URL = 'https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json'
COUNTRIES = extract_countries()
ANALYSIS_DATE = datetime.now()


# Very specific abstract parser function
def summary_parser(text):
    country_occur = defaultdict(int)
    for word in text.split(' '):
        word = word.strip('(),. ').replace("\n", "")
        if word == "":
            continue
        if word[0].isupper():
            try:
                pos_country = normalize_country(word)
                if pos_country in COUNTRIES:
                    country_occur[pos_country] += 1
            except KeyError:
                pass
    return None if len(country_occur) == 0 else max(country_occur, key=lambda i: country_occur[i])


# This function implements clearing the disambiguation of country's name
# I guess it's not necessarily to explain it, because code is merely simple
def normalize_country(country):
    norm_dict = {
        'U.S.': 'United States of America',
        'US': 'United States of America',
        'USA': 'United States of America',
        'United States': 'United States of America',
        'U.K.': 'United Kingdom',
        'UK': 'United Kingdom',
        'Soviet Union': 'Russia',
        'Scotland': 'United Kingdom',
        'Wales': 'United Kingdom',
        'England': 'United Kingdom',
        'Northern Ireland': 'United Kingdom',
    }
    if country in norm_dict.keys():
        return norm_dict[country]
    return country


def wikipedia_getter(artist):
    # try:
    #     artist = transliterate.translit(artist, reversed=True)
    # except transliterate.exceptions.LanguageDetectionError:
    #     pass
    try:
        page = wiki.page(artist)
        soup = BeautifulSoup(page.html(), "html.parser")
    except wiki.DisambiguationError:
        # If wiki cannot identify page correctly (possible other meanings like Drake)
        # Then script tries to search for something like Drake (band) or Drake (singer) etc.
        # This list is extendable and may be edited without serious consequences
        possible_variants = ['band', 'singer', 'songwriter', 'compositor', 'musician', 'artist', 'performer']
        soup = None
        # It will try to search for artist's wiki page until every variant in previous list will be checked out
        # (that may take long time, you can shorten list)
        for var in possible_variants:
            page = None
            t_artist = artist + ' ({})'.format(var)
            try:
                page = wiki.page(t_artist)
                if page:
                    soup = BeautifulSoup(page.html(), "html.parser")
                    break
            except wiki.DisambiguationError:
                continue
            except wiki.PageError:
                continue
        if not soup:
            return None
    except wiki.PageError:
        # Artist's page was not found, possible variants can be printed in console by uncommenting next line
        # print('Artist\'s page not found. Here is result list:\n{}'.format(wiki.search(artist)))
        return None

    # Most common case is "summary" table about artist, which contains his hometown etc.
    # So script tries to look for it in extracted 'soup'
    info_table = soup.find("table", {"class": "infobox"})
    if info_table:
        # In some cases artist's home is noted with specific tags, so next lines try to guess which variant is correct
        origin = info_table.find("span", {"class": "birthplace"})
        if not origin:
            try:
                origin = [elem for elem in info_table(text=re.compile(r'Origin|Born|Residence'))][0].parent.findNext()
            except AttributeError:
                return None
            except IndexError:
                return None
        # Till the end of the function, script tries to identify whether was extracted string in proper way or not
        try:
            res_country = normalize_country(origin.text.split(',')[-1][1:])
        except AttributeError:
            return summary_parser(page.summary)
        if res_country in COUNTRIES:
            return res_country
        return summary_parser(page.summary)
    else:
        return summary_parser(page.summary)


def brainz_getter(mbid):
    req = requests.get(MUSIC_BRAINZ_URL.format(mbid)).json()
    try:
        if 'area' in req:
            if req['area']:
                country = normalize_country(req['area']['name'])
                if country in COUNTRIES:
                    return country
                return None
        return None
    except TypeError and KeyError:
        return None


def last_summary_getter(artist):
    req = requests.get(LAST_FM_URL.format(artist, LAST_FM_API_KEY))
    try:
        data = req.json()['artist']
    except KeyError:
        return None

    fact_country = factbox_parser(data)
    if fact_country:
        return fact_country
    if 'bio' in data:
        if 'summary' in data['bio']:
            return summary_parser(data['bio']['summary'])
    return None


def factbox_parser(jd):  # jd variable is data in json format =)
    try:
        url = jd['url']
    except KeyError:
        return None
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        facts = soup.find('p', {'class': 'factbox-summary'}).text
    except AttributeError:
        return None

    pos_country = normalize_country(facts[:(facts.find('(') - 1)].split(',')[-1][1:])
    if pos_country in COUNTRIES:
        return pos_country
    return None


# TODO: implement it somehow
def discogs_getter(artist):
    dcl = disc_cli.Client('Last.fm location retriever', user_token=DISCOGS_API_KEY)
    art = dcl.search(artist, type='artist')
    return art


def dump_data(countries, username, limit, total_scr, uncounted):
    data = {
        'countries': countries,
        'username': username,
        'limit': limit,
        'analysis_date': ANALYSIS_DATE,
        'total_scrobbles': total_scr,
        'total_countries': len(countries),
        'uncounted_amount': uncounted,
        'uncounted_percentage': int(uncounted / len(countries) * 100)
    }
    filename = r'dumps/{}_{}_{}.dat'.format(username, limit, str(ANALYSIS_DATE.time())[:8])
    with open(filename, 'wb+') as file:
        pickle.dump(data, file)
        file.close()


def get_countries(name, lim):
    try:
        net = pyl.LastFMNetwork(api_key=LAST_FM_API_KEY, username=name)
        user = net.get_user(username=net.username)
        top = user.get_top_artists(limit=lim)

    except pyl.WSError:
        sys.exit('User with {} username not found'.format(name))

    countries = dict()
    print('No\tArtist\t\tCountry\tWeight\n--------------------------------------')
    uncounted = 0

    for step, artist in enumerate(top):
        scrobbles = int(artist.weight)
        if scrobbles < int(top[0].weight) / 1000 or scrobbles <= 2:
            break

        country = brainz_getter(artist.item.get_mbid())
        if not country:
            country = last_summary_getter(artist.item.name)
        if not country:
            country = wikipedia_getter(artist.item.name)

        if country:
            if country in countries.keys():
                countries[country] += scrobbles
            else:
                countries[country] = scrobbles
        else:
            uncounted += 1

        print('#{}\t{}\t{}\t{}'.format(step + 1, artist.item.name, country, scrobbles))

    if len(countries) == 0:
        print('Not enough data at your library, try to set bigger limit or to scrobble more. Sorry :(')
        exit(2)

    if len(top) >= 5:
        dump_data(countries, name, lim, sum(countries.values()), uncounted)
    return countries


if __name__ == '__main__':
    pass

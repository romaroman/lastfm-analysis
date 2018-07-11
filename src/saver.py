import sqlite3
# import pickle

# def dump_data(countries, username, limit, total_scr, uncounted):
#     data = {
#         'countries': countries,
#         'username': username,
#         'limit': limit,
#         'analysis_date': ANALYSIS_DATE,
#         'total_scrobbles': total_scr,
#         'total_countries': len(countries),
#         'uncounted_amount': uncounted,
#         'uncounted_percentage': int(uncounted / len(countries) * 100)
#     }
#     filename = r'dumps/{}_{}_{}.dat'.format(username, limit, str(ANALYSIS_DATE.time())[:8])
#     with open(filename, 'wb+') as file:
#         pickle.dump(data, file)
#         file.close()
#

def sqlite_handler():
    connection = sqlite3.connect('data.db')


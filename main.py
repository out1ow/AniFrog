import json
import sqlite3
import pprint as pp

import requests

from shikimori import Shikimori
from config import *

def console_print():
    connection = sqlite3.connect('anime.db')
    cursor = connection.cursor()

    cursor.execute('select name from plan')
    plan = cursor.fetchall()

    cursor.execute('select max(length(name)) from plan')
    max_pln = cursor.fetchall()[0][0]
    "=================================================================="
    cursor.execute('select name from watching')
    watching = cursor.fetchall()

    cursor.execute('select max(length(name)) from watching')
    max_wat = cursor.fetchall()[0][0]
    "=================================================================="
    cursor.execute('select name from completed')
    completed = cursor.fetchall()

    cursor.execute('select max(length(name)) from completed')
    max_com = cursor.fetchall()[0][0]
    "=================================================================="
    cursor.execute('select name from dropped')
    dropped = cursor.fetchall()

    cursor.execute('select max(length(name)) from dropped')
    max_drp = cursor.fetchall()[0][0]
    "=================================================================="

    print(('\n+' + '-' * (max_pln + 7)) + ('+' + '-' * (max_wat + 7) ) + ('+' + '-' * (max_com + 7)) + ('+' + '-' * (max_drp + 7) + '+'))

    print('|' + ' ' * ((max_pln + 7) // 2 - 6) + 'PLAN TO WATCH' + ' ' * (max_pln - (max_pln + 7) // 2), end='|')
    print(' ' * ((max_wat + 7) // 2 - 4) + 'WATCHING' + ' ' * (max_wat - (max_wat + 7) // 2 + 3), end='|')
    print(' ' * ((max_com + 7) // 2 - 4) + 'COMPLETED' + ' ' * (max_com - (max_com + 7) // 2 + 2), end='|')
    print(' ' * ((max_drp + 7) // 2 - 3) + 'DROPPED' + ' ' * (max_drp - (max_drp + 7) // 2 + 3), end='|')

    rows = max(len(plan), len(watching), len(completed), len(dropped))
    for i in range(0, rows):
        sym = ''
        print(('\n+----+' + '-' * (max_pln + 2)) + ('+----+' + '-' * (max_wat + 2) ) + ('+----+' + '-' * (max_com + 2)) + ('+----+' + '-' * (max_drp + 2) + '+'))

        sep = ' ' if i + 1 < 10 else ''

        try:
            print('|', (i + 1), sep + '|', plan[i][0], end=' ' * (max_pln - len(plan[i][0])) + ' |')
        except Exception:
            sym += '|    |' + ' ' * (max_pln + 2) + '|'
        try:
            print(sym, (i + 1), sep + '|', watching[i][0], end=' ' * (max_wat - len(watching[i][0])) + ' |')
        except Exception:
            sym += '    |' + ' ' * (max_wat + 2) + '|'
        try:
            print(sym, (i + 1), sep + '|', completed[i][0], end=' ' * (max_com - len(completed[i][0])) + ' |')
        except Exception:
            sym += '    |' + ' ' * (max_com + 2) + '|'
        try:
            print(sym, (i + 1), sep + '|', dropped[i][0], end=' ' * (max_drp - len(dropped[i][0])) + ' |')
        except Exception:
            print('    |' + ' ' * (max_drp + 2), end='|')

    print(('\n+----+' + '-' * (max_pln + 2)) + ('+----+' + '-' * (max_wat + 2) ) + ('+----+' + '-' * (max_com + 2)) + ('+----+' + '-' * (max_drp + 2) + '+'))

    connection.close()

#def token_saver(token: dict):
#    with open("token.json", 'w') as f:
#        f.write(json.dump(token))

def main():
    pass
    session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    print(session.get_user_anime())
    print("=-=-=-=-=-=-=-=---=-=========================================================================")
    print(session.get_user_manga())

    #print(requests.get("https://shikimori.one/api/users/waki0_0?is_nickname=1", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}).json())
    # 1501852
if __name__ == '__main__':
    main()
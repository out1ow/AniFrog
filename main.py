import json
import sqlite3
import pprint as pp

from shikimori import Shikimori
from ani_frog import AniFrog
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
    connection.close()

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

def fill_database(session: Shikimori, ani_frog: AniFrog):
    planned = [i["anime"]["russian"] for i in session.get_user_anime("planned")]
    watching = [(i["anime"]["russian"], i["episodes"], i["anime"]["episodes"]) for i in session.get_user_anime("watching")]
    completed = [i["anime"]["russian"] for i in session.get_user_anime("completed")]

    print(f"The data has been added to the \"planned\" table: {ani_frog.add_planned_anime(planned)}")
    print(f"The data has been added to the \"watching\" table: {ani_frog.add_watching_anime(watching)}")
    print(f"The data has been added to the \"completed\" table: {ani_frog.add_completed_anime(completed)}")

def main():
    try:
        with open('token.json') as f:
            token = json.load(f)
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token=token)
    except Exception:
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    frog = AniFrog()

    fill_database(session, frog)

if __name__ == '__main__':
    main()
import json
import sqlite3
import sys
from pprint import pprint

from main_window import *
from shikimori import Shikimori
from db_manager import DatabaseManager
from config import *

# TODO: сделать окно регистрации в приложении

def fill_database(session: Shikimori, db: DatabaseManager):
    planned = [i["anime"]["russian"] for i in session.get_user_anime("planned")]
    watching = [(i["anime"]["russian"], i["episodes"], i["anime"]["episodes"]) for i in
                session.get_user_anime("watching")]
    completed = [i["anime"]["russian"] for i in session.get_user_anime("completed")]

    db.clear()

    print(f"The data has been added to the \"planned\" table: {db.add_planned_anime(planned)}")
    print(f"The data has been added to the \"watching\" table: {db.add_watching_anime(watching)}")
    print(f"The data has been added to the \"completed\" table: {db.add_completed_anime(completed)}")


def main():
    try:
        with open('token.json') as f:
            token = json.load(f)
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token=token)
    except Exception:
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # print(session.post_user_anime("Наруто").json())
    pprint(session.get_anime("Первый шаг"))

    #db = DatabaseManager()
    #db.clear()
    # fill_database(session, db)

    #app = QApplication(sys.argv)
    #ex = MainWindow(session, db)
    #ex.show()
    #sys.exit(app.exec())


if __name__ == '__main__':
    main()

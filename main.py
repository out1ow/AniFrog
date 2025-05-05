import json
import sys

from main_window import *
from shikimori import Shikimori
from db_manager import DatabaseManager
from config import *

# TODO: сделать окно регистрации в приложении




def main():
    db = DatabaseManager()

    app = QApplication(sys.argv)

    try:
        with open('token.json') as f:
            token = json.load(f)
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, token=token)
        ex = MainWindow(session, db)
        ex.show()
    except Exception:
        db.clear()
        session = Shikimori("AniFrog", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        ex = MainWindow(session, db)
        ex.show()
        ex.registration()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

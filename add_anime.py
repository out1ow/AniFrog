from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow
from pprint import pprint

from db_manager import DatabaseManager
from shikimori import Shikimori


class AddAnime(QWidget):
    def __init__(self, main_win: QMainWindow, session: Shikimori, db: DatabaseManager, tab: int):
        super().__init__()

        self.main_win = main_win
        self.session = session
        self.db = db
        self.tab = tab

        uic.loadUi("src/ui/add_anime.ui", self)
        QApplication.setStyle("Windows")
        self.setWindowTitle("Add Anime")
        self.setFixedWidth(400)
        self.setFixedHeight(300)


        self.find_button.clicked.connect(self.find)
        self.add_button.clicked.connect(self.add_anime)

    def find(self):
        self.preview.clear()
        name = self.name_enter.text()
        data = self.session.get_anime(name, 20)
        for i in  data:
            self.preview.addItem(i["russian"])

    def add_anime(self):
        anime = self.preview.currentItem()
        if anime is not None:
            if self.tab == 0:
                self.db.add_planned_anime([anime.text()])
            elif self.tab == 1:
                self.db.add_watching_anime([(anime.text(), 0, self.session.get_anime_id(anime.text())['episodes'])])
            elif self.tab == 2:
                self.db.add_completed_anime([anime.text()])
            self.main_win.initUI()
            self.close()
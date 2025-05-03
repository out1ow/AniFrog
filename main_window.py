import os
import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from db_manager import DatabaseManager
from shikimori import Shikimori


class MainWindow(QMainWindow):
    def __init__(self, session: Shikimori):
        super().__init__()

        self.session = session

        uic.loadUi("main_form.ui", self)

        QApplication.setStyle("Windows")
        self.setWindowTitle("AniFrog")
        self.setFixedWidth(500)
        self.setFixedHeight(520)

        self.db = DatabaseManager()

        self.plan_table.itemSelectionChanged.connect(self.on_plan_selection)
        self.watch_table.itemSelectionChanged.connect(self.on_watch_selection)
        self.comp_table.itemSelectionChanged.connect(self.on_comp_selection)

        self.initUI()

    def initUI(self):
        data = self.db.get_planned_anime()
        self.plan_table.setColumnCount(1)
        self.plan_table.setRowCount(len(data))
        self.plan_table.setHorizontalHeaderLabels([''])
        self.plan_table.horizontalHeader().setDefaultSectionSize(150)
        for i, name in enumerate(data):
            cell = QTableWidgetItem(name)
            self.plan_table.setItem(i, 0, cell)

        data = self.db.get_watching_anime()
        self.watch_table.setColumnCount(1)
        self.watch_table.setRowCount(len(data))
        self.watch_table.setHorizontalHeaderLabels([''])
        self.watch_table.horizontalHeader().setDefaultSectionSize(150)
        for i, name in enumerate(data):
            cell = QTableWidgetItem(name)
            self.watch_table.setItem(i, 0, cell)

        data = self.db.get_completed_anime()
        self.comp_table.setColumnCount(1)
        self.comp_table.setRowCount(len(data))
        self.comp_table.setHorizontalHeaderLabels([''])
        self.comp_table.horizontalHeader().setDefaultSectionSize(150)
        for i, name in enumerate(data):
            cell = QTableWidgetItem(name)
            self.comp_table.setItem(i, 0, cell)

    def on_plan_selection(self):
        item = self.plan_table.selectedItems()[-1].text()
        data = self.session.get_anime(item)

        link = "<a href=\"https://shikimori.one" + data['url'] + "\">" + item + "</a>"
        self.plan_name.setText(link)

        self.plan_info.setText(data['description_html'])

    def on_watch_selection(self):
        item = self.watch_table.selectedItems()[-1].text()
        data = self.session.get_anime(item)

        link = "<a href=\"https://shikimori.one" + data['url'] + "\">" + item + "</a>"
        self.watch_name.setText(link)

        self.watch_info.setText(data['description_html'])

    def on_comp_selection(self):
        item = self.comp_table.selectedItems()[-1].text()
        data = self.session.get_anime(item)

        link = "<a href=\"https://shikimori.one" + data['url'] + "\">" + item + "</a>"
        self.comp_name.setText(link)

        # info = f"""
        #     Тип: {data[0]['kind']}
        #     Эпизоды: {data[0]['episodes']}
        #     Статус:  {data[0]['status']}
        #     Дата выхода: {data[0]['aired_on']}
        #     Рейтинг: {data[0]['score']}"""

        self.comp_info.setText(data['description_html'])

        # try:
        #     os.remove("src/previews/*")
        # except Exception:
        #     pass
        # img = self.session.get_anime_preview(item)
        # print(img)
        # pix = QPixmap(img)
        # print(pix)
        # self.comp_picture.setPixmap(pix)



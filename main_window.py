from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

from add_anime import AddAnime
from db_manager import DatabaseManager
from registration import Registation
from shikimori import Shikimori


class MainWindow(QMainWindow):
    def __init__(self, session: Shikimori, db: DatabaseManager):
        super().__init__()

        self.session = session
        self.db = db

        uic.loadUi("src/ui/main_form.ui", self)

        QApplication.setStyle("Windows")
        self.setWindowTitle("AniFrog")
        self.setFixedWidth(500)
        self.setFixedHeight(520)

        self.plan_table.itemSelectionChanged.connect(self.on_plan_selection)
        self.watch_table.itemSelectionChanged.connect(self.on_watch_selection)
        self.comp_table.itemSelectionChanged.connect(self.on_comp_selection)

    #======================================================================

        # self.plan_add_button.clicked.connect(self.plan_add)
        # self.plan_delete_button.clicked.connect(self.plan_delete)
        #
        # self.watch_add_button.clicked.connect(self.watch_add)
        # self.watch_edit_button.clicked.connect(self.watch_edit)
        # self.watch_delete_button.clicked.connect(self.watch_delete)
        #
        # self.comp_add_button.clicked.connect(self.comp_add)
        # self.comp_delete_button.clicked.connect(self.comp_delete)

        # TODO: реализовать кнопку настроек (принудительное обновление, выход из аккаунта)

    #======================================================================

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
        self.watch_table.setColumnCount(2)
        self.watch_table.setRowCount(len(data))
        self.watch_table.setHorizontalHeaderLabels(['', ''])
        # self.watch_table.horizontalHeader().setDefaultSectionSize(150)
        for i, j in enumerate(data):
            name, completed_episodes, episodes = j
            cell = QTableWidgetItem(name)
            self.watch_table.setItem(i, 0, cell)
            cell = QTableWidgetItem(f"{completed_episodes}/{episodes}")
            self.watch_table.setItem(i, 1, cell)

        data = self.db.get_completed_anime()
        self.comp_table.setColumnCount(1)
        self.comp_table.setRowCount(len(data))
        self.comp_table.setHorizontalHeaderLabels([''])
        self.comp_table.horizontalHeader().setDefaultSectionSize(150)
        for i, name in enumerate(data):
            cell = QTableWidgetItem(name)
            self.comp_table.setItem(i, 0, cell)

    def registration(self):
        self.exe = Registation(self, self.session)
        self.exe.exec()

    def fill_database(self):
        planned = [i["anime"]["russian"] for i in self.session.get_user_anime("planned")]
        watching = [(i["anime"]["russian"], i["episodes"], i["anime"]["episodes"]) for i in
                    self.session.get_user_anime("watching")]
        completed = [i["anime"]["russian"] for i in self.session.get_user_anime("completed")]

        self.db.clear()

        return all((self.db.add_planned_anime(planned), self.db.add_watching_anime(watching),
                   self.db.add_completed_anime(completed)))
    #======================================================================

    def on_plan_selection(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        item = self.plan_table.selectedItems()[-1].text()
        data = self.session.get_anime_id(item)

        link = "<a href=\"https://shikimori.one" + data['url'] + "\" style=\"color:#6666ff ;\"> <b>" + item + "</ b></a>"
        self.plan_name.setText(link)

        self.plan_info.setText(data['description_html'])
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def on_watch_selection(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        item = self.watch_table.selectedItems()[-1]
        if item.column() == 0:
            data = self.session.get_anime_id(item.text())

            link = "<a href=\"https://shikimori.one" + data['url'] + "\" style=\"color:#6666ff ;\"> <b>" + item.text() + "</ b></a>"
            self.watch_name.setText(link)

            self.watch_info.setText(data['description_html'])
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def on_comp_selection(self):
        self.setCursor(QCursor(Qt.CursorShape.WaitCursor))
        item = self.comp_table.selectedItems()[-1].text()
        data = self.session.get_anime_id(item)

        link = "<a href=\"https://shikimori.one" + data['url'] + "\" style=\"color:#6666ff ;\"> <b>" + item + "</ b></a>"
        self.comp_name.setText(link)

        # info = f"""
        #     Тип: {data[0]['kind']}
        #     Эпизоды: {data[0]['episodes']}
        #     Статус:  {data[0]['status']}
        #     Дата выхода: {data[0]['aired_on']}
        #     Рейтинг: {data[0]['score']}"""

        self.comp_info.setText(data['description_html'])
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        # try:
        #     os.remove("src/previews/*")
        # except Exception:
        #     pass
        # img = self.session.get_anime_preview(item)
        # print(img)
        # pix = QPixmap(img)
        # print(pix)
        # self.comp_picture.setPixmap(pix)

    #======================================================================
    # TODO: реализовать удаление и редактирование тайтлов

    # def plan_add(self):
    #     self.exe = AddAnime(self, self.session, self.db, 0)
    #     self.exe.show()
    #
    #
    # def plan_delete(self):
    #     print("plan_delete")
    #
    # #======================================================================
    #
    # def watch_add(self):
    #     self.exe = AddAnime(self, self.session, self.db, 1)
    #     self.exe.show()
    #
    # def watch_delete(self):
    #     print("watch_delete")
    #
    # def watch_edit(self):
    #     print("watch_edit")
    #
    # #======================================================================
    #
    # def comp_add(self):
    #     self.exe = AddAnime(self, self.session, self.db, 2)
    #     self.exe.show()
    #
    # def comp_delete(self):
    #     print("comp_delete")
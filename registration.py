from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QApplication, QMainWindow

from db_manager import DatabaseManager
from shikimori import Shikimori


class Registation(QDialog):
    def __init__(self, main_win: QMainWindow, session: Shikimori):
        super().__init__()

        self.main_win = main_win
        self.session = session

        uic.loadUi("src/ui/registration.ui", self)

        QApplication.setStyle("Registation")
        self.setWindowTitle("AniFrog")
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.label.setText(f'Войдите в свой аккаунт Shilimori по ссылке: '
                           f'<a href="{self.session.get_auth_url()}" style="color:#6666ff ;"> <b> -ССЫЛКА- </ b> </a>'
                           f'После чего введите код авторизации ↓ниже↓')

        self.buttonBox.accepted.connect(self.btn_clicked)

    def btn_clicked(self):
        token = self.lineEdit.text()
        if token != '':
            self.session.authorize(token)
            self.main_win.fill_database()
            self.main_win.initUI()
            self.accept()
        self.close()
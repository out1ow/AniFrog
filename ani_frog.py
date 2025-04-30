import sqlite3
import os

class AniFrog:
    _DB_FILE = "ani_frog.db"

    def __init__(self):
        try:
            if not os.path.exists(self._DB_FILE):
                self.connection = sqlite3.connect(self._DB_FILE)
                self.cursor = self.connection.cursor()
                self.cursor.execute("""
                    CREATE TABLE planned (
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name STRING UNIQUE NOT NULL);
                    """)
                self.cursor.execute("""
                    CREATE TABLE watching (
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name STRING UNIQUE NOT NULL,
                        completed_episodes INTEGER NOT NULL,
                        episodes INTEGER);
                    """)
                self.cursor.execute("""
                    CREATE TABLE completed (
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                        name STRING UNIQUE NOT NULL);
                    """)
                self.connection.commit()
            else:
                self.connection = sqlite3.connect(self._DB_FILE)
                self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error when creating table: {e}")


    def __del__(self):
        self.connection.close()

    def get_planned_anime(self) -> list:
        try:
            self.cursor.execute("SELECT name from planned")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return []

    def get_watching_anime(self) -> list:
        try:
            self.cursor.execute("SELECT name from watching")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return []

    def get_completed_anime(self) -> list:
        try:
            self.cursor.execute("SELECT name from completed")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return []
#========================================================================
    def add_planned_anime(self, anime: list) -> bool:
        """anime = [name1, name2.....]"""
        try:
            self.cursor.executemany("INSERT OR IGNORE INTO planned (name) VALUES(?)", [(name,) for name in anime])
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return False

    def add_watching_anime(self, anime: list):
        """anime = [(name, completed_episodes, episodes), (...),....]"""
        try:
            self.cursor.executemany("INSERT OR IGNORE INTO watching (name, completed_episodes, episodes) VALUES(?, ?, ?)", anime)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return False

    def add_completed_anime(self, anime: list):
        """anime = [name1, name2.....]"""
        try:
            self.cursor.executemany("INSERT OR IGNORE INTO completed (name) VALUES(?)", [(name,) for name in anime])
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error when adding data: {e}")
            return False
import sqlite3
import datetime
import sys

class NotInDatabaseException(Exception):
    pass

class DifferentPasswordException(Exception):
    pass

class Database:
    __REPO = "database/users.db"
    def __init__(self, repo=None):
        if repo is not None:
            self.conn = sqlite3.connect(repo, check_same_thread=False)
        else:
            self.conn = sqlite3.connect(self.__REPO, check_same_thread=False)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Clients (
        Email VARCHAR PRIMARY KEY,
        Password VARCHAR NOT NULL,
        Nickname VARCHAR NOT NULL
        );""")
        self.conn.commit()

    def show_table(self):
        self.cur.execute("""SELECT * FROM Clients""")
        data = self.cur.fetchall()
        self.conn.commit()
        return data

    def get_data(self, email):
        self.cur.execute("""SELECT * FROM Clients WHERE Email = ?""", (email,))
        data = self.cur.fetchall()
        self.conn.commit()
        return data

    def get_nickname(self, email):
        self.cur.execute("""SELECT Nickname FROM Clients WHERE Email = ?""", (email,))
        data = self.cur.fetchall()
        self.conn.commit()
        return data

    # data ==> email + password + nickname
    def insert_data(self, data):
        email, password, nickname = data
        try:
            self.cur.execute("""INSERT INTO Clients VALUES (?, ?, ?)""", (email, password, nickname))
            print(f"Successfully created user: {email}, nickname {nickname}.")
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Cannot insert {email} twice.")
        except sqlite3.OperationalError:
            print(f"Corruption occured, try wait for some time.")


    # data ==> email + password
    def delete_data(self, data):
        email, _, = data
        try:
            self.search_and_check_password(data)
        except NotInDatabaseException:
            print(f"{email} not found.")
        except DifferentPasswordException:
            print(f"Incorrect password. Access denied.")
        else:
            self.cur.execute("""DELETE FROM Clients WHERE Email = ?""", (email,))
            self.conn.commit()
            print(f"Deleted user {email}")


    # data ==> email + password + nickname
    def update_data(self, data):
        email, password, nickname = data
        self.cur.execute("""UPDATE Clients SET Password = ? WHERE Email = ?""", (password, email))
        self.cur.execute("""UPDATE Clients SET Nickname = ? WHERE Email = ?""", (nickname, email))
        self.conn.commit()

    def drop_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS Client""")
        self.conn.commit()

    # data ==> email + password
    def search_and_check_password(self, data):
        email, password = data
        query = self.get_data(email)
        if len(query) == 0:
            raise NotInDatabaseException
        _, org_pass, _ = query[0]
        if password != org_pass:
            raise DifferentPasswordException


if __name__ == '__main__':
    with Database() as db:
        db.create_table()
        db.insert_data(('asd@gmail.com','qwerty', 'tom'))
        db.insert_data(('qwe@gmail.com','asdfgh', 'jerry'))
        for row in db.show_table():
            print(row)
        db.update_data(('asd@gmail.com','qwerty2', 'Jerry'))
        for row in db.show_table():
            print(row)
        db.delete_data(('asd@gmail.com','querty2'))
        for row in db.show_table():
            print(row)
        db.delete_data(('asd@gmail.com','qwerty2'))
        for row in db.show_table():
            print(row)
        db.drop_table()

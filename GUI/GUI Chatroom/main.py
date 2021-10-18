import sqlite3
import datetime
import sys
import socket
import threading
from utils import welcome, display
from sql_data import Database
from queue import Queue


def main():
    with Database() as db:
        db.create_table()
        display(first=True)
        while True:
            welcome(db)

        # db.drop_table()

if __name__ == '__main__':
    main()
    # jobs = Queue(maxsize=8)
    # if not jobs.full():
    #     thread = threading.Thread(name=main)
    #     jobs.append(thread)
    # else:
    #     print("Too many visitors, wait for vacancies.")

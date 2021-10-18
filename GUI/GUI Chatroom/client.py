import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from utils import Client

def main():
    HOST = '127.0.0.1'
    PORT = 9090

    client = Client(HOST, PORT)

if __name__ == '__main__':
    main()

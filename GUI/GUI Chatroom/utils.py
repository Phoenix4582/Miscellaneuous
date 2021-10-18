import getpass
import sys
from sql_data import Database, NotInDatabaseException, DifferentPasswordException

import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

class DifferentPassException(Exception):
    def __init__(self, message="Passwords must be the same. Try again!"):
        super(DifferentPassException, self).__init__(message)
        self.message = message

class RangeException(Exception):
    def __init__(self, message="Invalid input. Try again!"):
        super(RangeException, self).__init__(message)
        self.message = message

def input_interface(new_user=False):
    email = input("Input your email address:")
    password = getpass.getpass(prompt="Input your password:")
    if new_user == True:
        re_password = getpass.getpass("Confirm your password:")
        if password != re_password:
            raise DifferentPassException()
        nickname = input("Input your nickname:")
        return email, password, nickname

    return email, password

def handle_new_user(database):
    try:
        email, password, nickname = input_interface(new_user=True)
    except DifferentPassException as dpe:
        print(dpe.message)
    else:
        database.insert_data((email, password, nickname))
    display()

def login_user(database, host='127.0.0.1', port=9090):
    email, password = input_interface()
    try:
        database.search_and_check_password((email, password))
    except NotInDatabaseException:
        print(f"{email} not found.")
    except DifferentPasswordException:
        print(f"Incorrect password. Access denied.")
    else:
        print(f"Login as {email}.")
        n_name = list((database.get_nickname(email)[0]))[0]
        print(f"Nickname: {n_name}")
        client = Client(host, port, n_name)
    display()

def delete_user(database):
    email, password = input_interface()
    database.delete_data((email, password))
    display()

def update_user(database):
    email, password = input_interface()
    try:
        database.search_and_check_password((email, password))
    except NotInDatabaseException:
        print(f"{email} not found.")
    except DifferentPasswordException:
        print(f"Incorrect password. Access denied.")
    else:
        new_password = getpass.getpass(prompt="Input your new password:")
        new_nickname = input("Input your new nickname:")
        database.update_data((email, new_password, new_nickname))

def quit(*args):
    print("Thank you for your usage!")
    sys.exit(1)

def display(first=False):
    if first == True:
        print("Welcome to the Prototype GUI ChatRoom!")
    else:
        print("Anything Else?")
    print("Usage:")
    print("--1.New User")
    print("--2.Login")
    print("--3.Update User")
    print("--4.Delete User")
    print("--5.Exit")

COMMAND_LIBRARY = {"1": handle_new_user, "2": login_user, "3": update_user, "4":delete_user, "5": quit}

def welcome(database):
    try:
        index = input("Select your service (input with corresponding number):")
        if index not in ["1", "2", "3", "4", "5"]:
            raise RangeException
    except RangeException as re:
        print(re.message)
    else:
        command = COMMAND_LIBRARY[index]
        command(database)
        for row in database.show_table():
            print(row)

class Client:
    def __init__(self, host, port, nickname):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = nickname

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_btn = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_btn.config(font=("Arial", 12))
        self.send_btn.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except Exception:
                print("ERROR")
                self.sock.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

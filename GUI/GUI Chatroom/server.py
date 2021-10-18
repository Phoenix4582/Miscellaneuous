import socket
import threading

def broadcast(message, clients):
    for client in clients:
        client.send(message)

def receive(server, nicknames, clients):
    while True:
        cli, address = server.accept()
        print(f"Connected with {str(address)}.")

        cli.send("NICK".encode('utf-8'))
        nickname = cli.recv(1024)

        nicknames.append(nickname)
        clients.append(cli)

        print(f"Nickname of the client name is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'), clients)
        cli.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(cli,clients,nicknames,))
        thread.start()


def handle(cli, clients, nicknames):
    while True:
        try:
            message = cli.recv(1024)
            print(f"{nicknames[clients.index(cli)]} says {message}")
            broadcast(message, clients)
        except Exception:
            index = clients.index(cli)
            clients.remove(cli)
            cli.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def start_server():
    HOST = '127.0.0.1'
    PORT = 9090

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen()

    clients = []
    nicknames = []

    print("Server running......")
    receive(server, nicknames, clients)


if __name__ == '__main__':
    start_server()

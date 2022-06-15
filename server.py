import socket
import colorama
import threading


class Server:
    def __init__(self, server_name, server_ip, server_port, encoding):
        self.server_name = server_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.encoding = encoding
        self.connections_list = []
        self.clients_list = []

    def send_message_to_all_clients(self, message):
        message = bytes(message, self.encoding)
        for connection in self.connections_list:
            connection.send(message)

    def handle_client(self, connection, client_ip, client_port):
        self.connections_list.append(connection)
        username = connection.recv(1024).decode()
        self.clients_list.append((username, client_ip, client_port))
        self.send_message_to_all_clients(f'{username} ({client_ip}, {client_port}) HAS JOINED THE CHAT.')
        print(f'{colorama.Fore.LIGHTBLUE_EX}[LOG]\t({client_ip}, {client_port}) CONNECTED AS {username}.')
        connected = True
        while connected:
            chat = connection.recv(1024).decode(self.encoding)
            if chat == f'{username} >> &exit':
                connection.send(bytes('&exit', self.encoding))
                connected = False
                connection.close()
                self.clients_list.remove((username, client_ip, client_port))
                self.connections_list.remove(connection)
                print(f'{colorama.Fore.LIGHTBLUE_EX}[LOG]\t{username} DISCONNECTED.')
                self.send_message_to_all_clients(f'{username} HAS LEFT THE CHAT.')
                print(f'{colorama.Fore.BLUE}[LOG]\tACTIVE CLIENTS: {self.clients_list}')
            else:
                self.send_message_to_all_clients(chat)

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        print(f'{colorama.Fore.BLUE}[LOG]\tSERVER {self.server_name} STARTED IN ({self.server_ip}, {self.server_port})')
        server.listen()
        print(f'{colorama.Fore.BLUE}[LOG]\tWAITING FOR CONNECTIONS....')
        connected = True
        while connected:
            connection, (client_ip, client_port) = server.accept()
            thread = threading.Thread(target=self.handle_client, args=[connection, client_ip, client_port])
            thread.start()


if __name__ == '__main__':
    SERVER_NAME = 'B'
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 2409
    ENCODING = 'utf-8'
    s = Server(SERVER_NAME, SERVER_IP, SERVER_PORT, ENCODING)
    s.run_server()

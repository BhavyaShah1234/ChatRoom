import socket
import colorama
import threading


class Client:
    def __init__(self, server_ip, server_port, encoding):
        self.server_ip = server_ip
        self.server_port = server_port
        self.encoding = encoding
        self.username = input(f'{colorama.Fore.YELLOW}[INPUT]\tENTER USERNAME: ')

    def receive_messages(self, client):
        chat = client.recv(1024).decode(self.encoding)
        if chat:
            print(f'{colorama.Fore.LIGHTGREEN_EX}[CHAT]\t{chat}')
        else:
            print(f'{colorama.Fore.YELLOW}[LOG]\tCLIENT DISCONNECTED.')

    def send_chat(self, client):
        chat = input('')
        message = bytes(f'{self.username} >> {chat}', self.encoding)
        client.send(message)

    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))
        print(f'{colorama.Fore.YELLOW}[LOG]\tCLIENT STARTED.')
        print(f'{colorama.Fore.YELLOW}[LOG]\tCONNECTED TO ({self.server_ip}, {self.server_port}).')
        print(f'{colorama.Fore.YELLOW}[LOG]\tTO EXIT THE SERVER ENTER "&exit"')
        client.send(bytes(self.username, self.encoding))
        running = True
        while running:
            message_receiving_thread = threading.Thread(target=self.receive_messages, args=[client])
            message_receiving_thread.start()
            chat_sending_thread = threading.Thread(target=self.send_chat, args=[client])
            chat_sending_thread.start()


if __name__ == '__main__':
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 2409
    ENCODING = 'utf-8'
    c = Client(SERVER_IP, SERVER_PORT, ENCODING)
    c.run_client()

import socket
import json
from multiprocessing.pool import ThreadPool
import http_server_db_handler


class TCPServer:

    def __init__(self):
        self.server_ip = '0.0.0.0'
        self.port = 8080
        self.thread_num = 5
        self.pool = ThreadPool(self.thread_num)
        self.client_handler = TCPClientHandler()

    def server_forever(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.port))
        server.listen(5)
        while True:
            client_socket, client_address = server.accept()
            print client_address
            # self.client_handler.handle_client(client_socket)
            self.pool.apply_async(self.client_handler.handle_client, (client_socket,))


class TCPClientHandler:

    def __init__(self):
        self.db_query_handler = http_server_db_handler.HttpServerDBHandler()
        self.end_message = "END_OF_MESSAGE&#"

    def handle_client(self, client_socket):
        # TODO: Change most of this. Only basic functionality exists.
        request = client_socket.recv(2048)
        request_json = json.loads(request)
        command_id = int(request_json['commandID'])
        param = request_json['param']
        paragraphs_records = self.db_query_handler.paragraph_by_url_query(param)
        paragraph_list = []
        for paragraph_record in paragraphs_records:
            paragraph_list.append(paragraph_record.get('paragraph'))
        response = json.dumps(paragraph_list)
        client_socket.send(response)
        client_socket.send(self.end_message)
        client_socket.close()


a = TCPServer()
a.server_forever()

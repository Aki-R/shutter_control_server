import socket   # モジュールのインポート
import queue
import json


listenSocket = socket.socket()  # socketを作成

with open('config.json', 'r') as file:
    data = json.load(file)
    port = data['socket_port']


def init():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(ip)

    listenSocket.bind((ip, port))   # ソケットを特定のIPアドレスとポートに紐付け
    listenSocket.listen(5)  # 接続の待受を開始
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1)


def main(q):
    init()
    while True:
        try:
            listenSocket.settimeout(10)
            print("accepting.....")
            conn, addr = listenSocket.accept()  # 接続を受信
            command = q.get(timeout=1)
            print(f'Socket:{command}')
            print(addr, "connected")    # 接続した相手のipアドレスを表示

            if len(command) > 0:
                conn.sendall(command.encode())
            conn.close()    # 接続を切断

        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    queq = queue.Queue()
    main(queq)

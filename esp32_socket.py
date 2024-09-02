import socket   # モジュールのインポート
import queue
import json
import time


listenSocket = socket.socket()  # socketを作成

with open('config.json', 'r') as file:
    data = json.load(file)
    port = data['socket_port']
    ip = data['host']


def init():
    listenSocket.bind((ip, port))   # ソケットを特定のIPアドレスとポートに紐付け
    listenSocket.listen(5)  # 接続の待受を開始
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1)


def main(q, ipadr):
    init()
    while True:
        try:
            listenSocket.settimeout(60)
            print("accepting.....")
            conn, addr = listenSocket.accept()  # 接続を受信
            ipadr.put(addr)
            print(addr, "connected")
            try:
                command = q.get(timeout=300)
                # Clear Queue
                while not q.empty():
                    q.get()
                print(f'Socket:{command}')
                if len(command) > 0:
                    conn.sendall(command.encode())
            except Exception as e:
                print(f'Error:{e}')
            conn.close()    # 接続を切断
            print("connection closed")
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(1)
        except KeyboardInterrupt:
            conn.close()
            listenSocket.close()


if __name__ == '__main__':
    queq = queue.Queue()
    ip = queue.Queue()
    main(queq, ip)

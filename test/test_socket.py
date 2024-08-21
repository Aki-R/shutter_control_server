import socket
import json

# サーバーの設定
with open('test_config.json', 'r') as file:
    data = json.load(file)
    HOST = data['host']     # サーバーのホスト
    PORT = data['port']     # サーバーのポート番号

# ソケットを作成してサーバーに接続
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        print(f"Received from server: {data.decode()}")

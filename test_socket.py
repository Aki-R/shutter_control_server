import socket

# サーバーの設定
HOST = '192.168.11.18'  # サーバーのホスト
PORT = 8000        # サーバーのポート番号

# ソケットを作成してサーバーに接続
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
        print(f"Received from server: {data.decode()}")

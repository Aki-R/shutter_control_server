#!/bin/bash

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 作業ディレクトリに移動する
cd "$SCRIPT_DIR"

# 仮想環境のディレクトリ名
VENV_DIR="venv"

# Pythonスクリプトのファイル名
SCRIPT_NAME="shutter_control_server.py"

# 仮想環境をアクティベートする
source "$VENV_DIR/bin/activate"

# 必要なパッケージをインストールする（requirements.txtがあれば）
if [ -f "requirements.txt" ]; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Pythonスクリプトを実行する
echo "Running Python script..."
python3 "$SCRIPT_NAME"

# 仮想環境をデアクティベートする
deactivate

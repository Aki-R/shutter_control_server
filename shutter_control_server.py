from flask import Flask, render_template, request, redirect, url_for, session
import threading
import queue
import esp32_socket
import json


q = queue.LifoQueue()
ipadr = queue.Queue(maxsize=1)
ipadr_str = "No IP"

app = Flask(__name__)

with open('config.json', 'r') as file:
    data = json.load(file)
    app.secret_key = data['secret_key']
    password = data['password']
    port = data['port']
    host = data['host']


@app.route('/')
def index():
    global ipadr_str
    if 'login' in session:
        if session['login'] is True:
            if not ipadr.empty():
                ipadr_str = str(ipadr.get())
            return render_template('top.html', ip_str=ipadr_str)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_password = request.form['password']

        if input_password == password:
            session['login'] = True

            return redirect(url_for('index'))
        else:
            return 'Invalid username/password'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('index'))


@app.route('/Up')
def get_forward():
    if session['login'] is True:
        print('Server:Up')
        q.put('Up\n')
    return redirect(url_for('index'))


@app.route('/Stop')
def get_stop():
    if session['login'] is True:
        print('Server:Stop')
        q.put('Stop\n')
    return redirect(url_for('index'))


@app.route('/Down')
def get_back():
    if session['login'] is True:
        print('Server:Down')
        q.put('Down\n')
    return redirect(url_for('index'))


@app.route('/Light')
def get_light():
    if session['login'] is True:
        print('Server:Light')
        q.put('Light\n')
    return redirect(url_for('index'))


def server_run():
    control_server = threading.Thread(target=esp32_socket.main, args=(q,ipadr,))
    control_server.start()
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == '__main__':
    server_run()

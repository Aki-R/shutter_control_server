from flask import Flask, render_template, request, redirect, url_for, session
import threading
import queue
import esp32_socket

q = queue.Queue()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ダミーのpassword
password = 'password'

@app.route('/')
def index():
    if session['login'] is True:
        return render_template('top.html')
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
        q.put('Up')
    return redirect(url_for('index'))


@app.route('/Stop')
def get_stop():
    if session['login'] is True:
        print('Server:Stop')
        q.put('Stop')
    return redirect(url_for('index'))


@app.route('/Down')
def get_back():
    if session['login'] is True:
        print('Server:Down')
        q.put('Down')
    return redirect(url_for('index'))


def server_run():
    control_server = threading.Thread(target=esp32_socket.main, args=(q,))
    control_server.start()
    app.run(port=8000, debug=True, use_reloader=False)


if __name__ == '__main__':
    server_run()

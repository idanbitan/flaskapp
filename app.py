from flask.app import Flask
from threading import Thread
import os

app1 = Flask('app1')

@app1.route('/')
def foo():
    return '1'

def start_app1():
    print("starting app1")
    app1.run(port=8081)

app2 = Flask('app2')

@app2.route('/')
def bar():
    return '2'

def start_app2():
    print("starting app2")
    app2.run(port=8082, debug=True)

if __name__ == '__main__':
    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    Thread(target=start_app1).start()
    start_app2()
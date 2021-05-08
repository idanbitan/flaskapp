from threading import Thread
from platforms import start_platforms_app
from apps import start_apps_app

if __name__ == '__main__':
    Thread(target=start_platforms_app).start()
    start_apps_app()
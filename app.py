import threading
from time import sleep
from flask import Flask, render_template

from config import CHECK_QUEUE_TIME, narou_request_queue, LOGGER, hameln_request_queue
from src.controller import Hameln, Narou, Download
from src.service.HamelnService import HamelnService
from src.service.NarouService import NarouService

app = Flask(__name__)
app.register_blueprint(Narou.app)
app.register_blueprint(Hameln.app)
app.register_blueprint(Download.app)
logger = LOGGER


@app.route('/')
def home():
    return render_template('index.html')


def narou_executor():
    service = NarouService()
    try:
        while True:
            while narou_request_queue.qsize() > 0:
                novels = narou_request_queue.get()
                logger.debug(f'[narou] get novels')
                service.take_novels(novels)
                logger.debug(f'[narou] completed.')
            sleep(CHECK_QUEUE_TIME)
    except Exception as e:
        logger.warning('narou exec', e)


def hameln_executor():
    service = HamelnService()
    try:
        while True:
            while hameln_request_queue.qsize() > 0:
                start, end = hameln_request_queue.get()
                print(start, end)

                logger.debug(f'[hameln] get novels')
                service.take_novels(start, end)
                logger.debug('[hameln] completed.')
            sleep(CHECK_QUEUE_TIME)
    except Exception as e:
        logger.warning('hameln exec', e)


if __name__ == '__main__':
    try:
        app_thread = threading.Thread(target=app.run)
        narou_executor_thread = threading.Thread(target=narou_executor)
        hameln_executor_thread = threading.Thread(target=hameln_executor)

        app_thread.setDaemon(True)
        narou_executor_thread.setDaemon(True)
        hameln_executor_thread.setDaemon(True)

        app_thread.start()
        narou_executor_thread.start()
        hameln_executor_thread.start()

        while app_thread.is_alive() and narou_executor_thread.is_alive() and hameln_executor_thread.is_alive():
            print(app_thread.is_alive(), narou_executor_thread.is_alive(), hameln_executor_thread.is_alive())
            sleep(60 * 60)
            pass

    except KeyboardInterrupt:
        print("Ctr-C")



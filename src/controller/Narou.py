import threading

from flask import Blueprint, render_template, request

from config import narou_request_queue, LOGGER
from src.Model.NarouParameters import Order, Category, Genre, NovelType
from src.lib.NarouParser import parse_to_RequestAttribute
from src.service.NarouService import NarouAPIService

app = Blueprint('naoru', __name__, url_prefix='/narou')
logger = LOGGER
service = NarouAPIService()


@app.route('/')
def home():
    return render_template('narou/home.html',
                           Order=Order,
                           Category=Category,
                           Genre=Genre,
                           NovelType=NovelType
                           )


@app.route('/take_novel_from_api', methods=['POST'])
def take_novel_list():
    try:
        request_attribute = parse_to_RequestAttribute(request.form)

        def task(request_attribute):
            logger.debug(f'{request_attribute}')
            novels = service.take_novel_information_from_api(request_attribute)
            narou_request_queue.put(novels)

        thread = threading.Thread(target=task, args=(request_attribute,))
        thread.setDaemon(True)
        thread.start()
        return '''
        Accepted.
        <br><a href="/">home</a>
        '''
    except Exception as e:
        return f'''
        {e}
        request failed.
        <br><a href="/">home</a>
        '''

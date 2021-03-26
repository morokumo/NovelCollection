from flask import Blueprint, render_template, request, make_response

from config import LOGGER, hameln_request_queue
from src.Model.Parameters import GlobalSiteGenre
from src.service.Repository import Repository
from src.lib.String import make_text_from_novels

app = Blueprint('hameln', __name__, url_prefix='/hameln')
logger = LOGGER


@app.route('/')
def home():
    return render_template('hameln/home.html')


@app.route('/request', methods=['POST'])
def take_novel_list():
    try:
        start, end = request.form['start'], request.form['end']
        hameln_request_queue.put((int(start), int(end)))
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

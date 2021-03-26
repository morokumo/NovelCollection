import os
from datetime import timezone, timedelta
from logging import Logger, INFO, DEBUG, StreamHandler, Formatter
from queue import Queue

# log settings
LOGGER = Logger(__name__)
handler = StreamHandler()
# formatter = Formatter('[debug] %{message}s')

handler.setLevel(DEBUG)
LOGGER.setLevel(DEBUG)

LOGGER.addHandler(handler)
LOGGER.propagate = False

# const parameters
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                  'Version/14.0.2 Safari/605.1.15 ',
}
ACCESS_DELAY = 3  # seconds
CHECK_QUEUE_TIME = 30  # seconds

DATABASE_NAME = 'debug'

NAROU_URL = 'https://ncode.syosetu.com'
HAMELN_URL = 'https://syosetu.org/'
KAKUYOMU = ''

TIMEZONE = timezone(timedelta(hours=+9), 'JST')

# dir settings
ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(ROOT, 'databases')

# global variable
narou_request_queue = Queue()
hameln_request_queue = Queue()


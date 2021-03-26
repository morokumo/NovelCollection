from time import sleep

import requests
from urllib.robotparser import RobotFileParser

from config import ACCESS_DELAY, LOGGER, HEADER
from bs4 import BeautifulSoup


class Driver:
    def __init__(self, root_url, cookies=None):
        if cookies is None:
            cookies = dict(over18='off', yes18='yes')
        self.logger = LOGGER
        self.root_url = root_url
        self.cookies = cookies
        self.header = HEADER
        self.now_content = None
        self.robots = None
        self.load_robots_txt()

    def load_robots_txt(self):
        self.robots = RobotFileParser()
        self.robots.set_url(self.root_url + '/robots.txt')
        self.robots.read()

    def get(self, url):
        try:
            sleep(ACCESS_DELAY)
            if self.robots.can_fetch("*", url):
                res = requests.get(url, headers=self.header, cookies=self.cookies)
                self.logger.debug(f"Access to {url}.")
                self.now_content = BeautifulSoup(res.text, 'html.parser')
            else:
                self.logger.warning(f"Access to this url is prohibited by robots.txt.\n<*>[URL={url}]")
        except Exception as e:
            self.logger.warning(e)

    def find_element_by_class_name(self, name):
        return self.now_content.select('.' + name)[0]

    def find_elements_by_class_name(self, name):
        return self.now_content.select('.' + name)

    def find_element_by_id(self, name):
        return self.now_content.select('#' + name)[0]

    def find_elements_by_id(self, name):
        return self.now_content.select('#' + name)

    def find_element_by_tag(self, name):
        return self.now_content.find_all(name)

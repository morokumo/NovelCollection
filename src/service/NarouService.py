import gzip
import io
import json
from time import sleep
from typing import List
import requests

from config import ACCESS_DELAY, NAROU_URL, LOGGER
from src.Model.NarouParameters import Category, Genre

from src.lib.Driver import Driver
from src.lib.Parser import parse_to_html
from src.lib.NarouConverter import connect_value, min_max
from src.lib.NarouParser import parse_to_NovelInformation, parse_to_novel_tags

from src.Model.Data import NovelContent
from src.Model.Parameters import GlobalSiteGenre
from src.Model.Data import RequestAttribute, Novel

from src.service.Repository import Repository


class NarouAPIService:
    def __init__(self, request_param: str = '?gzip=5&out=json'):
        self.base = 'https://api.syosetu.com/novelapi/api/'
        self.headers = {'content-type': 'application/json'}
        self.request_param = request_param

    def take_novel_information_from_api(self, req: RequestAttribute) -> List[Novel]:
        param = self.request_param
        param += f'&order={req.order}'
        param += '&word=' + connect_value(req.require_words)
        param += '&notword=' + connect_value(req.ng_words)

        param += '&biggenre=' + connect_value(req.require_category)
        param += '&notbiggenre=' + connect_value(req.ng_category)
        param += '&genre=' + connect_value(req.require_genre)
        param += '&notgenre=' + connect_value(req.ng_genre)
        param += '&userid=' + connect_value(req.user_ids)

        param += '&length=' + min_max(req.minimum_char_length, req.maximum_char_length)
        param += '&kaiwaritu=' + min_max(req.minimum_kaiwaritu, req.maximum_kaiwaritu)
        param += '&time=' + min_max(req.minimum_reading_time, req.maximum_reading_time)
        param += '&ncode=' + connect_value(req.ncodes)
        param += '&buntai=' + connect_value(req.novel_style)
        param += '&lastup=' + min_max(req.lastup_first, req.lastup_end)

        res = []
        st = req.start
        lim = req.limit
        while st <= lim:
            lim = min(500, req.limit - st)
            limit = f'&lim={lim}'
            start = f'&st={st}'

            sleep(ACCESS_DELAY)
            response = requests.get(self.base + param + limit + start, headers=self.headers)
            if response.status_code == 200:
                gzip_file = io.BytesIO(response.content)
                with gzip.open(gzip_file, 'rt')as f:
                    json_data = f.read()
                    data = json.loads(json_data)
                    for d in data[1:]:
                        for c in Category:
                            d['biggenre'] = c.value[1] if d['biggenre'] == int(c.value[0]) else d['biggenre']
                        for c in Genre:
                            d['genre'] = c.value[1] if d['genre'] == int(c.value[0]) else d['genre']
                        res.append(
                            Novel(parse_to_NovelInformation(d, GlobalSiteGenre.NAROU.value), parse_to_novel_tags(d)))
            st += 500

        return res


class NarouService:
    def __init__(self):
        self.driver = Driver(NAROU_URL)
        self.repository = Repository()
        self.logger = LOGGER
        self.site_genre = GlobalSiteGenre.NAROU.value

    def take_novels(self, novels: List[Novel]):
        for novel in novels:
            info = novel.novel_information
            tags = novel.novel_tags
            data = {'novel_code': info.novel_code, 'site_genre': self.site_genre}
            is_exists = len(self.repository.find_novel_information(data)) > 0

            if not is_exists:
                self.repository.insert_novel_information(info)
                for tag in tags:
                    self.repository.insert_novel_tag(tag)

            if info.novel_type:  # 連載中　
                for i in range(1, info.number_of_episode + 1):
                    self.take_and_save_content(info.novel_code, i)
            else:
                self.take_and_save_content(info.novel_code)

    def take_and_save_content(self, novel_code: str, episode: int = None):
        if episode is not None:
            url = f'{NAROU_URL}/{novel_code}/{episode}'
        else:
            url = f'{NAROU_URL}/{novel_code}/'

        episode = 1 if episode is None else episode
        data = {'novel_code': novel_code, 'site_genre': self.site_genre, 'episode': episode}
        if len(self.repository.find_novel_content(data)) > 0:
            return

        self.driver.get(url)
        title, body = self.parse_html_to_title_and_body()
        novel_content = NovelContent(novel_code=novel_code,
                                     site_genre=GlobalSiteGenre.NAROU.value,
                                     episode=episode,
                                     title=title,
                                     body=body)
        self.repository.insert_novel_content(novel_content)

    def parse_html_to_title_and_body(self) -> (str, str):
        try:
            title = self.driver.find_element_by_class_name('novel_title').text
        except:
            title = self.driver.find_element_by_class_name('novel_subtitle').text

        body = str(self.driver.find_element_by_id('novel_honbun'))
        body = parse_to_html(body)

        return title, body

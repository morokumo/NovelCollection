from config import LOGGER, HAMELN_URL
from src.lib.Driver import Driver
from src.lib.Parser import parse_to_html
from src.lib.HamelnParser import parse_to_novel_information

from src.Model.Data import NovelTag, NovelContent, NovelInformation
from src.Model.Parameters import GlobalSiteGenre

from src.service.Repository import Repository


class HamelnService:
    def __init__(self):
        self.repository = Repository()
        self.driver = Driver(HAMELN_URL)
        self.logger = LOGGER
        self.site_genre = GlobalSiteGenre.HAMELN.value
        self.parse_list = ['タイトル', '小説ID', '原作', '作者', 'あらすじ', 'タグ', '必須タグ',
                           '掲載開始', '話数', 'UA', '最新投稿', 'しおり', 'お気に入り', '開示設定', '合計文字数',
                           '感想', '感想受付設定', '平均文字数', '総合評価', '評価(黒→赤)', 'END', '']

    def take_novels(self, start, end):
        for novel_code in range(start, end):
            self.take_novel(novel_code=novel_code)

    def take_novel(self, novel_code):
        max_episode = self.take_and_save_information(novel_code)
        for episode in range(1, max_episode):
            self.take_and_save_content(novel_code, episode)

    def take_and_save_information(self, novel_code):
        data = {'novel_code': novel_code, 'site_genre': self.site_genre, 'episode_min': '-1'}
        novel_info = self.repository.find_novel_information(data)
        if len(novel_info) > 0:
            return novel_info[0].number_of_episode

        url = HAMELN_URL + f'?mode=ss_detail&nid={novel_code}'
        self.driver.get(url)

        key = self.driver.find_element_by_tag('td')
        output = {}
        index = 0
        for k in key:
            v = k.text
            if v == self.parse_list[index]:
                index += 1
            else:
                try:
                    output[self.parse_list[index - 1]] += '\n' + v
                except:
                    output[self.parse_list[index - 1]] = v

        novel_info = parse_to_novel_information(output)

        if novel_info is None:
            self.save_unknown_novel(novel_code)
            return -1

        tags = output['タグ'].split(' ') + output['必須タグ'].split(' ')
        tags.remove('')
        tags.remove('')
        if 'R-18' in tags:
            novel_info.is_r18 = True

        self.repository.insert_novel_information(novel_info)

        for tag_name in tags:
            novel_tag = NovelTag(tag_name, novel_code, self.site_genre)
            self.repository.insert_novel_tag(novel_tag)
        return novel_info.number_of_episode

    def take_and_save_content(self, novel_code, episode):
        data = {'novel_code': novel_code, 'site_genre': self.site_genre, 'episode': episode}
        if len(self.repository.find_novel_content(data)) > 0:
            return

        url = HAMELN_URL + f'novel/{novel_code}/{episode}.html'
        self.driver.get(url)
        try:
            body = self.driver.find_element_by_id('honbun')
            title = self.driver.find_element_by_tag('span')[1].text
            novel_content = NovelContent(novel_code=novel_code, site_genre=GlobalSiteGenre.HAMELN.value,
                                         episode=episode, title=title, body=parse_to_html(str(body)))
            self.repository.insert_novel_content(novel_content)
            return episode
        except Exception as e:
            self.logger.warning(e)

    def save_unknown_novel(self, novel_code):
        novel_info = NovelInformation(novel_code, self.site_genre, '-1', -1, '-1', '-1', '-1', '-1',
                                      False, False, '-1', '-1', -1, -1, -1, -1, -1, -1)
        self.repository.insert_novel_information(novel_info)

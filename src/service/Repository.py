import os
import sqlite3
from typing import List

from config import DATABASE_NAME, DATABASE_PATH, LOGGER
from src.lib.NarouConverter import convert_to_tuple

from src.Model.Data import NovelContent
from src.Model.Data import NovelInformation, NovelTag, Novel
from src.Model.sql import SQL


class Repository:
    def __init__(self):
        self.logger = LOGGER
        self.database_path = DATABASE_PATH
        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)
        self.database_name = DATABASE_NAME + '.db'
        self.database = os.path.join(self.database_path, self.database_name)
        self.conn = sqlite3.connect(self.database)
        self.create_tables()
        self.execute('PRAGMA foreign_keys=true;')

    def __del__(self):
        self.conn.close()

    def close(self):
        self.conn.close()

    def execute(self, sql: str, data: tuple = None):
        res = []
        try:
            if data is not None:
                res = self.conn.execute(sql, data)
            else:
                res = self.conn.execute(sql)

            self.conn.commit()

        except Exception as e:
            self.logger.warning(e)

        return res

    def create_tables(self):
        sql_list = [
            SQL.create_table_novel_information,
            SQL.create_table_novel_content,
            SQL.create_table_novel_tag,
        ]
        for sql in sql_list:
            self.execute(sql)

    def insert_novel_information(self, novel_information: NovelInformation, update=False):
        data = convert_to_tuple(novel_information)
        sql = SQL.insert_novel_information
        self.execute(sql, data)

    def insert_novel_content(self, novel_content: NovelContent, update=False):
        data = convert_to_tuple(novel_content)
        sql = SQL.insert_novel_content
        self.execute(sql, data)

    def insert_novel_tag(self, novel_tag: NovelTag, update=False):
        data = {'novel_code': novel_tag.novel_code, 'site_genre': novel_tag.site_genre, 'tag_name': novel_tag.tag_name}
        is_exist = len(self.find_novel_tag(data)) > 0
        if is_exist:
            self.logger.debug(f'this tag {novel_tag} is exits.')
            return

        data = convert_to_tuple(novel_tag)
        sql = SQL.insert_novel_tag
        self.execute(sql, data)

    def find_novel_information(self, params: dict, req: List = None):
        sql = SQL.find_novel_information
        data = []
        where = []
        try:
            if 'novel_code' in params and params['novel_code'] != '':
                where += [' novel_code = ? ']
                data += [params['novel_code']]
            if 'title' in params and params['title'] != '':
                where += [" title like ? "]
                data += [params['title']]
            if 'writer' in params and params['writer'] != '':
                where += [' writer = ? ']
                data += [params['writer']]
            if 'story' in params and params['story'] != '':
                where += [' story like ? ']
                data += [params['story']]

            if 'is_rensai' in params and 'is_tanpen' not in params:
                where += [' novel_type = ? ']
                data += ['1']
            elif 'is_rensai' not in params and 'is_tanpen' in params:
                where += [' novel_type = ? ']
                data += ['0']

            if 'is_end' in params:
                where += [' is_end = ? ']
                data += ['1']

            if 'site_genre' in params and params['site_genre'] != '':
                where += [' site_genre = ? ']
                data += [params['site_genre']]
            if 'genre' in params and params['genre'] == '' and params['category'] != '':
                where += [' category = ? ']
                data += [params['category']]
            elif 'genre' in params and params['genre'] != '':
                where += [' genre = ? ']
                data += [params['genre']]
            if 'length_min' in params and params['length_min'] != '':
                where += [' number_of_character >= ? ']
                data += [params['length_min']]
            if 'length_max' in params and params['length_max'] != '':
                where += [' number_of_character <= ? ']
                data += [params['length_max']]

            if 'fav_novel_cnt_min' in params and params['fav_novel_cnt_min'] != '':
                where += [' favorite_cnt >= ? ']
                data += [params['fav_novel_cnt_min']]
            if 'fav_novel_cnt_max' in params and params['fav_novel_cnt_max'] != '':
                where += [' favorite_cnt <= ? ']
                data += [params['fav_novel_cnt_max']]

            if 'review_cnt_min' in params and params['review_cnt_min'] != '':
                where += [' review_cnt >= ? ']
                data += [params['review_cnt_min']]
            if 'review_cnt_max' in params and params['review_cnt_max'] != '':
                where += [' review_cnt <= ? ']
                data += [params['review_cnt_max']]
            if 'all_hyoka_cnt_min' in params and params['all_hyoka_cnt_min'] != '':
                where += [' evaluation_point >= ? ']
                data += [params['all_hyoka_cnt_min']]
            if 'all_hyoka_cnt_max' in params and params['all_hyoka_cnt_max'] != '':
                where += [' evaluation_point <= ? ']
                data += [params['all_hyoka_cnt_max']]
            if 'episode_min' in params and params['episode_min'] != '':
                where += [' number_of_episode >= ? ']
                data += [params['episode_min']]
            else:
                where += [' number_of_episode > 0 ']
            if 'episode_max' in params and params['episode_max'] != '':
                where += [' number_of_episode <= ? ']
                data += [params['episode_max']]

            if 'r-18' in params:
                where += [' r_18 = ? ']
                data += ['1']
            if len(where) > 0:
                sql += ' where '
                for w in where:
                    sql += w + ' and '
                sql = sql[:len(sql) - 4]

        except Exception as e:
            self.logger.warning(e)

        if 'limit' in params:
            sql += ' limit ?;'
            data.append(params['limit'])
        else:
            sql += ';'
        res = []
        for row in self.execute(sql, tuple(data)):
            res.append(self.parse_to_novel_information(row))

        return res

    def find_novel_content(self, params: dict, req: List = None):
        sql = SQL.find_novel_content
        data = []
        where = []
        try:
            if 'novel_code' in params and params['novel_code'] != '':
                where += [' novel_code = ? ']
                data += [params['novel_code']]
            if 'site_genre' in params and params['site_genre'] != '':
                where += [' site_genre = ? ']
                data += [params['site_genre']]
            if 'episode' in params and params['episode'] != '':
                where += [' episode = ? ']
                data += [params['episode']]
            if 'title' in params and params['title'] != '':
                where += [' title like ? ']
                data += [params['title']]
            if 'body' in params and params['body'] != '':
                where += [' body like ? ']
                data += [params['body']]

            if len(where) > 0:
                sql += ' where '
                for w in where:
                    sql += w + ' and '
                sql = sql[:len(sql) - 4]

        except Exception as e:
            self.logger.warning(e)

        if 'limit' in params:
            sql += ' limit ?;'
            data.append(params['limit'])
        else:
            sql += ';'
        res = []
        for row in self.execute(sql, tuple(data)):
            res.append(self.parse_to_novel_content(row))
        return res

    def find_novel_tag(self, params: dict, req: List = None):
        sql = SQL.find_novel_tag
        data = []
        where = []
        try:
            if 'novel_code' in params and params['novel_code'] != '':
                where += [' novel_code = ? ']
                data += [params['novel_code']]
            if 'site_genre' in params and params['site_genre'] != '':
                where += [' site_genre = ? ']
                data += [params['site_genre']]
            if 'tag_name' in params and params['tag_name'] != '':
                where += [' tag_name like ? ']
                data += [params['tag_name']]
            if len(where) > 0:
                sql += ' where '
                for w in where:
                    sql += w + ' and '
                sql = sql[:len(sql) - 4]

        except Exception as e:
            self.logger.warning(e)

        if 'limit' in params:
            sql += ' limit ?;'
            data.append(params['limit'])
        else:
            sql += ';'
        res = []
        for row in self.execute(sql, tuple(data)):
            res.append(self.parse_to_novel_tag(row))
        return res

    def find_all_category(self):
        sql = 'select distinct category from novel_information order by category;'
        res = []
        for row in self.execute(sql):
            res.append(row[0])
        return res

    def find_all_genre(self):
        sql = 'select distinct genre from novel_information order  by genre;'
        res = []
        for row in self.execute(sql):
            res.append(row[0])
        return res

    def find_all_tag_name(self):
        sql = 'select distinct tag_name from novel_tag order by tag_name;'
        res = []
        for row in self.execute(sql):
            res.append(row[0])
        return res

    @staticmethod
    def parse_to_novel_information(row: tuple) -> NovelInformation:
        return NovelInformation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17])

    @staticmethod
    def parse_to_novel_content(row: tuple) -> NovelContent:
        return NovelContent(row[0], row[1], row[2], row[3], row[4])

    @staticmethod
    def parse_to_novel_tag(row: tuple) -> NovelTag:
        return NovelTag(row[1], row[2], row[3])

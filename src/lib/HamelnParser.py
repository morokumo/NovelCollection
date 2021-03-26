import re

from src.Model.Parameters import GlobalSiteGenre
from src.Model.Data import NovelInformation
import datetime


def parse_to_novel_information(output: dict):
    try:
        return NovelInformation(novel_code=output['小説ID'],
                                site_genre=GlobalSiteGenre.HAMELN.value,
                                title=output['タイトル'],
                                user_id=-1,
                                writer=output['作者'],
                                story=output['あらすじ'],
                                category='オリジナル' if
                                '現代 /' in output['原作'] or
                                'ファンタジー /' in output['原作'] or
                                'SF /' in output['原作'] or
                                '歴史 /' in output['原作'] or
                                'その他 /' in output['原作'] else '二次創作',
                                genre=output['原作'],
                                novel_type=True if '連載' in output['話数'] else False,
                                is_end=True if '完結' in output['話数'] else False,
                                first_upload_date=hameln_time_to_timestamp(output['掲載開始']),
                                last_upload_date=hameln_time_to_timestamp(output['最新投稿']),
                                number_of_episode=int(re.sub(r'\D', '', output['話数'])),
                                number_of_character=int(re.sub(r'\D', '', output['合計文字数'])),
                                favorite_cnt=int(re.sub(r'\D', '', output['お気に入り'])),
                                review_cnt=int(re.sub(r'\D', '', output['感想'])),
                                evaluation_point=int(re.sub(r'\D', '', output['総合評価'])),
                                number_of_evaluator=int(
                                    re.sub(r'\D', '', re.findall('投票者数:.*?人', output['評価(黒→赤)'])[0])),

                                )
    except Exception as e:
        return None


def hameln_time_to_timestamp(date_time: str):
    try:
        year = int(date_time[:4])
        month = int(date_time[5:7])
        day = int(date_time[8:10])
        hour = int(date_time[15:17])
        minute = int(date_time[18:20])
        return datetime.datetime(year, month, day, hour, minute)
    except:
        return datetime.datetime(0, 0, 0, 0, 0)

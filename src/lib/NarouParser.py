from typing import List

from werkzeug.datastructures import ImmutableMultiDict

from src.Model.Parameters import GlobalSiteGenre
from src.Model.Data import RequestAttribute, NarouNovelInformation, NovelInformation, NovelTag


def parse_to_RequestAttribute(form_dict: ImmutableMultiDict) -> RequestAttribute:
    return RequestAttribute(order=form_dict['order'],
                            limit=int(form_dict['limit'] or '0'),
                            start=int(form_dict['start'] or '0'),
                            require_words=form_dict['required_words'].split(','),
                            ng_words=form_dict['ng_words'].split(','),
                            )


def parse_to_NarouNovelInformation(dict_data: dict) -> NarouNovelInformation:
    return NarouNovelInformation(title=dict_data['title'],
                                 novel_code=dict_data['ncode'],
                                 user_id=dict_data['userid'],
                                 writer=dict_data['writer'],
                                 story=dict_data['story'],
                                 category=dict_data['biggenre'],
                                 genre=dict_data['genre'],
                                 tags=dict_data['keyword'].split(),
                                 first_upload_date=dict_data['general_firstup'],
                                 last_upload_date=dict_data['general_lastup'],
                                 novel_type=dict_data['novel_type'],
                                 is_end=dict_data['end'],
                                 number_of_episode=dict_data['general_all_no'],
                                 number_of_character=dict_data['length'],
                                 reading_time=dict_data['time'],
                                 is_longer_stopped=dict_data['isstop'],
                                 is_R15=dict_data['isr15'],
                                 is_bl=dict_data['isbl'],
                                 is_gl=dict_data['isgl'],
                                 is_zankoku=dict_data['iszankoku'],
                                 is_tensei=dict_data['istensei'],
                                 is_tenni=dict_data['istenni'],
                                 general_all_point=dict_data['global_point'],
                                 daily_point=dict_data['daily_point'],
                                 weekly_point=dict_data['weekly_point'],
                                 monthly_point=dict_data['monthly_point'],
                                 quarter_point=dict_data['quarter_point'],
                                 yearly_point=dict_data['yearly_point'],
                                 favorite_cnt=dict_data['fav_novel_cnt'],
                                 impression_cnt=dict_data['impression_cnt'],
                                 review_cnt=dict_data['review_cnt'],
                                 evaluation_point=dict_data['all_point'],
                                 number_of_evaluator=dict_data['all_hyoka_cnt'],
                                 kaiwaritu=dict_data['kaiwaritu'],
                                 updated_date=dict_data['novelupdated_at'])


def parse_to_NovelInformation(dict_data: dict, site_genre: int) -> NovelInformation:
    return NovelInformation(title=dict_data['title'],
                            site_genre=GlobalSiteGenre.NAROU.value,
                            novel_code=dict_data['ncode'],
                            user_id=dict_data['userid'],
                            writer=dict_data['writer'],
                            story=dict_data['story'],
                            category=dict_data['biggenre'],
                            genre=dict_data['genre'],
                            first_upload_date=dict_data['general_firstup'],
                            last_upload_date=dict_data['general_lastup'],
                            novel_type=True if dict_data['novel_type'] == 1 else False,
                            is_end=dict_data['end'],
                            number_of_episode=dict_data['general_all_no'],
                            number_of_character=dict_data['length'],
                            favorite_cnt=dict_data['fav_novel_cnt'],
                            review_cnt=dict_data['review_cnt'],
                            evaluation_point=dict_data['all_point'],
                            number_of_evaluator=dict_data['all_hyoka_cnt'],
                            )


def parse_to_novel_tags(dict_data: dict) -> List[NovelTag]:
    res = []
    for tag in dict_data['keyword'].split():
        res.append(NovelTag(tag_name=tag,
                            novel_code=dict_data['ncode'],
                            site_genre=GlobalSiteGenre.NAROU.value,
                            ))
    return res

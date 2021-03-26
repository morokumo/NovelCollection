from dataclasses import dataclass
from typing import List


@dataclass
class RequestAttribute:
    order: str
    limit: int = 5
    start: int = 0
    require_words: list = None
    ng_words: list = None
    include_words_in_title: bool = None
    include_words_in_outline: bool = None
    include_words_in_keyword: bool = None
    include_words_in_writer: bool = None
    require_category: list = None
    ng_category: list = None
    require_genre: list = None
    ng_genre: list = None
    user_ids: list = None
    is_R15: bool = None
    is_bl: bool = None
    is_gl: bool = None
    is_zankoku: bool = None
    is_tensei: bool = None
    is_tenni: bool = None
    is_tt: bool = None
    minimum_char_length: int = None
    maximum_char_length: int = None
    minimum_kaiwaritu: int = None
    maximum_kaiwaritu: int = None
    minimum_reading_time: int = None
    maximum_reading_time: int = None
    ncodes: list = None
    novel_type: str = None
    novel_style: list = None
    stop: bool = None
    lastup_first: int = None
    lastup_end: int = None
    is_pickup: bool = None


@dataclass
class NarouNovelInformation:
    novel_code: str
    site_genre: int
    title: str
    user_id: int
    writer: str
    story: str
    tags: list
    first_upload_date: str
    last_upload_date: str
    novel_type: bool
    number_of_episode: int
    number_of_character: int
    general_all_point: int
    category: str
    genre: str
    is_end: bool
    reading_time: int
    is_longer_stopped: bool
    is_R15: bool
    is_bl: bool
    is_gl: bool
    is_zankoku: bool
    is_tensei: bool
    is_tenni: bool
    daily_point: int
    weekly_point: int
    monthly_point: int
    quarter_point: int
    yearly_point: int
    favorite_cnt: int
    impression_cnt: int
    review_cnt: int
    evaluation_point: int
    number_of_evaluator: int
    kaiwaritu: float
    updated_date: str


@dataclass
class NovelInformation:
    novel_code: str
    site_genre: int

    title: str
    user_id: int
    writer: str
    story: str

    category: str
    genre: str

    novel_type: bool
    is_end: bool
    first_upload_date: str
    last_upload_date: str

    number_of_episode: int
    number_of_character: int

    favorite_cnt: int
    review_cnt: int
    evaluation_point: int
    number_of_evaluator: int

    is_r18: bool = False


@dataclass
class NovelTag:
    tag_name: str
    novel_code: str
    site_genre: str


@dataclass
class NovelContent:
    novel_code: str
    site_genre: int
    episode: int
    title: str
    body: str


@dataclass
class Novel:
    novel_information: NovelInformation
    novel_tags: List[NovelTag]
    novel_contents: List[NovelContent] = None

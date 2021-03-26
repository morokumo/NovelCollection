from enum import Enum


class Order(Enum):
    new = 'new', '新着更新順'
    favnovelcnt = 'favnovelcnt', 'ブックマーク数の多い順'
    reviewcnt = 'reviewcnt', 'レビューの多い順'
    hyoka = 'hyoka', '総合ポイントの高い順'
    hyokaasc = 'hyokaasc', '総合ポイントの低い順'
    dailypoint = 'dailypoint', '日間ポイントの高い順'
    weeklypoint = 'weeklypoint', '週間ポイントの高い順'
    monthlypoint = 'monthlypoint', '月間ポイントの高い順'
    quaterpoint = 'quaterpoint', '四半期ポイントの高い順'
    yearlypoint = 'yearlypoint', '年間ポイントの高い順'
    impressioncnt = 'impressioncnt', '感想の多い順'
    hyokacnt = 'hyokacnt', '評価者数の多い順'
    hyokacntasc = 'hyokacntasc', '評価者数の少ない順'
    weekly = 'weekly', '週間ユニークユーザーの多い順'
    lengthdesc = 'lengthdesc', '小説本文の文字が多い順'
    lengthasc = 'lengthasc', '小説本文の文字が少ない順'
    ncodedesc = 'ncodedesc', '新着投稿順'
    old = 'old', '更新が古い順'


class OutputStyle(Enum):
    none = '', '指定なし'
    ymal = 'ymal', 'ymal'
    json = 'json', 'json'
    php = 'php', 'php'
    atom = 'atom', 'atom'
    jsonp = 'jsonp', 'jsonp'


class Category(Enum):
    none = '-1', '指定なし'
    love = '1', '恋愛'
    fantasy = '2', 'ファンタジー'
    literature = '3', '文芸'
    sf = '4', 'SF'
    non_genre = '98', 'その他'
    other = '99', 'ノンジャンル'


class Genre(Enum):
    none = '-1', '指定なし'
    isekai_love = '101', '異世界（恋愛）'
    real_love = '102', '現実世界（恋愛）'
    high_fantasy = '201', 'ハイファンタジー（ファンタジー）'
    low_fantasy = '202', 'ローファンタジー（ファンタジー）'
    pure_literature = '301', '純文学（文芸）'
    human_drama = '302', 'ヒューマンドラマ'
    history = '303', '歴史'
    reasoning = '304', '推理'
    horror = '305', 'ホラー'
    action = '306', 'アクション'
    comedy = '307', 'コメディー'
    vr = '401', 'VRゲーム'
    space = '402', '宇宙'
    fantasy_science = '403', '空想科学'
    panic = '404', 'パニック'
    fairy_tale = '9901', '童話'
    poem = '9902', '詩'
    essai = '9903', 'エッセイ'
    replay = '9904', 'リプレイ'
    other = '9999', 'その他'
    non_genre = '9801', 'ノンジャンル'


class NovelType(Enum):
    none = '', '指定なし'
    tanpen = 't', '短編'
    serialized = 'r', '連載中'
    completed = 'er', '完結済み'
    serialized_and_completed = 're', '連載中と完結済み'
    tanpen_and_completed = 'ter', '短編と完結済み'


class NovelStyle(Enum):
    a = 'a'

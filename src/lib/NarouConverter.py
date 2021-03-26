from src.Model.NarouParameters import Category, Genre, Order


def min_max(min_value: int = None, max_value: int = None) -> str:
    res = ''
    if min_value is not None:
        res += f'{min_value}-'
        if max_value is not None:
            res += f'{max_value}'
    elif max_value is not None:
        res += f"-{max_value}"
    return res


def connect_value(value_list: list) -> str:
    res = ''
    if value_list is None:
        return res

    for v in value_list:
        if type(v) == str or type(v) == int:
            res += f'-{v}'
        else:
            res += f'-{v.value}'

    if len(res) > 0:
        res = res[1:]
    return res


def half_width_to_full_width_character(text: str) -> str:
    return text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))


def full_width_to_half_width_character(text: str) -> str:
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


def find_category_with_id(id: str):
    res = None
    for e in Category:
        if e.value[0] == id:
            res = e.value[1]
    assert res is None
    return res


def find_genre_with_id(id: str):
    res = None
    for e in Genre:
        if e.value[0] == id:
            res = e.value[1]
    assert res is None
    return res


def find_order_with_id(id: str):
    res = None
    for e in Order:
        if e.value[0] == id:
            res = e.value[1]
    assert res is None
    return res


def convert_to_tuple(cla):
    res = ()
    for _, v in cla.__dict__.items():
        res += (v,)
    return res

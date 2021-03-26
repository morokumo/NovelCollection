from enum import Enum


class GlobalSiteGenre(Enum):
    NAROU = 1
    HAMELN = 2
    KAKUYOMU = 3


class Site(Enum):
    all = ''
    narou = '1', '小説家になろう'
    hameln = '2', 'ハーメルン'
    kakuyomu = '3', 'カクヨム'


class Token(Enum):
    unk = '<unk>'
    pad = '<pad>'
    # sentence
    sos = '<sos>'
    eos = '<eos>'
    # download title
    tsos = '<tsos>'
    teos = '<teos>'
    # download tag (keyword)
    cksos = '<cksos>'
    ckeos = '<ckeos>'
    # download content title
    ctsos = '<ctsos>'
    cteos = '<cteos>'
    # download content body
    cbsos = '<cbsos>'
    cbeos = '<cbeos>'

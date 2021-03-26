import re


def parse_to_html(body) -> str:
    body = re.sub('<div.*?>', '', body)
    body = re.sub('</div>', '', body)
    body = re.sub('<p id=".*?">', '', body)
    body = re.sub('</p>', '\n', body)
    body = re.sub('<br>', '\n', body)
    body = re.sub('<br/>', '', body)
    body = re.sub('<ruby>', '', body)
    body = re.sub('</ruby>', '', body)
    body = re.sub('<rp>.*?</rp>', '', body)
    return body

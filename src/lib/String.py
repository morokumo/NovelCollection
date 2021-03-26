from typing import List

from src.Model.Data import Novel
from src.Model.Parameters import Token


def make_text_from_novels(novels: List[Novel],
                          separate_novel=False,
                          separate_episode=False,
                          with_token=False) -> List:
    response = []
    for novel in novels:
        res = ''
        if with_token:
            novel = add_token_to_novel(novel)

        info = novel.novel_information
        tags = novel.novel_tags
        tag_name_list = [tag.tag_name for tag in tags]

        res += info.title + '\n'
        res += '<tag> ' + " ".join(tag_name_list) + '</tag>\n'

        for content in novel.novel_contents:
            res += content.title + '\n'
            res += content.body + '\n'
            if separate_episode:
                res += '<*>separate_episode<*> \n'

        if separate_novel:
            res += '<*>separate_novel<*> \n'
        response.append(res)

    return response


def add_token_to_novel(novel: Novel):
    info = novel.novel_information
    info.title = Token.sos.value + info.title + Token.eos.value
    tags = novel.novel_tags
    if len(tags) > 0:
        # for i, tag in enumerate(tags):
        #     tags[i].tag_name = Token.sos.value + tag.tag_name + Token.eos.value
        tags[0].tag_name = Token.sos.value + tags[0].tag_name
        tags[len(tags) - 1].tag_name = tags[len(tags) - 1].tag_name + Token.eos.value

    contents = novel.novel_contents
    for i, content in enumerate(contents):
        contents[i].title = Token.sos.value + content.title + Token.eos.value
        body = ''
        for sentence in content.body.split('\n'):
            if sentence != '' and sentence != '　' and sentence != ' ':
                body += Token.sos.value + sentence + Token.eos.value + '\n'
            else:
                body += '\n'
        contents[i].body = body

    return Novel(novel_information=info,
                 novel_tags=tags,
                 novel_contents=contents)

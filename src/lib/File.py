import bz2
import io
import zipfile
from typing import List

import io
import tarfile
import gzip

from src.Model.Data import Novel
from src.service.Repository import Repository


def make_bz2_from_text(text: str):
    return bz2.compress(bytes(text))


def convert_novels_to_tar_gz(novels: List[Novel], encoding: str = 'utf-8') -> bytes:
    with io.BytesIO() as output_io:
        with tarfile.TarFile(fileobj=output_io, mode='w')as tar:
            for novel in novels:
                for novel_content in novel.novel_contents:
                    input_io = io.BytesIO(novel_content.body.encode(encoding))
                    info = tarfile.TarInfo(name=novel_content.title)
                    info.size = input_io.getbuffer().nbytes
                    tar.addfile(info, input_io)

        res = output_io.getvalue()
    return gzip.compress(res)


def test(novels: List[Novel], encoding: str = 'utf-8'):
    with tarfile.open('test.tar.gz', 'w:gz')as tar:
        for novel in novels:
            for novel_content in novel.novel_contents:
                text = novel_content.body
                input_io = io.BytesIO(text.encode(encoding))
                info = tarfile.TarInfo(name=novel_content.title)
                info.size = input_io.getbuffer().nbytes
                tar.addfile(info, input_io)



#
# repository = Repository()
# novel_information = repository.find_novel_information({})
# novels = []
# for info in novel_information:
#     data = {'novel_code': info.novel_code, 'site_genre': info.site_genre}
#     tags = repository.find_novel_tag(data)
#     contents = repository.find_novel_content(data)
#     novels.append(Novel(info, tags, contents))
#
# test(novels)
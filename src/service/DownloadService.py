from src.Model.Data import Novel
from src.lib.String import make_text_from_novels
from src.service.Repository import Repository


class DownloadService:
    def __init__(self):
        self.repository = Repository()

    def make(self, params: dict):
        novel_information = self.repository.find_novel_information(params)
        novels = []
        for info in novel_information:
            data = {'novel_code': info.novel_code, 'site_genre': info.site_genre}
            tags = self.repository.find_novel_tag(data)
            contents = self.repository.find_novel_content(data)
            novels.append(Novel(info, tags, contents))
        texts = make_text_from_novels(novels)
        return "".join(texts)

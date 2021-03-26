import gzip
from io import BytesIO

from flask import Blueprint, render_template, make_response, request, send_file

from config import LOGGER
from src.Model.Data import Novel
from src.Model.Parameters import Site
from src.lib.String import make_text_from_novels
from src.service.DownloadService import DownloadService
from src.service.Repository import Repository

app = Blueprint('download', __name__, url_prefix='/download')
logger = LOGGER
downloadService = DownloadService()


@app.route('/')
def home():
    repo = Repository()
    return render_template('download/home.html',
                           site=Site,
                           tag_name=[''] + repo.find_all_tag_name(),
                           category=[''] + repo.find_all_category(),
                           genre=[''] + repo.find_all_genre()
                           )


@app.route('/get_novel', methods=['POST'])
def get_novel():
    response = make_response(render_template('index.html'))
    repository = Repository()
    novel_information = repository.find_novel_information(request.form)
    novels = []
    for info in novel_information:
        data = {'novel_code': info.novel_code, 'site_genre': info.site_genre}
        tags = repository.find_novel_tag(data)
        contents = repository.find_novel_content(data)
        novels.append(Novel(info, tags, contents))
    response.data = "".join(make_text_from_novels(novels))
    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
    gzip_file.write(response.data)
    gzip_file.close()
    response.data = gzip_buffer.getvalue()
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Length'] = len(response.data)
    response.headers['Content-Disposition'] = 'attachment; filename=novels.gz'
    return response

# NovelCollection

NLPを行うにあたって，大量にデータが欲しかったので作ったもの

## Feature
- [小説家になろう](https://syosetu.com)，[ハーメルン](https://syosetu.org)にて掲載されている小説の収集アプリ
- タイトル，あらすじ，本文,etc...　を取得
- Robots.txtに基づいてアクセスが禁止されている場所にはアクセスをしない
- データベースによって検索，ダウンロード
- 「Librahack事件」に基づいてアクセス間隔を1秒以上に　（Default 3 seconds）
- このアプリは情報解析を目的として作成
  

- 自分が使えればいいアプリだったのでUIはないに等しいです　時間があれば作りたい

## setup (dev)
1. `git clone {this repository} `
2. `pip install requirements.txt`
3. `python app.py`
4. Access to http://localhost:5000




# misskey-crawler

<!--![Coverage reports](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/shift4869/ad61760f15c4a67a5c421cf479e3c7e7/raw/01_MediaGathering.json)-->

## 概要
- Misskeyでリアクションをつけたノートについて、メディアをDLし、情報をDBに蓄積するクローラ


## 特徴（できること）
- Misskeyでリアクションをつけたノートに添付されているメディアをDLする  
- Misskeyでリアクションをつけたノートの以下の情報をDBに蓄積する  
    - つけたリアクション  
    - ノートの情報（テキスト等）  
    - 投稿したユーザの情報  
    - メディアの情報  

※定期的な実行を前提としてますが機能としては同梱していないので「タスクのスケジュール」などOS標準の機能で定期実行してください。  
※windows 11でのみ動作確認をしております。  


## 前提として必要なもの
- Pythonの実行環境(3.11以上)
- MisskeyのAPIトークン

## 使い方
1. このリポジトリをDL
    - 右上の「Clone or download」->「Download ZIP」からDLして解凍
1. config/config_example.jsonの中身を自分用に編集してconfig/config.iniにリネーム
    - MisskeyのAPIトークンを設定する（必須）
    - ローカルの保存先パスを設定する（必須）
1. python misskey_crawler.pyで実行する
1. 出力されたmc_db.dbをsqliteビュワーで確認する
1. ローカルの保存先パスにメディアが保存されたことを確認する


## License/Author
[MIT License](https://github.com/shift4869/misskey-crawler/blob/master/LICENSE)  
Copyright (c) 2023 - 2024 [shift](https://twitter.com/_shift4869)


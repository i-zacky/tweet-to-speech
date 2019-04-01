# tweet-to-speech

## 環境要件

* Python v3.7.1

## 環境構築

### pipenvのインストール
https://github.com/pypa/pipenv

### pyenv / Pythonのインストール
https://github.com/pyenv/pyenv

### direnvのインストール
https://github.com/direnv/direnv

### Cloud Text-to-Speech APIのサービスアカウントキーの作成
* 以下のURLを参考にText-to-Speech APIの利用登録をする  
  https://cloud.google.com/text-to-speech/docs/quickstart-protocol?hl=ja
* ダウンロードしたJsonファイル(サービスアカウントキー)を配置する
  ```bash
  $ cp app/config/tweet-to-speech.json.origin app/config/tweet-to-speech.json
  $ cat (downloaded json) > app/config/tweet-to-speech.json
  ```

### TwitterのDeveloper利用およびアプリケーション登録
* 以下のURLを参考にTwitterのDeveloperアカウント利用登録、およびアプリケーションの作成・登録  
  https://developer.twitter.com/en/docs/basics/apps/overview.html
* 登録したアプリケーションのConsumer API keysおよびAccess token & access token secretを取得する
* アプリケーション設定ファイルを配置する
  ```bash
  $ cp app/config/application.ini.origin app/config/application.ini
  ```
* 取得したキー情報をapplication.ini(設定ファイル)に記載する

### direnvの設定
* 設定ファイルの配置
  ```bash
  $ cp .envrc.origin .envrc
  $ echo "export GOOGLE_APPLICATION_CREDENTIALS=\"(path to tweet-to-speech.json)\"" > .envrc.origin
  ```

## アプリケーション起動方法
```bash
$ pipenv shell
$ cd app
$ python tweet_to_speech.py
```
⇒ `out` ディレクトリにmp3ファイルが保管されていきます

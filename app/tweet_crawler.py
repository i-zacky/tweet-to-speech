# -*- coding: utf-8 -*-
import configparser
import tweepy
import emoji
import re
from google.cloud import texttospeech
import datetime

'''
* 設定ファイルの読み込み
  - アプリケーション設定ファイル(application.ini)
  - ツイート収集対象のユーザーリスト(user-list.txt)
* Cloud Text to Speechのインスタンス化
'''
users = open('user-list.txt')

conf = configparser.ConfigParser()
conf.read('application.ini')
consumer_key = conf.get('twitter', 'consumer_key')
consumer_secret = conf.get('twitter', 'consumer_secret')
access_token = conf.get('twitter', 'access_token')
access_token_secret = conf.get('twitter', 'access_token_secret')

client = texttospeech.TextToSpeechClient()


def crawling_tweet():
    """
    Twitter APIを利用して対象ユーザーのツイートを収集する
    収集したツイートはGoogle Cloud Text to Speech APIへ連携し、
    音声読み上げデータとしてmp3に変換し、保存する
    :return:
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = []
    for user in users:
        print('crawling tweet at: {}'.format(user))
        # 各ユーザーの最新ツイートを1件取得(ただしリツイートは収集対象外)
        for tweet in api.user_timeline(screen_name=user, count=1):
            if hasattr(tweet, 'retweeted_status'):
                continue

            tweet.text = format_tweet(tweet.text)
            tweets.append(tweet)

    for tweet in tweets:
        print('convert text to speech. id: {}\n'.format(tweet.id_str))
        text_to_speech(tweet)


def format_tweet(text):
    """
    ツイートの文字列から絵文字と画像のURLを除去する
    :param text:
    :return:
    """
    emoji_removed = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
    return re.sub(r'https?:\/\/.*[\r\n]*', '', emoji_removed, flags=re.MULTILINE)


def text_to_speech(tweet):
    """
    ツイートをGoogle Cloud Text to Speech APIを利用して音声データに変換する
    :param tweet:
    :return:
    """
    synthesis_input = texttospeech.types.SynthesisInput(text=tweet.text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ja',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d_%H%M%S_%f')
    with open('../out/{}.mp3'.format(filename), 'wb') as out:
        out.write(response.audio_content)


if __name__ == '__main__':
    crawling_tweet()

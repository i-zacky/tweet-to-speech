import configparser
import tweepy
import emoji
import re

'''
設定ファイルの読み込み
* アプリケーション設定ファイル(application.ini)
* ツイート収集対象のユーザーリスト(user-list.txt)
'''
users = open('user-list.txt')

conf = configparser.ConfigParser()
conf.read('application.ini')
consumer_key = conf.get('twitter', 'consumer_key')
consumer_secret = conf.get('twitter', 'consumer_secret')
access_token = conf.get('twitter', 'access_token')
access_token_secret = conf.get('twitter', 'access_token_secret')


def format_tweet(text):
    """
    ツイートの文字列から絵文字と画像のURLを除去する
    :param text:
    :return:
    """
    emoji_removed = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
    return re.sub(r'https?:\/\/.*[\r\n]*', '', emoji_removed, flags=re.MULTILINE)


'''
Twitter APIを利用して対象ユーザーのツイートを収集する
収集したツイートはGoogle Cloud Text to Speech APIへ連携し、
音声読み上げデータとしてmp3に変換し、保存する
'''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for user in users:
    # 各ユーザーの最新ツイートを1件取得
    tweets = api.user_timeline(screen_name=user, count=1)

    for tweet in tweets:
        # リツイートは収集対象外とする
        if hasattr(tweet, 'retweeted_status'):
            continue

        print("created_at:{}, id:{}, screen_name:{}".format(
            tweet.created_at,
            tweet.id_str,
            user
        ))
        print(format_tweet(tweet.text))
        print('---------------------------------------------')

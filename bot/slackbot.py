import time
import configparser
from slackclient import SlackClient

from router.listener import MsgListener

class SlackBot:
    def __init__(self, channel=None, user=None):
        config = configparser.ConfigParser()
        config.read('./config/config.ini')

        self.sc = SlackClient(config['SLACKER']['TOKEN'])
        self.channel = channel
        self.user = user

        self.listener = MsgListener(self)

    def start_session(self):
        if self.sc.rtm_connect(with_team_state=False):
            while True:
                msg = self.sc.rtm_read()

                if len(msg):
                    self.listener.handle(msg[0])
                    time.sleep(0.5)
        else:
            print('바이 바이')

    def send_message(self, text=None, attachments=None, as_user=True):
        self.sc.api_call(
            'chat.postMessage',
            channel = self.channel,
            text = text,
            attachments = attachments,
            as_user = as_user
        )


if __name__ == '__main__':
    slack = SlackBot(channel='#general')

    dict = dict()
    dict['pretext'] = 'content'
    dict['title'] = 'title'
    dict['title_link'] = 'https://www.naver.com'
    dict['fallback'] = 'notice'
    dict['text'] = '본문 텍스트'
    dict['mrkdwn_in'] = ['text', 'pretext']
    slack.send_message(text='Hello from python :tada:', attachments=[dict])

    slack.start_session()
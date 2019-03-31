from .router import MsgRouter

class MsgListener:
    def __init__(self, slackbot):
        self.slackbot = slackbot
        self.router = MsgRouter(self.slackbot)

    def handle(self, msg):
        if self.is_message(msg):
            self.handle_user_message(msg)

    def handle_user_message(self, msg):
        msg_text = msg.get('text')
        msg_ner = msg_text.split(' ')
        print(msg_ner)
        self.router.route_msg(msg_ner)

    def is_message(self, msg):
        msg_type = msg.get('type')
        if msg_type == 'message':
            return True
        else:
            return False

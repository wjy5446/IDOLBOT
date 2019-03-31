from .function.weather import Weather

class MsgRouter:
    def __init__(self, slackbot):
        self.slackbot = slackbot
        self.skill_weather = Weather()

    def route_msg(self, msg_ner):
        if '날씨' in msg_ner:
            if '지금' in msg_ner:
                print('실행')
                attachments = self.skill_weather.tell_current_forecast()
                print(attachments)
                self.slackbot.send_message(attachments=[attachments])

            if '오늘' in msg_ner:
                print('실행')
                attachments = self.skill_weather.tell_today_forecast()
                self.slackbot.send_message(attachments=attachments)
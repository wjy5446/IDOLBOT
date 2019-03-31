import datetime
import configparser
from collections import Counter

import forecastio

'''
Weather class
날씨를 알려주는 기능

기능
- 현재 날씨 알림
- 오늘 날씨 일정 알림
- 특정 날짜 날씨 알

summary version

detail version
'''

class Weather(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('./config/config.ini')
        self.config = self.config['WEATHER']

    def tell_current_forecast(self):
        self.now_date = datetime.datetime.now()

        self.set_forecastio()

        current_forecast = self.forecast.currently()

        current_summary = current_forecast.summary
        current_icon = current_forecast.icon
        current_time = current_forecast.time
        current_temperature = current_forecast.temperature
        current_precipProbability = current_forecast.precipProbability

        dict_attachments= {}
        dict_attachments['pretext'] = '오늘 날씨예요!'
        dict_attachments['color'] = '#ff69b4'
        dict_attachments['title'] = '오늘의 날씨 : {}'.format(current_time)
        dict_attachments['fields'] = [
            {
                'title': '요약',
                'value': ':cloud:',
                'short': False
            },
            {
                'title': '온도',
                'value': '{} 도'.format(current_temperature),
                'short': True
            },
            {
                'title': '정확도',
                'value': '{} %'.format(current_precipProbability),
                'short': True
            }
        ]

        return dict_attachments

    def tell_today_forecast(self):

        current_date = datetime.datetime.now()
        today_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 6, 0, 0)
        self.set_forecastio(today_date)

        hourly_forecast = self.forecast.hourly()
        summary_weather = self.summary_daily_forecast(hourly_forecast)

        dict_att_morning = {}
        dict_att_morning['pretext'] = '오늘 날씨예요!'
        dict_att_morning['color'] = '#ff4000'
        dict_att_morning['title'] = '오전'
        dict_att_morning['text'] = '06:00-12:00 :city_sunrise:'
        dict_att_morning['fields'] = [
            {
                'title': 'Summary',
                'value': summary_weather['morning']['summary'],
                'short': True
            },
            {
                'title': 'Icon',
                'value': summary_weather['morning']['icon'],
                'short': True
            },
            {
                'title': 'Temperature',
                'value': round(summary_weather['morning']['avg_temp'], 2),
                'short': True
            },
            {
                'title': 'Humnity',
                'value': round(summary_weather['morning']['avg_hum'], 2),
                'short': True
            }
        ]

        dict_att_afternoon = {}
        dict_att_afternoon['color'] = '#2E9AFE'
        dict_att_afternoon['title'] = '오후'
        dict_att_afternoon['text'] = '12:00-18:00 :cityscape:'
        dict_att_afternoon['fields'] = [
            {
                'title': 'Summary',
                'value': summary_weather['afternoon']['summary'],
                'short': True
            },
            {
                'title': 'Icon',
                'value': summary_weather['afternoon']['icon'],
                'short': True
            },
            {
                'title': 'Temperature',
                'value': round(summary_weather['afternoon']['avg_temp'], 2),
                'short': True
            },
            {
                'title': 'Humnity',
                'value': round(summary_weather['afternoon']['avg_hum'], 2),
                'short': True
            }
        ]

        dict_att_night = {}
        dict_att_night['color'] = '#0431B4'
        dict_att_night['title'] = '저녁'
        dict_att_night['text'] = '18:00-24:00 :night_with_stars:'
        dict_att_night['fields'] = [
            {
                'title': 'Summary',
                'value': summary_weather['night']['summary'],
                'short': True
            },
            {
                'title': 'Icon',
                'value': summary_weather['night']['icon'],
                'short': True
            },
            {
                'title': 'Temperature',
                'value': round(summary_weather['night']['avg_temp'], 2),
                'short': True
            },
            {
                'title': 'Humnity',
                'value': round(summary_weather['night']['avg_hum'], 2),
                'short': True
            }
        ]

        dict_att_dawn = {}
        dict_att_dawn['color'] = '#B43104'
        dict_att_dawn['title'] = '새벽'
        dict_att_dawn['text'] = '24:00-06:00 :bridge_at_night:'
        dict_att_dawn['fields'] = [
            {
                'title': 'Summary',
                'value': summary_weather['dawn']['summary'],
                'short': True
            },
            {
                'title': 'Icon',
                'value': summary_weather['dawn']['icon'],
                'short': True
            },
            {
                'title': 'Temperature',
                'value': round(summary_weather['dawn']['avg_temp'], 2),
                'short': True
            },
            {
                'title': 'Humnity',
                'value': round(summary_weather['dawn']['avg_hum'], 2),
                'short': True
            }
        ]

        return [dict_att_morning, dict_att_afternoon, dict_att_night, dict_att_dawn]



    def tell_tomorrow_forecast(self):
        dict_count_weather = {}

        tomorrow_local = self.now_date_local + datetime.timedelta(days=1)
        tomorrow_local = datetime.datetime(tomorrow_local.year, tomorrow_local.month, tomorrow_local.day, 6, 0, 0)

        forecast = forecastio.load_forecast(self.config['API_DARKSKY'].get('API_DARKSKY'),
                                            self.config['POS_SEOUL'].get('LAT'),
                                            self.config['POS_SEOUL'].get('LNG'),
                                            time=tomorrow_local
                                            )
        hourly_forecast = forecast.hourly()
        summary_weather = self.summary_daily_forecast(hourly_forecast)

        attachments_dict = {}
        attachments_dict['pretext'] = "내일 날씨 정보예요!!"
        attachments_dict['title'] = "내일 날씨"
        attachments_dict['text'] = """
		오전의 날씨: {weather_morning}, 온도 {temper_morning}, 습도 {humidity_morning}\n
		오후의 날씨: {weather_afternoon}, 온도 {temper_afternoon}, 습도 {humidity_afternoon}\n
		저녁의 날씨: {weather_night}, 온도 {temper_night}, 습도 {humidity_night}\n
		""".format(weather_morning=summary_weather['weather_morning'],
                   weather_afternoon=summary_weather['weather_afternoon'],
                   weather_night=summary_weather['weather_night'],
                   temper_morning=summary_weather['avg_temp_morning'],
                   temper_afternoon=summary_weather['avg_temp_afternoon'],
                   temper_night=summary_weather['avg_temp_night'],
                   humidity_morning=summary_weather['avg_hum_morning'],
                   humidity_afternoon=summary_weather['avg_hum_afternoon'],
                   humidity_night=summary_weather['avg_hum_night'])

        if len(summary_weather['list_rain_hour']) > 0:
            print(summary_weather['list_rain_hour'])
            rain_hour = " ".join(summary_weather['list_rain_hour'])
            dialog_rain_hour = "비는 {rain_hour}에 올테니 우산 준비해 나가세요".format(rain_hour=rain_hour)
            attachments_dict['text'] += dialog_rain_hour

        attachments = [attachments_dict]

        return attachments



    def tell_asked_date_forecast(self, month, day, year=None, hour=None, minute=None, second=None):
        now = self.now_date

        if year is None:
            year = now.year

        if hour is None:
            hour = 12

        if minute is None:
            minute = 0

        if second is None:
            second = 0

        asked_date_local = datetime.datetime(year, month, day, hour, minute, second)

        self.forecast = forecastio.load_forecast(self.config['API_DARKSKY'].get('API_DARKSKY'),
                                                 self.config['POS_SEOUL'].get('LAT'),
                                                 self.config['POS_SEOUL'].get('LNG'),
                                                 time=self.local2utc(asked_date)
                                                 )
        asked_date_forecast = self.forecast.currently()

        print(asked_date_forecast)

    def summary_daily_forecast(self, hourly_datas):
        """
        정보(주된 날씨만)
        오전 시간(6-12)
        오후 시간(12-18)
        저녁 시간(18-24)

        비 정보 만 출력
        """
        dict_weather_info = {}
        li_rain = []

        for data in hourly_datas.data:
            summary = data.icon
            temper = data.temperature
            humidity = data.humidity
            hour = self.utc2local(data.time).hour

            if 'rain' in summary:
                li_rain.append(str(hour))

            time = self.categorize_time(hour)
            if time not in dict_weather_info:
                dict_weather_info[time] = {'summary': [], 'icon': [], 'avg_temp': 0, 'avg_hum': 0}

            dict_weather_info[time]['summary'] += [summary]
            dict_weather_info[time]['avg_temp'] += temper
            dict_weather_info[time]['avg_hum'] += humidity

        for time, info in dict_weather_info.items():
            dict_weather_info[time]['summary'] = Counter(info['summary']).most_common(1)[0][0]
            dict_weather_info[time]['icon'] = self.cvtStr2Emoji(dict_weather_info[time]['summary'])
            dict_weather_info[time]['avg_temp'] /= 6
            dict_weather_info[time]['avg_hum'] /= 6

        dict_weather_info['li_rain'] = li_rain

        return dict_weather_info

    def utc2local(self, utc, offset=9):
        local = utc + datetime.timedelta(hours=offset)
        return local

    def local2utc(self, local, offset=9):
        utc = local - datetime.timedelta(hours=offset)
        return utc

    def set_forecastio(self, current_date=None):
        if current_date is None:
            current_date = datetime.datetime.now()

        self.forecast = forecastio.load_forecast(self.config.get('TOKEN'),
                                                 self.config.get('LAT_SEOUL'),
                                                 self.config.get('LNG_SEOUL'),
                                                 time=current_date
                                                 )

    def categorize_time(self, hour):
        if hour < 6:
            cate_time = 'dawn'
        elif hour < 12:
            cate_time = 'morning'
        elif hour < 18:
            cate_time = 'afternoon'
        else:
            cate_time = 'night'

        return cate_time

    def cvtStr2Emoji(self, cate_time):

        dict_weather_emoji = {'clear-day': ':sunny:', 'clear-night': ':full_moon:',
                              'rain': ':umbrella_with_rain_drops:', 'snow': ':snowflake:', 'sleet': ':snow_cloud:', 'wind': '', 'fog': ':fog:',
                              'cloudy': ':cloud:', 'partly-cloudy-day': ':partly_sunny:', 'partly-cloudy-night': ':partly_sunny:'
                              }

        return dict_weather_emoji[cate_time]

if __name__ == "__main__":
    w = Weather()
    w.tell_tomorrow_forecast()
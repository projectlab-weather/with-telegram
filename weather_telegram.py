import requests
from datetime import datetime
import xmltodict
import telepot
from telepot.loop import MessageLoop

def get_current_date_string():
    current_date = datetime.now().date()
    return current_date.strftime("%Y%m%d")

def get_current_hour_string():
    now = datetime.now()
    if now.minute < 45:
        if now.hour == 0:
            base_time = "2330"
        else:
            pre_hour = now.hour - 1
            if pre_hour < 10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"

    return base_time

def forecast(nx, ny):
    keys = '공공데이터에서 제공 받은 기상청 API'
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params = {
        'serviceKey': keys,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': get_current_date_string(),
        'base_time': get_current_hour_string(),
        'nx': nx,
        'ny': ny
    }

    # 값 요청
    res = requests.get(url, params=params)

    # XML -> 딕셔너리
    xml_data = res.text
    dict_data = xmltodict.parse(xml_data)

    # 값 가져오기
    weather_data = dict()
    for item in dict_data['response']['body']['items']['item']:
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['fcstValue']
        if item['category'] == 'REH':
            weather_data['hum'] = item['fcstValue']
        if item['category'] == 'SKY':
            weather_data['sky'] = item['fcstValue']
        if item['category'] == 'PTY':
            weather_data['sky2'] = item['fcstValue']

    return weather_data

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        location = msg['text']
        if location.lower() == '/start':
            bot.sendMessage(chat_id, '날씨 정보를 얻고 싶은 지역의 이름을 입력하세요.')
        else:
            # 직접 위도와 경도를 지정
            if location.lower() == '서울':
                nx, ny = 60, 127  # 서울의 위도와 경도
            elif location.lower() == '부산':
                nx, ny = 98, 76  # 부산의 위도와 경도
            elif location.lower() == '군산':
                nx, ny = 56, 92 
            elif location.lower() == '익산':
                nx, ny = 60, 91  
            elif location.lower() == '전주':
                nx, ny = 63, 89  
            elif location.lower() == '김제':
                nx, ny = 59, 68
            elif location.lower() == '인천':
                nx, ny = 55, 124 
            elif location.lower() == '대구':
                nx, ny = 89, 90  
            elif location.lower() == '광주':
                nx, ny = 58, 74  
            elif location.lower() == '울릉도':
                nx, ny = 127, 127 
            elif location.lower() == '독도':
                nx, ny = 144, 123  
            elif location.lower() == '경주':
                nx, ny = 100, 91 
            elif location.lower() == '안동':
                nx, ny = 91, 106
            elif location.lower() == '세종':
                nx, ny = 66, 103
            elif location.lower() == '울산':
                nx, ny = 102, 84 
            elif location.lower() == '파주':
                nx, ny = 56, 131   
            else:
                bot.sendMessage(chat_id, '해당 지역의 날씨 정보를 찾을 수 없습니다.')
                return

            # 위도와 경도 값을 forecast 함수에 전달하여 날씨 정보 가져오기
            weather_data = forecast(nx, ny)

            # 날씨 정보 출력
            str_sky = f"{location} 날씨 정보:\n"
            if 'sky' in weather_data and 'sky2' in weather_data:
                str_sky += "날씨: "
                if weather_data['sky2'] == '0':
                    if weather_data['sky'] == '1':
                        str_sky += "맑음"
                    elif weather_data['sky'] == '3':
                        str_sky += "구름많음"
                    elif weather_data['sky'] == '4':
                        str_sky += "흐림"
                elif weather_data['sky2'] == '1':
                    str_sky += "비"
                elif weather_data['sky2'] == '2':
                    str_sky += "비와 눈"
                elif weather_data['sky2'] == '3':
                    str_sky += "눈"
                elif weather_data['sky2'] == '5':
                    str_sky += "빗방울이 떨어짐"
                elif weather_data['sky2'] == '6':
                    str_sky += "빗방울과 눈이 날림"
                elif weather_data['sky2'] == '7':
                    str_sky += "눈이 날림"
                str_sky += "\n"
            if 'tmp' in weather_data:
                str_sky += f"온도: {weather_data['tmp']}°C\n"
            if 'hum' in weather_data:
                str_sky += f"습도: {weather_data['hum']}%"
            
            bot.sendMessage(chat_id, str_sky)
            bot.sendMessage(chat_id, '날씨 정보를 얻고 싶은 지역의 이름을 입력하세요.')

TOKEN = '텔레그램 토큰 key'  # 텔레그램 봇의 API 토큰을 설정해야 합니다.

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

print('Listening ...')
while True:
    pass
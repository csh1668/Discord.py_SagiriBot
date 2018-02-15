#-*- coding:utf-8 -*-
# Discord.py 날씨 알리미 봇

import requests
import discord
import asyncio
import os
import random
import urllib.request


client = discord.Client()

client_id = "NAVER API ID" # 네이버 API
client_secret = "NAVER API SECRET" # 네이버 API 비밀번호

location = 0 # 주사위 게임 위치 
turn = 0 # 주사위 게임 턴

yabawi_money = 100 # 야바위 기본돈

@client.event
async def on_ready():
    print("="*20)
    print(client.user.name)
    print('봇 작동 중') 
    print("="*20)
@client.event
async def on_message(message):
    global w
    global location
    global turn
    global yabawi
    global yabawi_money
    global i
    global msg
    await client.change_presence(game=discord.Game(name='!명령 를 통해 명령어 확인')) # ~~~ playing
    if message.author != client.user: # 봇이 봇에게 명령하지 못합니다.
        
        if message.content.startswith('!명령'): # !commands
            print("질문 '!명령'를 요청받았다.")
            msg = await client.send_message(message.channel, """
모든 명령어 앞에는 항상 !를 붙입니다.
날씨, 주사위, 야바위(작동 안함), 주인, 삭제, 번역기영한, 번역기한영, 이미지
""") # bot's answer
        elif message.content.startswith('!삭제'):
            msg = await client.send_message(message.channel, "삭제 가즈아")
            await client.delete_message(msg)
        
        elif message.content.startswith('!주인'):
            emm = message.content
            em = discord.Embed(title='↑ 얘가 만듦', description='딱히 적을거 없음', colour=0xDEADBF)
            em.set_author(name='! 사기리 노예', icon_url=client.user.avatar_url)
            await client.send_message(message.channel, embed=em)
        
    # 현재 날씨를 알려주는 코드
        elif message.content.startswith('!날씨'): # !weather
            a = requestCurrentWeather('강원', '원주시', '신림면')
            print("질문 '!날씨'를 요청받았다.")
            mgs = await client.send_message(message.channel, '현재 강원도 원주시 신림면의 날씨는\n' + w + '\n입니다.')

        elif message.content.startswith('cheat'):
            print( "누군가가 치트를 사용했다.")
            location += 20
        elif message.content.startswith('!주사위'): #dice game
            print("주사위 게임을 시작한다.")
            dice = random.randrange(1,6) # 주사위 눈의 수
            turn +=1
            location += dice
            msg = await client.send_message(message.channel,  '주사위의 눈은 {0}이므로 {0}칸 앞으로 갑니다. {1}/20, {2}턴째.'.format(dice, location, turn))
        elif location < 0:
            location == 0
        elif location == 5:
            location -= 3
            msg =await client.send_message(message.channel, '이런! 뱀을 만났습니다! 뒤로 3칸 갑니다. {}/20'.format(location))
        elif location == 12:
            location -= 4
            msg = await client.send_message(message.channel, '이런! 사자를 만났습니다! 뒤로 4칸 갑니다. {}/20'.format(location))
        elif location == 16:
            location -= 3
            msg = await client.send_message(message.channel, '이런! 뱀을 만났습니다! 뒤로 3칸 갑니다. {}/20'.format(location))
        elif location == 7:
            location += 2
            msg = await client.send_message(message.channel, '와우! 사다리입니다! 앞으로 2칸 갑니다. {}/20'.format(location))
        elif location == 15:
            location += 2
            msg = await client.send_message(message.channel, '와우! 사다리입니다! 앞으로 2칸 갑니다. {}/20'.format(location))
        elif location >= 20:
            print("주사위 게임을 끝냈다.")
            location = 0
            msg = await client.send_message(message.channel, '무사히 목표 지점에 도착했습니다! 주사위는 ' + str(turn) + '번 던져졌습니다.')
            turn = 0

        elif message.content.startswith('!야바위'):
            print("야바위 게임을 시작한다.")
            yabawi_money -= 50
            yabawi = random.randrange(1,3)
            m = message.content
            print(m[5:])
            if m[5:] == yabawi:
                yabawi_money += 150
                msg = await client.send_message(message.channel, """
{0}번입니다. 맞추셨네요.
150원 지급. 현재 돈: {1}
""" .format(yabawi, yabawi_money))
            elif m[5:] != yabawi and m[5:] != None:
                msg = await client.send_message(message.channel, """
{0}번입니다. 아쉽네요.
현재 돈: {1}
""" .format(yabawi, yabawi_money))
            elif m[5:] == None:
                msg = await client.send_message(message.channel, "'!야바위 1' 이런식으로 입력해주세요." .format(yabawi, yabawi_money))

        elif message.content.startswith('!번역기한영'):
            print("'!번역기' 요청을 받았다.")
            m = message.content
            encText = urllib.parse.quote(m[7:])
            data = "source=ko&target=en&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                await client.send_message(message.channel, response_body.decode('utf-8')[152:-4])
        elif message.content.startswith('!번역기영한'):
            print("'!번역기' 요청을 받았다.")
            m = message.content
            encText = urllib.parse.quote(m[7:])
            data = "source=en&target=ko&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                await client.send_message(message.channel, response_body.decode('utf-8')[152:-4])
        elif message.content.startswith('!이미지'):
            print("'!이미지' 요청을 받았다.")
            m = message.content
            encText = urllib.parse.quote(m[5:])
            url = "https://openapi.naver.com/v1/search/image?query=" + encText # json 결과
            # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                response_body.decode('utf-8').replace(' 'and':'and',', '')
                b=response_body.decode('utf-8').split('"')
                await client.send_message(message.channel, b[19])


            
# appKey는
# https://developers.sktelecom.com/
# 여기에서 받을 수 있다.
appKey = "WEATHER PLANET APPKEY"

# 현재 날씨(시간별) 요청 URL
# 일일 사용 제한 횟수에 따라 분별대신 시간별을 사용함.
url_hourly = "https://api2.sktelecom.com/weather/current/hourly"
# 현재 날씨(분별) 요청 URL 이건 그냥 장식
url_minutely = "http://api2.sktelecom.com/weather/current/minutely"

# 헤더
headers = {'Content-Type': 'application/json; charset=utf-8', 'appKey': appKey}


def hourly(weather):
    global w
    print("날씨")

    # 상대 습도
    humidity = weather['humidity']

    # 발표 시간
    timeRelease = weather['timeRelease']

    # 격자정보
    # 위도
    grid_la = weather['grid']['latitude']
    # 경도
    grid_lo = weather['grid']['longitude']
    # 시, 도
    grid_city = weather ['grid']['city']
    # 시, 군, 구
    grid_county = weather['grid']['county']
    # 읍, 면, 동
    grid_village = weather['grid']['village']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc  = weather ['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰 유뮤
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']
    
    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']

    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']
    w = '시간별 온도 ' + temperature_tc + '도, 최고 ' + temperature_tmax + '도, 최저 ' + temperature_tmin + '도, 하늘 ' + sky_name + ', 바람 ' + wind_wspd + 'm/s, 습도' + humidity + '%'
    print(w)

#현재 날씨(분별)
def minutely(weather):
    #print(weather)
    # 상대 습도
    humidity     = weather['humidity']

    # 기압정보
    # 현지기압(Ps)
    pressure_surface  = weather['pressure']['surface']
    # 해면기압(SLP)
    pressure_seaLevel  = weather['pressure']['seaLevel']

    # 관측소
    # 관측소명
    station_name      = weather['station']['name']
    # 관측소 지점번호(stnid)
    station_id      = weather['station']['id']
    # 관측소 유형
    #- KMA: 기상청 관측소
    #- BTN: SKP 관측소
    station_type  = weather['station']['type']
    # 위도
    station_latitude  = weather['station']['latitude']
    # 경도
    station_longitude = weather['station']['longitude']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']
    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    # 강우정보
    # 1시간 누적 강우량
    rain_sinceOntime   = weather['rain']['sinceOntime']
    # 일 누적 강우량
    rain_sinceMidnight = weather['rain']['sinceMidnight']
    # 10분 이동누적 강우량
    rain_last10min     = weather['rain']['last10min']
    # 15분 이동누적 강우량
    rain_last15min     = weather['rain']['last15min']
    # 30분 이동누적 강우량
    rain_last30min     = weather['rain']['last30min']
    # 1시간 이동누적 강우량
    rain_last1hour     = weather['rain']['last1hour']
    # 6시간 이동누적 강우량
    rain_last6hour     = weather['rain']['last6hour']
    # 12시간 이동누적 강우량
    rain_last12hour    = weather['rain']['last12hour']
    # 24시간 이동누적 강우량
    rain_last24hour    = weather['rain']['last24hour']

    str = '분별 온도 ' + temperature_tc + ', 최고 ' + temperature_tmax + ', 최저 ' + temperature_tmin + ', 하늘 ' + sky_name + ', 바람 ' + wind_wspd + ', 습도' + humidity
    print(str)

def requestCurrentWeather(city, county, village, isHourly = True):
    params = { "version": "1",
                "city": city,
                "county": county,
                "village": village }
    if isHourly:
        print("요청")
        response = requests.get(url_hourly, params=params, headers=headers)
    else:
        response = requests.get(url_minutely, params=params, headers=headers)

    if response.status_code == 200:
        print(response.status_code)
        print("변경")
        # json을 딕셔너리로 변경 
        response_body = response.json()
        print(response.json())
       
        #날씨 정보
        try:
            print("시도")
            if isHourly:
                print("시간별")
                weather_data = response_body['weather']['hourly'][0]
            else:
                print("분별")
                weather_data = response_body['weather']['minutely'][0]

            if isHourly:
                print("시간별2")
                
                hourly(weather_data)
                
            else:
                print("분별2")
                minutely(weather_data)
        except:
            print("except")
            pass

    else:
        print("에러")
        pass
        #에러


        



client.run('FUCK THE HACKERS LOL')

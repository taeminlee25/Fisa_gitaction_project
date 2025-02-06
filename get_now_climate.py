import requests 
import os
from datetime import datetime
from dotenv import load_dotenv
import pytz

# 서울 시간대로 현재 시간 가져오기
seoul_tz = pytz.timezone('Asia/Seoul')
seoul_time = datetime.now(seoul_tz)

load_dotenv()

def get_now_climate():
    AUTHKEY = os.getenv("AUTHKEY")
    # 예보지점의 x 좌표값 -> 서울시 마포구 상암동 좌표 : 58, 예보지점의 y 좌표값 -> 서울시 마포구 상암동 좌표 : 127
    nx, ny = 58, 127

    # 발표 일자는 오늘 날짜
    now = seoul_time
    date = now.strftime("%Y%m%d")
    time = now.strftime("%H%M")
    # 발표 시각 06시 발표(정시단위) -매시각 10분 이후 호출
    url = f"https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst?pageNo=1&numOfRows=1000&dataType=json&base_date={date}&base_time={time}&nx={nx}&ny={ny}&authKey={AUTHKEY}"

    # API 호출
    response = requests.get(url)
    response = response.json()

    # 상태 코드 확인
    if response['response']['header']["resultCode"] != "00":
        return "날씨 정보를 가져오지 못했습니다."
    else:
        # 기온 ℃ -> T1H
        temp = response['response']['body']['items']['item'][3]['obsrValue'] 
        # 1시간 강수량 mm -> RN1
        rn = response['response']['body']['items']['item'][2]['obsrValue']
        # 습도 % -> REH
        hum = response['response']['body']['items']['item'][1]['obsrValue']
        # 풍속 m/s -> WSD
        ws = response['response']['body']['items']['item'][-1]['obsrValue']

        return temp, rn, hum, ws



# README.md 파일 경로
README_PATH = "README.md"

# README.md 파일을 열고, 기존의 날씨 정보를 업데이트된 정보로 변경하여 저장하세요.
def update_readme():
    # get_now_climate() 함수를 호출하고 반환
    temp, rn, hum, ws = get_now_climate()

    now = seoul_time.strftime("%Y년 %m월 %d일 %H시 %M분")

    readme_content = f"""
# 마포구 상암동 초단기 실황 날씨 정보 🌤️

이 리포지토리는 기상청 API를 사용하여 서울 마포구 상암동의 날씨 정보를 업데이트합니다. 

🌡️ 기온: {temp} ℃
💧 강수량: {rn} mm
💦 습도: {hum} %
🌬️ 풍속: {ws} m/s

마지막 업데이트 시각: {now}    
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

# update_readme() 함수를 호출하여 README.md 파일을 업데이트하세요.
if __name__ == "__main__": # 이 파일이 직접 실행될 때만 update_readme() 함수를 호출합니다.
    update_readme()
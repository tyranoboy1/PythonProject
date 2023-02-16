import requests
import xmltodict
import json
import pandas as pd
import matplotlib.pylab as plt
import math
import re

corona19_id = []
corona19_date = []
corona19_no = []
corona19_country = []
corona19_personal = []
corona19_area = []
corona19_travel_history = []
corona19_contact_history = []
corona19_corrective = []
corona19_leave_status = []
corona19_moving_path =[]
corona19_idate =[]
corona19_mdate = []

key = '73567a6f7a73756e38384655755572'#api 인증키
total_information = 46302 #api의 총수는 46302 #19000개는 2021-02-03까지의 데이터 값이다 머신러닝을 위해 임의로 설정

for i in range(1, math.ceil(total_information / 1000) + 1):

    end = i * 1000
    start = end - 1000 + 1

    if end > total_information:
        end = total_information

    url = f'http://openapi.seoul.go.kr:8088/{key}/xml/Corona19Status/{start}/{end}/'
    req = requests.get(url)
    dict_data = xmltodict.parse(req.text)#xml 데이터를 dict으로 변환
    json_data = json.dumps(dict_data)#dict_data를 json문자열로 변환
    dict_data = json.loads(json_data)#json문자열을 파이썬 오브젝트로 변환

    for u in dict_data['Corona19Status']['row']:
        corona19_id.append(u['CORONA19_ID'])
        corona19_date.append(u['CORONA19_DATE'])
        corona19_no.append(u['CORONA19_NO'])
        corona19_country.append(u['CORONA19_COUNTRY'])
        corona19_personal.append(u['CORONA19_PERSONAL'])
        corona19_area.append(u['CORONA19_AREA'])
        corona19_travel_history.append(u['CORONA19_TRAVEL_HISTORY'])
        corona19_contact_history.append(u['CORONA19_CONTACT_HISTORY'])
        corona19_corrective.append(u['CORONA19_CORRECTIVE'])
        corona19_leave_status.append(u['CORONA19_LEAVE_STATUS'])
        corona19_moving_path.append(u['CORONA19_MOVING_PATH'])
        corona19_idate.append(u['CORONA19_IDATE'])
        corona19_mdate.append(u['CORONA19_MDATE'])

df = pd.DataFrame({"연번": corona19_id,
                   "확진일": corona19_date,
                   "환자번호": corona19_no,#삭제
                   "국적": corona19_country,#삭제
                   "환자정보": corona19_personal,#삭제
                   "지역":  corona19_area,
                   "여행력": corona19_travel_history,#삭제
                   "접촉력":  corona19_contact_history,#삭제
                   "조치사항":corona19_corrective,#삭제
                   "상태": corona19_leave_status,
                   "이동경로": corona19_moving_path,#삭제
                   "등록일": corona19_idate,#삭제
                   "수정일":  corona19_mdate,#삭제
                   })


# 연번, 확진일, 지역, 상태 말고는 다 삭제
df = df.drop(columns=["환자번호","국적","환자정보","여행력","접촉력","조치사항","이동경로","등록일","수정일"])
df['확진일'] = df['확진일'].apply(pd.to_datetime)

#날짜를 입력받고 확진자 수를 구해줌
def coronaday(dayc):
    numdate = df.loc[df["확진일"]==dayc, ["확진일"]]
    print(dayc, "->   총 확진자 수는 :", len(numdate), "입니다")
def cellectday():
    while True:
        dayz = input('날짜를 입력하세요(ex xxxx-xx-xx):')

        pat =r'(\d{4})-(\d{1,2})-(\d{1,2})'
        correctdate = bool(re.search(pat,dayz))
        if(correctdate):
            coronaday(dayz)
            break
        else:
            print("날짜형식이 아닙니다.")
            continue

#지역을 입력받고 확진자수를 구해줌
def coronaarea(area):
    numarea = df.loc[df["지역"] ==area, ["지역"]]
    print(area+ "의 확진자 수는 :", len(numarea), "입니다.")

def sellectcity():
    while True:
        area1=input("원하는 구를 입력하세요(ex 노원구):")

        pat =('강남구|강동구|강북구|관악구|광진구|구로구|금천구|노원구|동대문구|도봉구|동작구|마포구|서대문구|성동구|성북구|서초구|송파구|영등포구|용산구|양천구|은평구|종로구|중구|중랑구')
        selectarea = bool(re.search(pat, area1))
        if(selectarea):
            coronaarea(area1)
            break
        else:
            print("형식이 잘못되었습니다.")
            continue

#3-1(확진자 수 그래프(x = 날짜 y = 확진자수))
def corona19_graph():
    betweendata = (df['확진일']>='2021-02-26')&(df['확진일']<='2021-06-13')
    filtered_df = df.loc[betweendata]
    df_count = filtered_df['확진일'].value_counts().sort_index(ascending=False)#날짜별 확진자수를 세어줌
    corona19_num = pd.DataFrame(df_count)#새로 데이터프레임을 시켜줌
    corona19_num.columns = ["확진자수"]#행이름 확진자수 #종속변수가 될것임 y가 됨
    corona19_num['확진자수'].plot()
    plt.show()

#3-2누적 예방접종자수(x = 날짜 y = 예방접종자 수)
def vaccination_graph():
    vaccination_num = pd.read_excel('C:/Users/82102/PycharmProjects/pythonProject2/Today_vaccination.xls',usecols=[0,1])
    vaccination_num.index = vaccination_num['일자']
    vaccination_num['예방접종자수'].plot()
    plt.show()

#3-3인공머신을 위한 그래프(x = 누적 예방접종자수 y = 확진자수)
def machine_running_graph():
    vaccination_num = pd.read_excel(
        'C:/Users/82102/PycharmProjects/pythonProject2/Today_vaccination.xls',
        usecols=[0, 1]
    )
    between_data = (df['확진일']>='2021-02-26')&(df['확진일']<='2021-06-13')
    filtered_df = df.loc[between_data]

    df_count = filtered_df['확진일'].value_counts().sort_index(ascending=False) #날짜별 확진자수를 세어줌
    corona19_num = pd.DataFrame(df_count) # 새로 데이터프레임을 시켜줌
    corona19_num.columns = ["확진자수"] # 행이름 확진자수 #종속변수가 될것임 y가 됨
    corona19_num = corona19_num.reset_index(drop=True)# 인덱스를 초기화 시켜줌
    result_data = pd.concat([vaccination_num, corona19_num], axis=1)#df두개를 합쳐준다. (axis = 1) 행으로
    result_data.index = result_data['예방접종자수']
    result_data['확진자수'].plot()
    plt.show()

def SelectMenu():
    print("코로나 프로그램")
    print("1: 코로나 극복")
    print("2: 지역별 확진자 수")
    print("3: 확진 일수 별 확진 자 수")
    print("4: 그래프")
    print("0: 종료")
    print("                    ")
    return input("번호를 선택하세요 : ")



def theory():
    print(
        """         I want to be a day to give the best of me
             최선을 다하는 하루가 되길 바라죠
             My finest day is yet anonymous.
             내 삶의 가장 좋은 날은 아직 오지 않았으니까요.

                 -휘트니 휴스턴(whitney Houston)-
        """)


def areap():
    sellectcity()



def dayp():
    cellectday()


def graphchose():
    print("1: 확진자수 그래프(x = 날짜, y = 확진자 수)")
    print("2: 누적 백신 접종자수 그래프(x = 날짜, y = 누적 접종자수)")
    print("3: 누적 백신 접종자수에 따른 확진자수 (x = 누적 접종자수, y = 확진자 수)")



def clearconsole():
    next = input(' ')
    if(next == ' '):
        print('\n'* 9)








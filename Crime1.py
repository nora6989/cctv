import pandas as pd 
import numpy as np
import googlemaps 
from sklearn import preprocessing 
import matplotlib.pyplot as plt 
import seaborn as sns 
import folium

crime_anal_police = pd.read_csv('./crime_in_Seoul.csv', thousands=',', encoding='euc-kr')
crime_anal_police.head()

gmaps_key = "AIzaSyA3PGHkcMudz-7XKWwCB9h9vQcYrxdSWOE"
gmaps = googlemaps.Client(key = gmaps_key)
gmaps.geocode('서울중부경찰서', language='ko')

station_name = []

for name in crime_anal_police['관서명'] :
    station_name.append('서울'+str(name[:-1])+'경찰서') # -1 전부 
station_name 

station_address = []
station_lat =[] # 위도 
station_lng =[] # 경도
for name in station_name: 
    tmp = gmaps.geocode(name, language='ko')
    station_address.append(tmp[0].get('formatted_address'))

    tmp_loc = tmp[0].get('geometry')
    station_lat.append(tmp_loc['location']['lat'])
    station_lng.append(tmp_loc['location']['lng'])
    print(name+'----->'+tmp[0].get('formatted_address'))

station_lat
station_lng

gu_name = []
for name in station_address:
    tmp = name.split()
    tmp_gu = [gu for gu in tmp if gu[-1] =='구'][0]
    print('***'+tmp_gu) 
    gu_name.append(tmp_gu)
gu_name

type(crime_anal_police) # <class 'pandas.core.frame.DataFrame'>
len(crime_anal_police['관서명']) # 31: 서울시내에 총 31개의 관할서가 존재함 
crime_anal_police['구별'] = gu_name 

crime_anal_police.head()

# 금천경찰서는 관악구 위치에 있어서 금천서는 제외 
crime_anal_police[crime_anal_police['관서명']=='금천서'] 
crime_anal_police 
crime_anal_police.loc[crime_anal_police['관서명']=='금천서', ['구별']]='금천구'
# 금천서를 찾아서 관악구로 되어있는 것을 금천구로 고쳐라
crime_anal_police.to_csv('./crime_in_Seoul_include_gu_name.csv',sep=',', encoding='utf-8')


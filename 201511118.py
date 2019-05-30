#-------------------------------------------------------------------------------
# Name:        parking_finder
# Purpose:     연휴 기간 무료주차장 탐색 및 분석 프로그램
#
# Author:      201511118_민성훈
#
# Created:     16-05-2019
# Copyright:   (c) 201511118_민성훈 2019
#-------------------------------------------------------------------------------

import pandas as pd
import folium
from datetime import datetime as date

def readfile() : #파일을 읽는 함수
    data = input("파일이름을 입력하시요. ->")
    datafile = pd.read_csv(data+'.csv', encoding = 'cp949')
    return datafile

def addArea(data) : #'지역구' 항목을 추가하는 함수
    adress = data['주소']
    aList = []
    for a in adress :
        temp = a.split(" ")
        aList.append(temp[1])
    data['지역구'] = aList
    return data

def mapping(aroundarea) : #주차장 정보를 표기하고 주차장 지도 html파일을 생성하는 함수
    while(1) :
        name = input("주차장명을 입력하여 주세요 ->\n"+"프로그램 종료를 원할 시 '종료'를 입력하십시오")
        namelist = list(aroundarea['주차장명'])
        if name == '종료' :
            print("프로그램이 종료되었습니다.")
            break
        elif name in namelist :
            print("###해당 주차장 정보 입니다.###")
            pointdata = aroundarea.loc[aroundarea['주차장명'] == name]
            parkdata = pointdata.iloc[:,[1,2,3,7]]
            for p in pointdata.iloc[:,[1,2,3,7]] :
                print(p, ":", list(pointdata[p])[0])
            latitude = list(pointdata['위도'])
            longitude = list(pointdata['경도'])
            point = [float(latitude[0]), longitude[0]]
            map = folium.Map(location = point, zoom_start = 18)
            folium.Marker(location = point, popup = name).add_to(map)
            map
            map.save(name+'.html')
            print("주차장 위치를 html파일로 생성하였습니다.")

        else : print("주차장명이 존재하지 않습니다.")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

data = readfile()
addArea(data)
areastr = ''
for a in sorted(list(set(data['지역구']))) :
    areastr = areastr + ' ' + a
areastr = '(' + areastr.strip().replace(" ",", ") + ')'
here = input("위치하고 있는 지역구를 선택하여 주십시오.\n"+areastr)
print(areastr[1:-1].split(", "))
if here in areastr[1:-1].split(", ") :
    aroundarea = data.loc[data['지역구'] == here]
    print("주변 주차장명은 다음과 같습니다.")
    print(list(aroundarea['주차장명']))
    mapping(aroundarea)
else : print("지역구 입력 오류입니다. 프로그램을 종료합니다.")
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame as df

# CU URL
cu = ""
# Emart24 URL
emart = ""


# ********** 여기만 건들것 **********
# csv_name 변수를 원하는 상품목록의 변수로 바꿔주면됨
csv_name = "cu"
# ********** 여기만 건들것 **********


# 상품명, 세일 항목, 가격 리스트 생성
product_list = []
sale_list = []
price_list = []

# url 설정
url_base = eval(csv_name)

# '1+1'상품부터 '4+1'상품까지 각 세일 항목 루프
for i in range(1, 5):
    event_type = "type=" + str(i)
    url = url_base.replace("type=1", event_type)
    # 각 세일 항목별 페이지 수 크롤링
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")
    # 예외처리 : 각 세일 항목의 상품이 하나도 없을 경우 패스
    try:
        page_base = int(bsObject.find("span", {"class":"current"}).text.strip().split(" ")[2]) + 1
    except:
        pass
    # 쓰레기값 걸러내기 위한 변수
    head = True
    tail = True
    # 각 항목의 페이지 루프
    for j in range(1, page_base):
        page = "page=" + str(j)
        url_use = url.replace("page=1", page)
        html = urlopen(url_use)
        bsObject = BeautifulSoup(html, "html.parser")
        # 상품명, 세일 항목 리스트 채우기
        for link in bsObject.find_all('strong'):
            value = link.text.strip()
            if tail:  # value가 "최근 게시글" ~ "현재 페이지 공유하기"가 아닐 경우 True
                if head:
                    head = False
                else:
                    if value == "최근 게시글":
                        tail = False
                    else:
                        # 리스트에 추가
                        value = value.replace("HEYROO", "헤이루")
                        value = value.replace("Vplan", "브이플랜")
                        value = value.replace("Dole", "돌")
                        value = value.replace("HEYROO", "헤이루")
                        value = value.replace("Vplan", "브이플랜")
                        value = value.replace("Dole", "돌")
                        value = value.replace("SPAR", "스파")
                        value = value.replace("GRN", "지알앤")
                        value = value.replace("SNJ", "에스앤제이")
                        value = value.replace("BIG", "빅")
                        value = value.replace("CVS", "씨브이에스")
                        value = value.replace("F&G", "에프앤지")
                        value = value.replace("New", "뉴")
                        value = value.replace("CJ", "씨제이")
                        value = value.replace("SF", "에스에프")
                        value = value.replace("CM", "센티미터")
                        value = value.replace("cm", "센티미터")
                        value = value.replace("ML", "밀리리터")
                        value = value.replace("ml", "밀리리터")
                        value = value.replace("GO", "고")
                        value = value.replace("XS", "엑스에스")
                        value = value.replace("UP", "업")
                        value = value.replace("GT", "지티")
                        value = value.replace("KG", "킬로그램")
                        value = value.replace("kg", "킬로그램")
                        value = value.replace("O/N", "오버나이트")
                        value = value.replace("C", "씨")
                        value = value.replace("V", "브이")
                        value = value.replace("s", "에스")
                        value = value.replace("T", "티")
                        value = value.replace("B", "비")
                        value = value.replace("X", "엑스")
                        value = value.replace("M", "미터")
                        value = value.replace("m", "미터")
                        value = value.replace("G", "그램")
                        value = value.replace("g", "그램")
                        value = value.replace("L", "리터")
                        value = value.replace("P", "피")
                        value = value.replace("N", "나이트")
                        value = value.replace("e", "이")
                        value = value.replace("F", "에프")
                        value = value.replace("W", "더블유")
                        value = value.replace("*", "에")
                        value = value.replace("%", "프로")
                        value = value.replace("&", "앤")
                        value = value.replace(".", "점")
                        value = value.replace("/", "")
                        value = value.replace("(", "")
                        value = value.replace(")", "")
                        value = value.replace(" ", "")
                        product_list.append(value)
                        sale_list.append(i)
            elif value == "현재 페이지 공유하기":
                tail = True
                head = True
        # 가격 리스트 채우기
        for link in bsObject.find_all("span", {"class":"text-muted small"}):
            value = int(link.text.strip().replace('(', "").replace(',', "").replace('원)', ""))
            # 총 가격 구하기
            if i == 1:
                value = value * 2
            elif i == 2:
                value = value * 3
                if value % 10 == 1:
                    value = value - 1
                elif value % 10 == 9:
                    value = value + 1
            elif i == 3:
                value = value * 4
            elif i == 4:
                value = value * 5
            price_list.append(value)

# 데이터프레임 생성
db = df(data={'Product': product_list, 'Sale': sale_list, 'Price': price_list})

# csv 변환
db.to_csv(csv_name + ".csv", mode="w", header=False, index=False, encoding='utf-7')

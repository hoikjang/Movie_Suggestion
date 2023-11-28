##############################################################################################################
### 데이터 적재 및 IMPORT 패키지
##############################################################################################################

import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine

##############################################################################################################
### 모델링용 패키지 IMPORT
##############################################################################################################
import numpy as np
import sklearn 
from sklearn.model_selection import train_test_split 
import sklearn.ensemble  as rf
import lightgbm as lgbm
import xgboost  as xgb
import re
import copy
import pytz
import pickle
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO

KST = pytz.timezone('Asia/Seoul')


########################################################################################################################
### DB 연결
########################################################################################################################
# 일반연결
conn          = sqlite3.connect("pine.db", isolation_level=None)
cur           = conn.cursor()

# SQLAlchemy 연결
engine        = create_engine('sqlite:///pine.db')
conn2         = engine.connect()

########################################################################################################################
### 필요 객체 생성
########################################################################################################################

baseYM        = os.environ['baseYM']
gnr           = os.environ['gnr']
phase         = os.environ['phase']

# baseYM        = '201206'
# gnr           = '범죄'

dst_tm        = datetime.now(KST)
baseYm_bfr_1y = datetime.strftime(datetime.strptime(baseYM, '%Y%m') - relativedelta(months = 11), '%Y%m')


print(f'''[LOG] 전처리 코드 실행, 기준년월 = {baseYM}, 장르:{gnr}''')

########################################################################################################################
### 분석마트 생성
########################################################################################################################
dst_tm        = datetime.now(KST)

print(f'''[LOG] 분석마트 적재 시작, 기준년월 = {baseYM}, 시작시간 = {datetime.strftime(dst_tm, '%Y%m%d %H:%M:%S')}''')
##############################################################################################################
#### 학습용 분석마트 생성
##############################################################################################################
####################################################################################################
#### 1차 분석마트 생성
####################################################################################################
# sql_anlys_mart = f'''
#     SELECT
#         DISTINCT
#         A.기준년월
#        ,A.회원번호                                                                                                 
#        ,A.장르명
#        ,A.샘플구분
#        ,A.Y
#        ,B.성별
#        ,B.나이
#        ,B.나이범주
#        ,B.학력
#        ,B.직업군
#        ,B.고객군
#        ,B.통근거리
#        ,B.결혼여부
#        ,B.애완동물
#        ,B.가족구성원수
#        ,B.가족구성원수범주
#        ,B.대륙코드
#        ,B.국가명
#        ,B.주명
#        ,B.모기지액수
#        ,B.모기지액수범주
#        ,B.소유모기지수
#        ,B.소유차량수
#        ,B.소유차량수범주
#        ,B.계좌잔액
#        ,B.계좌잔액범주
#        ,B.전임근무
#        ,B.연봉
#        ,B.연봉범주
#        ,B.연봉구간
#        ,B.자가소유형태
#        ,B.잔액부족횟수
#        ,B.모기지납입지연횟수
#        ,B.모기지납입지연횟수범주
#        ,B.월별드라마시청여부
#        ,B.월별애니시청여부
#        ,B.월별역사시청여부
#        ,B.월별코미디시청여부
#        ,B.월별액션시청여부
#        ,B.월별범죄시청여부
#        ,B.월별스릴러시청여부
#        ,B.월별다큐시청여부
#        ,B.월별모험시청여부
#        ,B.월별판타지시청여부
#        ,B.월별가족시청여부
#        ,B.월별로맨스시청여부
#        ,B.월별음악시청여부
#        ,B.월별호러시청여부
#        ,B.월별전쟁시청여부
#        ,B.월별서부시청여부
#        ,B.월별미스테리시청여부
#        ,B.월별단편시청여부
#        ,B.월별뮤지컬시청여부
#        ,B.월별스포츠시청여부
#        ,B.월별공상과학시청여부
#        ,B.월별전기시청여부
#        ,B.월별뉴스시청여부
#        ,B.월별평점평균
#        ,B.월별판매금액평균
#        ,B.월별평점총합
#        ,B.월별판매금액총합
#        ,B.월별시청횟수
#        ,B.월별탐색횟수
#        ,B.월별만족횟수
#        ,B.월별불만족횟수
#        ,B.월별시청평균
#        ,B.월별탐색평균
#        ,B.월별만족평균
#        ,B.월별불만족평균
#        ,B.월별시청흥행액평균
#        ,B.월별시청예산액평균
#        ,B.월별시청흥행액총액
#        ,B.월별시청예산액총액
#        ,B.월별애니판매금액총액
#        ,B.월별드라마판매금액총액
#        ,B.월별역사판매금액총액
#        ,B.월별코미디판매금액총액
#        ,B.월별액션판매금액총액
#        ,B.월별범죄판매금액총액
#        ,B.월별스릴러판매금액총액
#        ,B.월별다큐판매금액총액
#        ,B.월별모험판매금액총액
#        ,B.월별판타지판매금액총액
#        ,B.월별가족판매금액총액
#        ,B.월별로맨스판매금액총액
#        ,B.월별음악판매금액총액
#        ,B.월별호러판매금액총액
#        ,B.월별전쟁판매금액총액
#        ,B.월별서부판매금액총액
#        ,B.월별미스테리판매금액총액
#        ,B.월별단편판매금액총액
#        ,B.월별뮤지컬판매금액총액
#        ,B.월별스포츠판매금액총액
#        ,B.월별공상과학판매금액총액
#        ,B.월별전기판매금액총액
#        ,B.월별뉴스판매금액총액
#        ,B.월별애니판매금액평균
#        ,B.월별드라마판매금액평균
#        ,B.월별역사판매금액평균
#        ,B.월별코미디판매금액평균
#        ,B.월별액션판매금액평균
#        ,B.월별범죄판매금액평균
#        ,B.월별스릴러판매금액평균
#        ,B.월별다큐판매금액평균
#        ,B.월별모험판매금액평균
#        ,B.월별판타지판매금액평균
#        ,B.월별가족판매금액평균
#        ,B.월별로맨스판매금액평균
#        ,B.월별음악판매금액평균
#        ,B.월별호러판매금액평균
#        ,B.월별전쟁판매금액평균
#        ,B.월별서부판매금액평균
#        ,B.월별미스테리판매금액평균
#        ,B.월별단편판매금액평균
#        ,B.월별뮤지컬판매금액평균
#        ,B.월별스포츠판매금액평균
#        ,B.월별공상과학판매금액평균
#        ,B.월별전기판매금액평균
#        ,B.월별뉴스판매금액평균
#        ,B.월별애니시청횟수
#        ,B.월별애니탐색횟수
#        ,B.월별드라마시청횟수
#        ,B.월별드라마탐색횟수
#        ,B.월별역사시청횟수
#        ,B.월별역사탐색횟수
#        ,B.월별코미디시청횟수
#        ,B.월별코미디탐색횟수
#        ,B.월별액션시청횟수
#        ,B.월별액션탐색횟수
#        ,B.월별범죄시청횟수
#        ,B.월별범죄탐색횟수
#        ,B.월별스릴러시청횟수
#        ,B.월별스릴러탐색횟수
#        ,B.월별다큐시청횟수
#        ,B.월별다큐탐색횟수
#        ,B.월별모험시청횟수
#        ,B.월별모험탐색횟수
#        ,B.월별판타지시청횟수
#        ,B.월별판타지탐색횟수
#        ,B.월별가족시청횟수
#        ,B.월별가족탐색횟수
#        ,B.월별로맨스시청횟수
#        ,B.월별로맨스탐색횟수
#        ,B.월별음악시청횟수
#        ,B.월별음악탐색횟수
#        ,B.월별호러시청횟수
#        ,B.월별호러탐색횟수
#        ,B.월별전쟁시청횟수
#        ,B.월별전쟁탐색횟수
#        ,B.월별서부시청횟수
#        ,B.월별서부탐색횟수
#        ,B.월별미스테리시청횟수
#        ,B.월별미스테리탐색횟수
#        ,B.월별단편시청횟수
#        ,B.월별단편탐색횟수
#        ,B.월별뮤지컬시청횟수
#        ,B.월별뮤지컬탐색횟수
#        ,B.월별스포츠시청횟수
#        ,B.월별스포츠탐색횟수
#        ,B.월별공상과학시청횟수
#        ,B.월별공상과학탐색횟수
#        ,B.월별전기시청횟수
#        ,B.월별전기탐색횟수
#        ,B.월별뉴스시청횟수
#        ,B.월별뉴스탐색횟수
#        ,B.월별애니추천횟수
#        ,B.월별애니만족횟수
#        ,B.월별드라마추천횟수
#        ,B.월별드라마만족횟수
#        ,B.월별역사추천횟수
#        ,B.월별역사만족횟수
#        ,B.월별코미디추천횟수
#        ,B.월별코미디만족횟수
#        ,B.월별액션추천횟수
#        ,B.월별액션만족횟수
#        ,B.월별범죄추천횟수
#        ,B.월별범죄만족횟수
#        ,B.월별스릴러추천횟수
#        ,B.월별스릴러만족횟수
#        ,B.월별다큐추천횟수
#        ,B.월별다큐만족횟수
#        ,B.월별모험추천횟수
#        ,B.월별모험만족횟수
#        ,B.월별판타지추천횟수
#        ,B.월별판타지만족횟수
#        ,B.월별가족추천횟수
#        ,B.월별가족만족횟수
#        ,B.월별로맨스추천횟수
#        ,B.월별로맨스만족횟수
#        ,B.월별음악추천횟수
#        ,B.월별음악만족횟수
#        ,B.월별호러추천횟수
#        ,B.월별호러만족횟수
#        ,B.월별전쟁추천횟수
#        ,B.월별전쟁만족횟수
#        ,B.월별서부추천횟수
#        ,B.월별서부만족횟수
#        ,B.월별미스테리추천횟수
#        ,B.월별미스테리만족횟수
#        ,B.월별단편추천횟수
#        ,B.월별단편만족횟수
#        ,B.월별뮤지컬추천횟수
#        ,B.월별뮤지컬만족횟수
#        ,B.월별스포츠추천횟수
#        ,B.월별스포츠만족횟수
#        ,B.월별공상과학추천횟수
#        ,B.월별공상과학만족횟수
#        ,B.월별전기추천횟수
#        ,B.월별전기만족횟수
#        ,B.월별뉴스추천횟수
#        ,B.월별뉴스만족횟수
#        ,B.월별애니불만족횟수
#        ,B.월별드라마불만족횟수
#        ,B.월별역사불만족횟수
#        ,B.월별코미디불만족횟수
#        ,B.월별액션불만족횟수
#        ,B.월별범죄불만족횟수
#        ,B.월별스릴러불만족횟수
#        ,B.월별다큐불만족횟수
#        ,B.월별모험불만족횟수
#        ,B.월별판타지불만족횟수
#        ,B.월별가족불만족횟수
#        ,B.월별로맨스불만족횟수
#        ,B.월별음악불만족횟수
#        ,B.월별호러불만족횟수
#        ,B.월별전쟁불만족횟수
#        ,B.월별서부불만족횟수
#        ,B.월별미스테리불만족횟수
#        ,B.월별단편불만족횟수
#        ,B.월별뮤지컬불만족횟수
#        ,B.월별스포츠불만족횟수
#        ,B.월별공상과학불만족횟수
#        ,B.월별전기불만족횟수
#        ,B.월별뉴스불만족횟수
#        ,B.월별흥행0등급시청횟수
#        ,B.월별흥행1등급시청횟수
#        ,B.월별흥행2등급시청횟수
#        ,B.월별흥행3등급시청횟수
#        ,B.월별흥행4등급시청횟수
#        ,B.월별예산0등급시청횟수
#        ,B.월별예산1등급시청횟수
#        ,B.월별예산2등급시청횟수
#        ,B.월별예산3등급시청횟수
#        ,B.월별예산4등급시청횟수
#        ,B.월별1950이전시청횟수
#        ,B.월별1965이전시청횟수
#        ,B.월별1980이전시청횟수
#        ,B.월별1999이전시청횟수
#        ,B.월별2010이전시청횟수
#        ,B.월별2010이후시청횟수
#     FROM TRGTMART_SUB                                                                                                AS A
#     LEFT JOIN FTRMART                                                                                                AS B
#         ON A.기준년월 = B.기준년월 AND A.회원번호 = B.회원번호  
#     WHERE 장르명 = '{gnr}'
#       AND A.기준년월 <= '{baseYM}'
# '''


####################################################################################################
###### 2차 분석마트 생성
####################################################################################################
sql_anlys_mart2 = f'''
    SELECT
        DISTINCT
        A.기준년월
       ,A.회원번호                                                                                                 
       ,A.장르명
       ,A.샘플구분
       ,A.Y
       ,B.나이
       ,B.통근거리
       ,B.모기지액수
       ,B.계좌잔액
       ,B.연봉
       ,B.월별드라마탐색횟수
       ,B.월별스릴러불만족횟수
       ,B.월별드라마불만족횟수
       ,B.월별시청횟수
       ,B.월별탐색횟수
       ,B.월별불만족횟수
       ,B.월별공상과학불만족횟수
       ,B.월별판매금액총합
       ,B.월별드라마추천횟수
       ,B.월별스릴러탐색횟수
       ,B.월별액션불만족횟수
       ,B.월별범죄불만족횟수
       ,B.월별2010이전시청횟수
       ,B.월별드라마시청횟수
       ,B.월별예산3등급시청횟수
       ,B.월별액션탐색횟수
       ,B.월별판타지불만족횟수
       ,B.월별흥행4등급시청횟수
       ,B.월별범죄탐색횟수
       ,B.월별평점총합
       ,B.월별전쟁탐색횟수
       ,B.월별시청예산액총액
       ,B.월별공상과학탐색횟수
       ,B.월별코미디탐색횟수
       ,B.월별스릴러판매금액평균
       ,B.월별범죄추천횟수
       ,B.월별코미디불만족횟수
       ,B.월별호러불만족횟수
       ,B.월별판타지탐색횟수
       ,B.월별만족횟수
       ,B.월별시청흥행액총액
       ,B.월별예산2등급시청횟수
       ,B.월별모험불만족횟수
       ,B.월별모험탐색횟수
       ,B.월별전쟁불만족횟수
       ,B.월별드라마판매금액총액
       ,B.월별스릴러추천횟수
       ,B.월별스릴러시청횟수
       ,B.월별액션판매금액평균
       ,B.월별전쟁추천횟수
       ,B.월별1999이전시청횟수
       ,B.월별범죄시청횟수
       ,B.월별단편불만족횟수
       ,B.월별스릴러시청여부
       ,B.월별액션판매금액총액
       ,B.월별액션시청여부
       ,B.월별호러탐색횟수
       ,B.월별범죄시청여부
       ,B.월별공상과학시청여부
       ,B.월별흥행3등급시청횟수
       ,B.월별만족평균
       ,B.월별판매금액평균
       ,B.월별공상과학판매금액평균
       ,B.월별스릴러판매금액총액
       ,B.월별범죄판매금액평균
       ,B.월별코미디시청횟수
       ,B.월별액션시청횟수
       ,B.월별시청평균
       ,B.월별역사불만족횟수
       ,B.월별액션추천횟수
       ,B.월별모험추천횟수
       ,B.월별판타지추천횟수
       ,B.월별공상과학판매금액총액
       ,B.월별모험시청횟수
       ,B.월별애니탐색횟수
       ,B.월별호러판매금액평균
       ,B.월별전쟁시청횟수
       ,B.월별탐색평균
       ,B.월별시청흥행액평균
       ,B.월별전기추천횟수
       ,B.월별시청예산액평균
       ,B.월별전쟁시청여부
       ,B.월별불만족평균
       ,B.월별드라마판매금액평균
       ,B.월별코미디판매금액평균
       ,B.월별평점평균
       ,B.월별모험판매금액평균
       ,B.월별전기불만족횟수
       ,B.월별판타지판매금액평균
       ,B.월별로맨스탐색횟수
       ,B.월별코미디판매금액총액
       ,B.월별전쟁판매금액평균
       ,B.월별단편추천횟수
       ,B.월별가족불만족횟수
       ,B.월별로맨스불만족횟수
       ,B.월별가족판매금액평균
       ,B.월별코미디추천횟수
       ,B.월별가족탐색횟수
       ,B.월별애니불만족횟수
    FROM TRGTMART_SUB                                                                                                AS A
    LEFT JOIN FTRMART                                                                                                AS B
        ON A.기준년월 = B.기준년월 AND A.회원번호 = B.회원번호  
    WHERE 장르명 = '{gnr}'
        AND A.기준년월 <= '{baseYM}'
'''

##############################################################################################################
### 예측용 인풋마트 생성
##############################################################################################################

sql_anlys_mart1 = f'''
    SELECT
        DISTINCT
        기준년월
       ,회원번호                                                                                                 
       ,나이
       ,통근거리
       ,모기지액수
       ,계좌잔액
       ,연봉
       ,월별드라마탐색횟수
       ,월별스릴러불만족횟수
       ,월별드라마불만족횟수
       ,월별시청횟수
       ,월별탐색횟수
       ,월별불만족횟수
       ,월별공상과학불만족횟수
       ,월별판매금액총합
       ,월별드라마추천횟수
       ,월별스릴러탐색횟수
       ,월별액션불만족횟수
       ,월별범죄불만족횟수
       ,월별2010이전시청횟수
       ,월별드라마시청횟수
       ,월별예산3등급시청횟수
       ,월별액션탐색횟수
       ,월별판타지불만족횟수
       ,월별흥행4등급시청횟수
       ,월별범죄탐색횟수
       ,월별평점총합
       ,월별전쟁탐색횟수
       ,월별시청예산액총액
       ,월별공상과학탐색횟수
       ,월별코미디탐색횟수
       ,월별스릴러판매금액평균
       ,월별범죄추천횟수
       ,월별코미디불만족횟수
       ,월별호러불만족횟수
       ,월별판타지탐색횟수
       ,월별만족횟수
       ,월별시청흥행액총액
       ,월별예산2등급시청횟수
       ,월별모험불만족횟수
       ,월별모험탐색횟수
       ,월별전쟁불만족횟수
       ,월별드라마판매금액총액
       ,월별스릴러추천횟수
       ,월별스릴러시청횟수
       ,월별액션판매금액평균
       ,월별전쟁추천횟수
       ,월별1999이전시청횟수
       ,월별범죄시청횟수
       ,월별단편불만족횟수
       ,월별스릴러시청여부
       ,월별액션판매금액총액
       ,월별액션시청여부
       ,월별호러탐색횟수
       ,월별범죄시청여부
       ,월별공상과학시청여부
       ,월별흥행3등급시청횟수
       ,월별만족평균
       ,월별판매금액평균
       ,월별공상과학판매금액평균
       ,월별스릴러판매금액총액
       ,월별범죄판매금액평균
       ,월별코미디시청횟수
       ,월별액션시청횟수
       ,월별시청평균
       ,월별역사불만족횟수
       ,월별액션추천횟수
       ,월별모험추천횟수
       ,월별판타지추천횟수
       ,월별공상과학판매금액총액
       ,월별모험시청횟수
       ,월별애니탐색횟수
       ,월별호러판매금액평균
       ,월별전쟁시청횟수
       ,월별탐색평균
       ,월별시청흥행액평균
       ,월별전기추천횟수
       ,월별시청예산액평균
       ,월별전쟁시청여부
       ,월별불만족평균
       ,월별드라마판매금액평균
       ,월별코미디판매금액평균
       ,월별평점평균
       ,월별모험판매금액평균
       ,월별전기불만족횟수
       ,월별판타지판매금액평균
       ,월별로맨스탐색횟수
       ,월별코미디판매금액총액
       ,월별전쟁판매금액평균
       ,월별단편추천횟수
       ,월별가족불만족횟수
       ,월별로맨스불만족횟수
       ,월별가족판매금액평균
       ,월별코미디추천횟수
       ,월별가족탐색횟수
       ,월별애니불만족횟수
    FROM FTRMART
    WHERE 기준년월 BETWEEN '{baseYm_bfr_1y}' AND '{baseYM}'
'''

##############################################################################################################
### 파생변수 생성
##############################################################################################################
if   phase == '학습':
    df_anlys_mart                    = pd.read_sql(sql_anlys_mart2,conn)
    df_anlys_mart_sub                = df_anlys_mart.drop(columns = ['기준년월','나이','장르명','Y','샘플구분','통근거리','모기지액수','계좌잔액','연봉'])
    

elif phase == '운영':
    df_anlys_mart                    = pd.read_sql(sql_anlys_mart1,conn)
    df_anlys_mart_sub                = df_anlys_mart.drop(columns = ['기준년월','나이','통근거리','모기지액수','계좌잔액','연봉'])


df_anlys_mart_sub                    = df_anlys_mart_sub.astype(float)
df_anlys_mart_sub_sum                = df_anlys_mart_sub.groupby('회원번호').sum().reset_index()
df_anlys_mart_sub_sum.columns        = ['회원번호']+['총합' + str(col_name) for col_name in df_anlys_mart_sub_sum.columns[1:]]
df_anlys_mart_sub_avg                = df_anlys_mart_sub.groupby('회원번호').mean().reset_index()
df_anlys_mart_sub_avg.columns        = ['회원번호']+['평균' + str(col_name) for col_name in df_anlys_mart_sub_avg.columns[1:]]
df_anlys_mart['회원번호']            = df_anlys_mart['회원번호'].astype('float')
df_anlys_mart2                       = pd.merge(df_anlys_mart,df_anlys_mart_sub_sum)
df_anlys_mart3                       = pd.merge(df_anlys_mart2,df_anlys_mart_sub_avg)

dend_tm = datetime.now(KST)
del_tm  = dend_tm-dst_tm

print(f'''[LOG] 분석마트 적재 완료, 기준년월 = {baseYM}, 완료시간 = {datetime.strftime(dend_tm, '%Y%m%d %H:%M:%S')}, 소요시간 = {del_tm}, 행수 = {len(df_anlys_mart3)}, 컬럼 수 = {len(df_anlys_mart3.columns)}''')
########################################################################################################################
### 결측 처리 및 데이터 적재
########################################################################################################################
dst_tm                 = datetime.now(KST)
print(f'''[LOG] 분석마트 전처리 및 인풋마트 적재 시작, 기준년월 = {baseYM}, 시작시간 = {datetime.strftime(dst_tm, '%Y%m%d %H:%M:%S')}''')

if   phase == '학습':
    df_anlys_mart3     = df_anlys_mart3.fillna(0)
    input_mart         = df_anlys_mart3
    
elif phase == '예측':
    df_anlys_mart3     = df_anlys_mart3.fillna(0)
    input_mart         = df_anlys_mart3.loc[df_anlys_mart3['기준년월']==f'{baseYM}'].reset_index().drop(columns='index')



########################################################################################################################
###### 2차 3차 분석마트 리스트
########################################################################################################################
# list_col_cat = ['']


########################################################################################################################
###### 범주형 컬럼 원핫인코딩
########################################################################################################################

# df_anlys_mart_cat = df_anlys_mart[list_col_cat]
# df_anlys_mart_cat = df_anlys_mart_cat.applymap(str)
# df_ohe_tot          = pd.DataFrame()
# oneHotEncdr       = OneHotEncoder(sparse=False, drop = 'first', handle_unknown = 'ignore').fit(df_anlys_mart_cat)
## 원핫인코딩 적용
# tmp_cat           = pd.DataFrame(oneHotEncdr.transform(df_anlys_mart_cat), columns=[[x.replace(" ", "") for x in oneHotEncdr.get_feature_names_out(df_anlys_mart_cat.columns.to_list())]])
# tmp_cat.columns   = [f"{x[0]}" for x in tmp_cat.columns]
# input_mart          = pd.concat([df_anlys_mart.drop(columns = list_col_cat),tmp_cat], axis = 1)
# print(input_mart)




########################################################################################################################
###### 마트 적재
########################################################################################################################

filename      = f'{gnr}_input_mart.sav'
pickle.dump(input_mart, open(filename, 'wb'))
dend_tm = datetime.now(KST)
del_tm  = dend_tm-dst_tm
print(f'''[LOG] 분석마트 전처리 및 인풋마트 적재 완료, 기준년월 = {baseYM}, 완료시간 = {datetime.strftime(dend_tm, '%Y%m%d %H:%M:%S')}, 소요시간 = {del_tm}, 행수 = {len(input_mart)}, 컬럼 수 = {len(input_mart.columns)}''')
print(f'''[LOG] 전처리 코드 실행 완료, 기준년월 = {baseYM}, 장르:{gnr}''')

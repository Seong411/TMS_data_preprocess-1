#TMS_data_preprocess

웨어러블 기기(zepher, E4 empatica)에서 얻는 생체신호를 기반으로 스트레스의 유무를 확인하고자 함


#[Label Format]
- 분노: A
- 공포: F
- 슬픔: S
- 스트레스 아님: X

#The final order of csv files
- Label, EDA, HR, IBI, RR, TEMP, ....

#Program to create
- 라벨링
- 데이터 csv파일 read, write
- ?

#csv file handling program design
1. Hz 맞추기 (일단 64로...?)
 - EDA: 4Hz
 - HR: 1Hz
 - IBI: Hz 단위가 아님. Time Stamp = 첫 column + initial time(처음 시작 시간)
 - TEMP: 4Hz

2. 파일 합치기

3. 쓰레기값 지우는 것
- HR 60미만 지우기
- blank 지우기
- zephyr 정확도 ??% 미만 지우기
- 그 외 noise 처리 (지울거? 평탄화? 평탄화 한다면 평균,최대,최소,처음,끝,중간?)

4. feature 추가하기 (이건 다른파일로?)


TMS_data_preprocess

#라벨링은 각자 자기가 알아서 할 것
[Label Format]
분노: A
공포: F
슬픔: S
스트레스 아님: X

#최종 csv파일 column 순서
Label, EDA, HR, IRI, II, T, ....

#PL은 PYTHON으로

#제작할 program
- 라벨링
- 데이터 csv파일 read, write
- ?

#csv파일 handleing program
1. Hz 맞추기 (일단 64로)

2. 파일 합치기

3. 쓰레기값 지우는 것
- HR 60미만 지우기
- blank 지우기
- zephyr 정확도 ??% 미만 지우기
- 그 외 noise 처리 (지울거? 평탄화? 평탄화 한다면 평균,최대,최소,처음,끝,중간?)

4. feature 추가하기 (이건 다른파일로?)


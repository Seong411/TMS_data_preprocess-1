#어떻게 돌아가나 궁금해서 공부하면서 대충 만든거..

import csv

class FileHandling:
    #RESULT.csv 만들 때 첫 row에 넣을 거 순서
    columns = ['Label', 'EDA', 'HR', 'IBI', 'RR', 'TEMP']

    def __init__(self):
        pass

    #TODO: self.columns를 쓸게 아니라 직접 매개변수로 전달받는 것도 방법. 파일 이름을 'column'.csv 형식으로 하면 문제 없음
    def make_file(self):
        #TODO: Label.csv 만들어지면 바로 밑의 for (tar.close 까지 포함) 복원시키고 그 밑 att='HR' 지울 것
        '''for att in self.columns:'''
        att = 'HR'
        #TODO: 파일 open할 때 디렉토리부터 변수로 열어야 함. 158... 이렇게 표현되는 시간, 기기명 붙여서 넣자
        tar = open('../Data/1583990996_A01A06/RESULT.csv','w')
        target = cvs.writer(tar)

        read_t = open('../Data/1583990996_A01A06/RESULT.csv', 'r')
        rt = read_t.readlines()

        file = open('../Data/1583990996_A01A06/' + att + '.csv', 'r')
        f = file.readlines()

        #tt: 처음 시작 time stamp, t: 다음으로 넘어갔을 때 time stamp.
        #TODO: 변수 이름 바꾸자..
        t = f[0][:-1].split(', ')
        tt = t

        for line, i in f, range(0, len(f)):
            if i == 1:
                #attributes to first row
                #TODO: '기존 row' + '추가되는 attribute' 이런 형식으로 바꿔야 함
                target.writerow(rt[0].split(', ')[0] + [att])
            elif i == 2:
                continue
            else:
                #TODO: [t] 이부분도 rt[i-1].split(', ')[0] 이렇게 바꾸던가 하자. 그럼 처음 입력 때는 어카지?
                target.writerow(rt[i-1].split(', ')[0] + line[:-1].split(', '))

            #TODO: Hz에 따라서 바꿔줘야 함. 지금은 HR이라서 1초씩 더했음
            t += 1

        file.close()
        read_t.close()
        tar.close()

#뭘 해야할까

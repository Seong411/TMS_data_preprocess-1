'''
zephyr의 데이터 파일의 이름을 Empatica의 데이터 파일 이름 양식으로 바꿔줌
1. zephyr 데이터 파일을 empatica 데이터 파일이 있는 곳으로 옮겨준 뒤
2. file_naming을 실행시킨다(path = 데이터 파일이 위치한 폴더명)

끝
'''
import os
import glob

def File_C(path, filenames):
    for i in filenames:
        i = i[len(path):]
        new = i
        for k in range(len(new)):
            if new[k] == '.':
                new = new[:k].upper()+new[k:]
        if new.count('_') > 0:
            for k in range(len(new)):
                if new[k].isalpha():
                    new = new[k:]
                    break

        os.rename(r'%s' % (path + i), r'%s' % (path + new))
    return

def file_naming(path):
    file_list = glob.glob(path+'\\*')
    File_C(path+'\\', file_list)

def Change_All_Datafiles_Name():
    dir = os.path.dirname(os.path.abspath(__file__))
    file_list = glob.glob(dir+'\\Data\\*')
    for i in file_list:
        if i.count('.') > 0:
            continue
        else:
            file_naming(i)
from random import *
import csv

f = open('c:\\data_setting\\data.csv', 'w')  # 주차장 목록 열기
wr = csv.writer(f)
parked_seat = [11, 21, 31, 41, 51, 61, 71, 81, 91, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 자동차 주차자리


def rand(n):  # scv파일에 랜덤데이터 저장하는 함수
    for i in range(n):
        time = randint(0, 11)
    if (time < 10):
        time = "0" + str(time)
    time_min = randint(0, 59)
    if (time_min < 10):
        time_min = "0" + str(time_min)
    time_sec = randint(0, 59)
    if (time_sec < 10):
        time_sec = "0" + str(time_sec)
    carnumber = str(randint(1111, 9999))
    temp = randint(0, 18)
    parkseat = str(parked_seat[temp])
    wr.writerow([("%s:%s:%s" % (time, time_min, time_sec)), carnumber, parkseat])


temp_num = 7  # 자동차 갯수
rand(temp_num)  # 위에 함수에 자동차 갯수 대입
f.close()
f = open('c:\\data_setting\\data.csv', 'r')  # 읽기용으로 다시 열기
data = [0 for i in range(temp_num)]
csv_r = csv.reader(f)
cnt = 0
cnt_s = 0
for line in csv_r:  # line의 데이터를 data배열에 넣어줌
    if cnt == 0 or cnt % 2 == 0:
        data[cnt_s] = line
    cnt_s += 1
    else:
    pass
    cnt += 1
data_array = [[[0 for col in range(10)] for row in range(10)] for r in range(temp_num)]  # [시간][주차장
가로][주차장 세로]  # 입구:100,자리:11,21,31,41,510,61,71,81,91,0,1,2,3,4,5,6,7,8,9,10
for i in range(0, temp_num):  # data 배열 정리
    data[i][0] = data[i][0][0:2]  # 시간의 분초 삭제
for t in range(0, 3):
    data[i][t] = int(data[i][t])  # int형 변환


def s(a):  # 두자리수 각자리 분리시키는 함수
    return a // 10, a % 10


def making_array(D, num):  # data의 데이터를 data_array에 넣어주는 함수 time은 시간
    x, y = s(D[2] - 1)
    x, y = int(x), int(y)
    data_array[num][x][y] += 1


# (a,b)
def finding_path(num, i_num):  # 경로만들어주는 함수 num:자리숫자(11,21,1,2,8등)
    y1, x1 = 9, 9
    y2, x2 = s(num - 1)
    y2, x2 = int(y2), int(x2)
    if (x2 == 0):  # 옆
        while y2 != y1:
            y1 -= 1
    data_array[i_num][y1][9] += 1
    while x2 != x1:
        x1 -= 1
    data_array[i_num][y2][x1] += 1
    if (y2 == 0):  # 위
        while x2 != x1:
            x1 -= 1
    data_array[i_num][9][x1] += 1
    while y2 != y1:
        y1 -= 1
    data_array[i_num][y1][x2] += 1


for i in range(0, temp_num):  # 함수에 시간대입
    making_array(data[i], i)
for i in range(0, temp_num):
    finding_path(data[i][2], i)
print(data, "\n")
for i in data_array:
    for l in i:
        print(l)
    print("\n")
# 축적
# ----------->
# 1,2,4,7,11,16,20,20,20... 총 20개 데이터
# 7일
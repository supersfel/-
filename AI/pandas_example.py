"""
Pandas
데이터 조작을 용이하게 하기 위해 다차원 배열에 인덱스를 지정한 자료구조를 정의하고 정렬, 변환, 삭제 등을 할 수 있는 메서드를 제공

Series - 1차원 데이터 구조 ( 하나의 Row )
DataFrame - 2차원 데이터 구조 ( 여러개의 시리즈가 모여서 생성 )
"""
import pandas as pd
import seaborn as sns

"""
데이터 프레임 샘플
"""
data = sns.load_dataset('titanic')

print('일반')
print(pd.DataFrame(data))


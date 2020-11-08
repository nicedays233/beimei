### 8.柱状图
import pandas as pd
import matplotlib.pyplot as plt
from ipykernel.pylab.config import InlineBackend
from sklearn.preprocessing import StandardScaler
job1 = pd.read_csv('E:/QQData/741454344/FileRecv/jobs_csv.csv')
job = job1['location'].value_counts()
print(job)
print(job.index)

plt.rcParams['font.sans-serif'] = ['SimHei']
InlineBackend.figure_format = 'svg'

# 输入横坐标和纵坐标
plt.bar(job.index, job)
plt.show()




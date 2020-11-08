import numpy as np
# m = 1
# k = 3
# var = []
import pandas as pd
# for i in range(1, 4):
#     var.append([q for q in range(m, k)])
#     m += 2
#     k += 2
# print(var)
var = np.asarray([i for i in range(1, 7)]).reshape(3, 2)
data = {'state': {'wyw': 'ohio', 'wyw2': 'sss'},
        'year': {'wyw': '2004', 'wyw2': '2003'},
        'pop': {'wyw': 2.4, 'wyw3':  3.2}
       }
frame = pd.DataFrame(data)
print(frame.head())

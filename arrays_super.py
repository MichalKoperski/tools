import numpy as np

arr = np.zeros((4,4))

for i in range(4):
    arr[i,i]=i
print(arr)
print(int(arr[1,1]))
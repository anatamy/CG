import numpy as np
#--------------------- A(make 1d array  M [2,3,4.......26]) and print M
M = np.arange(2,27)
print(M)
#--------------------- B(reshape 1d array M to 2D array) and print M

M=M.reshape(5,5)
print(M)
#--------------------- C(change the values of first column of M to 0)
M[:,0]=0
print(M)
#--------------------- D(assign M^2 to M and print it)
M=M@M
print(M)
#-------------------- E get magintude of first row of M
magintude=0
for column in range(5):
    magintude+=M[0][column]**2
magintude=np.sqrt(magintude)
print (magintude)

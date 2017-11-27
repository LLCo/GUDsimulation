# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def getNDVITimeSeris(a,b,c,d,time):
    expValue = np.exp(a + b*time)
    timeseris = c/(1 + expValue) + d
    return(timeseris)

def getMatrixGUD(timeSeris):
    shape = np.shape(timeSeris)
    minusShape = list(shape)
    minusShape[-1] = minusShape[-1] - 1
    derivative = np.zeros(minusShape)
    #print(timeSeris)
    derivative = timeSeris[1:] - timeSeris[:-1]
    #print(derivative)
    derivative2 = derivative[1:] - derivative[:-1]
    derivative3 = derivative2[1:] - derivative2[:-1]
    GUD = getFirstMaxValue(derivative3)
    #return(GUD,derivative2,derivative,derivative3)
    #return(float(GUD) / ((shape[0] - 3)/shape[0]))
    return(GUD)

def getMixNDVI(timeSerisA, timeSerisB):
    fm = np.arange(0, 1.01, 0.1)
    mixNDVI = np.zeros([len(fm),len(timeSerisA)])
    for index,val in enumerate(fm):
        mixNDVI[index,:] =  val * timeSerisA\
            + (1 - val) * timeSerisB
    return(mixNDVI)
    
def getFirstMaxValue(line):
    valTemp = -1000
    for index,val in enumerate(line):
        if(val < valTemp):
            plt.figure()
            plt.plot(range(362),line)
            plt.axvline(index)
            return(index)
        else: valTemp = val

    print('error')
    return(-1)
    
'''

不变量为：
A:
    a:10
    b:-007
    d:0.1
B:
    a:12.1
    b:-007
    c:0.7
    d:0.1

(A，B地物有30天的返青期隔)
(返青期到成熟期所需要的时间不变)
(B地物NDVI的最大值变化)
(A,B地物NDVI的最小值不变)


变量为：
Fm:
    反应的是A，B两种地物类型混合程度对GUD的影像
c:
    最大值变化范围为：c_range = np.arange(0.3,0.81,0.1)
'''
'''
time = 365
timeX = np.arange(0,time,1)
a_A=10
a_B=12.1
b=-0.07
c = 0.7
d=0.1
a_range = np.arange(8.6,10.01,0.1)
b_range = np.arange(10,12.11,0.1)
Fm = np.arange(0,1.01,0.1)

serisB = getNDVITimeSeris(a_B,b,c,d,timeX)
serisAList = np.zeros([len(a_range),time])
for index,val in enumerate(a_range):
    serisAList[index,:] = getNDVITimeSeris(val,b,c,d,timeX)

plt.figure(figsize = (10,6))
plt.plot(timeX,serisB,'g',label= 'serisB')
for index,val in enumerate(a_range):
    plt.plot(timeX,serisAList[index,:],'r--',\
             label= 'serisA GUD a = ' + str(val),\
             color = (1,1 - index/(len(a_range)),0))
plt.grid()
plt.legend()
plt.show()


GUDserisB = getMatrixGUD(serisB)
minusMatrix = np.zeros([len(Fm),len(a_range)])
for indexi,vali in enumerate(Fm):
    for indexj,valj in enumerate(a_range):
        mixSeris = vali * serisB + (1 - vali)*serisAList[indexj,:]
        GUDmix = getMatrixGUD(mixSeris)
        minusMatrix[indexi,indexj] = GUDmix
        
plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(minusMatrix)
#print(im)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
ax.set_xlabel('GUD A\'s Shift');
ax.set_ylabel('Fa');
ax.set_xticks(range(len(a_range)))
ax.set_yticks(range(11))
ax.set_xticklabels(list(map(str,a_range)))
label = ['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
label.reverse()
ax.set_yticklabels(label)
plt.title('mix GUD')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.show()
print(minusMatrix) 
print(minusMatrix.mean(axis = 1))
print()

plt.figure(figsize = (6,6))
temp = minusMatrix.mean(axis = 0)
plt.plot(range(len(a_range)),temp,'ro--')
ax = plt.gca()
ax.set_ylabel('mix GUD')
ax.set_xlabel('GUD A\'s Shift');
ax.set_xticks(range(len(a_range)))
ax.set_xticklabels(list(map(str,a_range)))

plt.show()
'''
time = 365
timeX = np.arange(0,time,1)
a_A=10
a_B=12.1
b=-0.07
c = 0.7
d=0.1
a_range = np.arange(12.1,13.51,0.1)
Fm = np.arange(0,1.01,0.1)

serisB = getNDVITimeSeris(a_A,b,c,d,timeX)
serisAList = np.zeros([len(a_range),time])
for index,val in enumerate(a_range):
    serisAList[index,:] = getNDVITimeSeris(val,b,c,d,timeX)

plt.figure(figsize = (10,6))
plt.plot(timeX,serisB,'r',label= 'serisA')
for index,val in enumerate(a_range):
    plt.plot(timeX,serisAList[index,:],'r--',\
             label= 'serisB GUD a = ' + str(val),\
             color = (index/(len(a_range)),1,0))
plt.grid()
plt.legend()
plt.show()


GUDserisB = getMatrixGUD(serisB)
minusMatrix = np.zeros([len(Fm),len(a_range)])
for indexi,vali in enumerate(Fm):
    for indexj,valj in enumerate(a_range):
        mixSeris = vali * serisB + (1 - vali)*serisAList[indexj,:]
        GUDmix = getMatrixGUD(mixSeris)
        minusMatrix[indexi,indexj] = GUDmix
        
plt.figure(figsize = (10,10))
ax = plt.gca()
im = ax.imshow(minusMatrix)
#print(im)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
ax.set_xlabel('GUD A\'s Shift');
ax.set_ylabel('Fb');
ax.set_xticks(range(len(a_range)))
ax.set_yticks(range(11))
ax.set_xticklabels(list(map(str,a_range)))
label = ['0%','10%','20%','30%','40%','50%','60%','70%','80%','90%','100%']
label.reverse()
ax.set_yticklabels(label)
plt.title('mix GUD')
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.show()
print(minusMatrix) 
print(minusMatrix.mean(axis = 1))
print()

plt.figure(figsize = (6,6))
temp = minusMatrix.mean(axis = 0)
plt.plot(range(len(a_range)),temp,'ro--')
ax = plt.gca()
ax.set_ylabel('mix GUD')
ax.set_xlabel('GUD B\'s Shift');
ax.set_xticks(range(len(a_range)))
ax.set_xticklabels(list(map(str,a_range)))

plt.show()

        


import numpy as np
import matplotlib.pyplot as py

def CDF2(x):
    u = np.unique(x)
    y = x.searchsorted(u,sorter=np.argsort(x))
    return u,np.concatenate((y[1:],[x.size]))/x.size



def CDF1(inputlist):
    sort_list = np.sort(inputlist,axis=None)

    listlen = len(inputlist)
    p = np.arange (listlen)/(listlen-1)
    return sort_list, p


#list1 = np.random.normal(0,0.1,10000)
#sl, pl = CDF_convert(list1)
#plt.plot(sl,pl)





z = np.random.normal(0,0.1,1000)


def CDF_Genetor(numlist):

    plist = []
    length = len(numlist)

    count =0
    while (count < length):
        value = numlist[count]
        p = 0
        for i in numlist:
            if i<=value:
                p+=1
        probility = p/length
        plist.append(probility)
        count+=1
    i=np.argsort(numlist)
    numlist=numlist[i]
    plist=np.array(plist)[i]
    return numlist,plist
    




















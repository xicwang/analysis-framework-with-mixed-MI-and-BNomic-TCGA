


import os
import numpy as np

'''
meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/GBM/GBM.meth.by_mean.data.txt'
test_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/meth_test.txt'
'''
#the result table contains everything extract from raw data, patient name and methylation values. gene names. 
def meth_extraction(filename):
    complexFile = open(filename)
    linecount = 0
    all_data = []
    for line in complexFile:
        linecount +=1
        if linecount ==1:
            line = line.strip()
            id_list = line.split('\t')
            all_data.append(id_list) 
        if linecount >=3:
            line = line.strip()
            split_list = line.split('\t')
            meth = []    
            for item in split_list:
                if item == 'NA':
                    item = '0'
                if item == 'null':
                    item = '0'
                meth.append(item)
            all_data.append(meth)
    res = np.array(all_data)   
    ''' with repr print, we can print , between each element in the numpy array. '''
    #print(repr(res))

    #p_id = res[0:1]
    p_id = res[0:1,1:]
    remove_index = []
    for index, patient in np.ndenumerate(p_id):
        #index is the tuple, contains (0,1), like row, and column, we need only column.
        #print (index, patient)
        #we can only get the sample code 01 for primary solid tumor, to remove some patient id. 
        #if patient[13:] == '11':
        if patient[13:] != '01':
            #remove_index.append(index[1])
            remove_index.append(index[1]+1)
    #print(remove_index)
    remove = tuple(remove_index)
    res = np.delete(res, remove, 1)
    #sort the row, which is patient id, without the first element of the table (0,0)
    res[0:,1:] = res[0:,1:][:,np.argsort(res[0,1:])]
    #sort the column, which is gene name, without the first element of the table (0,0)
    res[1:]=res[1:][np.argsort(res[1:,0])]

    return res

#G[1:]=G[1:][np.argsort(G[1:,0])]
'''
         'BRCA', 'GBM', 'GBMLGG', 'HNSC', 'KIPAN', 'KIRC', 'LGG', 'LUAD', 'LUSC', 'OV', 'PRAD', 'SKCM', 'STES', 'THCA', 'UCEC'
no. id    885,    285,     685,     580,     867,    480,    530,   492,    412,   612,   549,    475,    599,    567,    478
11 in id: 97,      0,       2,      50,      205,    160,    0,     32,     42,    12,    50,     2,      18,     56,     46
          788     285      683      530      662     320     530    460     370    600    499     473     581     511     432

see mRNA_table for COADREAD numbers
'''
def make_meth_file_link(cancer):
    meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    meth_file += cancer
    meth_file += '/'
    meth_file += cancer
    meth_file += '.meth.by_mean.data.txt'
    return meth_file
    
def check_id_has_11_or_not():
    list = ['BRCA','COADREAD','GBM','GBMLGG','HNSC','KIPAN','KIRC','LGG','LUAD','LUSC','OV','PRAD','SKCM','STES','THCA','UCEC']
    count_list = []
    total_list = []
    alt_list = []
    for item in list:
        print('processing ', item, ' data...')
        file_name = make_meth_file_link(item)
        complexFile = open(file_name)
        linecount = 0
        count = 0
        alt_count = 0
        for line in complexFile:
            linecount +=1
            if linecount ==1:
                line = line.strip()
                id_list = line.split('\t')
                patient = id_list[1:]
                total = len(patient)
                for p in patient:
                    check = p[13:] 
                    if check == '11':
                        #print(item)
                        count+=1
                    if check == '02':
                        alt_count +=1
        count_list.append(count)
        total_list.append(total)
        alt_list.append(alt_count)
    print(list, ':')
    print('total number of patient is: ', total_list)
    print('the number of patients has 11 in id: ', count_list)
    print('the number of patients has 02 in id: ', alt_list)
    print('the valid no. of patient for analysis: ', np.array(total_list)-np.array(count_list))
    return count 

def remove11a():
    
    return 0
        



























import os
import numpy as np

'''
expression_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/mRNA_test.txt'    

dict_keys(['SLC35E2'])
IMPORTANT, FOUND ONE DUPLICATE ID: in PAAD, dict_keys(['SLC35E2']), IN BRCA, there is one duplicate gene too. 


'''
#the result table contains everything extract from raw data, patient name and methylation values. gene names. 
def expression_extraction(filename):
    complexFile = open(filename)
    linecount = 0
    all_data = []
    gene_id_list = []
    for line in complexFile:
        linecount +=1
        if linecount ==1:
            line = line.strip()
            id_list = line.split('\t')
            all_data.append(id_list) 
        if linecount >=2:
            line = line.strip()
            split_list = line.split('\t')
            expression = []
            gene_name = split_list[0]
            if gene_name[0] != '?':
                gene_id  = gene_name.split('|',1)[0]
                '''I found one duplicate gene id in BRCA and PAAD, so need to solve this from the source, need to remove these duplicated gene id, so I added this line of code, if gene id already in the gene id list, then do not add, so I remove one gene id by this line. '''
                if gene_id not in gene_id_list:
                    gene_id_list.append(gene_id)
                    expression.append(gene_id)
                    for item in split_list[1:]:
                        if item == 'NA':
                            item = '0'
                        if item == 'null':
                            item = '0'
                        expression.append(item)
                    all_data.append(expression)
    res = np.array(all_data)   
    ''' with repr print, we can print , between each element in the numpy array. '''
    #print(repr(res))
    #print(res.shape)
    ''' this means get row beginning from the first row 0, to the second row 1, so only one first row will be selected, if change to res[0,], it will select the first row as a whole, and then when iterate the list, it will only give index (0,)(1,)(2,)(3,), I will have to change the remove_index operation too'''
    p_id = res[0:1,1:]
    #print(p_id)
    remove_index = []
    for index, patient in np.ndenumerate(p_id):
        #index is the tuple, contains (0,1), like row, and column, we need only column.
        #print (index, patient)
        # HERE WE MADE THE CHANGE TO ONLY KEEP 01 PATIENTS
        #if patient[13:] == '11':
        if patient[13:] != '01':
            #because I didn't consider the first item in the list, so 'gene' is not in the p_id, when count the index, I need to add 1 to get the right index. 
            remove_index.append(index[1]+1)
    #print(remove_index)
    remove = tuple(remove_index)
    res = np.delete(res, remove, 1)
    #sort the row, which is patient id, without the first element of the table (0,0)
    res[0:,1:] = res[0:,1:][:,np.argsort(res[0,1:])]
    #sort the column, which is gene name, without the first element of the table (0,0)
    res[1:]=res[1:][np.argsort(res[1:,0])]

    return res

'''
mRNA:

'BRCA', 'COADREAD', 'GBM', 'GBMLGG', 'HNSC', 'KIPAN', 'KIRC', 'LGG', 'LUAD', 'LUSC', 'OV', 'PRAD', 'SKCM', 'STES', 'THCA', 'UCEC1212,     677,       171,    701,     566,     1020,    606,    530,   576,    552,   307,   550,    473,   646,     568,    581
 112,       51,       5,      5,       44,      129,     72,     0,     59,     51,    0,     52,     1,     46,     59,     35
 0,         2,         13,     27,      0,       0,       0,     14,     2,     0,     4,     0,      0,     0,       0,     1
1100       626        166     696      522      891      534    530     517     501   307    498     472     600    509     546


methylation:

'BRCA', 'COADREAD','GBM', 'GBMLGG', 'HNSC', 'KIPAN', 'KIRC', 'LGG', 'LUAD', 'LUSC', 'OV', 'PRAD', 'SKCM', 'STES', 'THCA', 'UCEC'
  885,     441      285,    685,     580,     867,    480,     530,   492,    412,   612,   549,   475,    599,     567,   478
  97,       45       0,       2,      50,      205,    160,    0,     32,     42,    12,    50,     2,      18,     56,     46
  0,        2,       0,      27,      0,       0,       0,     14,     2,      0,    18,     0,     0,       0,      0,      1
 788      396      285      683      530      662     320     530    460     370    600    499     473     581     511     432

Mutation:
'BRCA', 'COADREAD', 'GBM', 'GBMLGG', 'HNSC', 'KIPAN', 'KIRC', 'LGG', 'LUAD', 'LUSC', 'OV', 'PRAD', 'SKCM', 'STES', 'THCA', 'UCEC 982,     223,       290,     576,     279,    644,     417,    286,   230,    178,   316,   332,    345,    474,   405,    248
 0,        0,        0,        0,       0,      0,       0,     0,     0,      0,      0,     0,      0,      0,     0,     0
 0,        0,        7,        7,       0,      0,       0,     0,     0,      0,      0,     0,      0,      0,     0,     0
982       223        290      576      279     644      417     286    230     178    316    332     345     474    405     248

total number of patient is
the number of patients has 11 in id:  
the number of patients has 02 in id:  
the valid no. of patient for analysis:  

'''

def make_exp_file_link(cancer):
    exp_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    exp_file += cancer
    exp_file += '/'
    exp_file += cancer
    exp_file += '.uncv2.mRNAseq_RSEM_normalized_log2.txt'
    return exp_file
    
def check_id_has_11_or_not():
    list = ['BRCA','COADREAD','GBM','GBMLGG','HNSC','KIPAN','KIRC','LGG','LUAD','LUSC','OV','PRAD','SKCM','STES','THCA','UCEC']
    count_list = []
    total_list = []
    alt_list = []
    for item in list:
        print('processing ', item, ' data...')
        file_name = make_exp_file_link(item)
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
















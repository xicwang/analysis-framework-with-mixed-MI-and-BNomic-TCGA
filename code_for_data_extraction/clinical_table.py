
import numpy as np

'''
a[0,:] first row, array(['BCR_PATIENT_BARCODE', 'TCGA-CS-6665', 'TCGA-CS-6670'...])

a[1,:] second row, array(['Tumor_Status', 'with tumor', 'with tumor', 'tumor free', 'NA'...])

clinic = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/clinical_test.txt'

'''
def id_status_table_read_rawdata(filename):
    complexFile = open(filename, encoding = "ISO-8859-1")
    linecount = 0
    id_status_table =[]
    for line in complexFile:
        line = line.strip()
        split_list = line.split('\t')        
        target = split_list[0]  
        #we can change to different target to get different variables, 09-08-2018, after talked with Sergio to use three sorted table to integrate all the info. 
        #if target == 'patient.bcr_patient_barcode':
        if target == 'bcr_patient_barcode':    
            #print(len(split_list))
            id = []
            for item in split_list:
                id.append(item.upper())
            # after compare 3 other database, id all has sample code, we remove sample code 02, 06 and others, only keep 01, so we can add 01 to the end of the id, for the further comparison and extraction. 
            t = list(map(( lambda x: x + '-01'), id))
            t[0] = 'PATIENT_barcode'
            #print('patient id number: ', len(id)-1)
            id_status_table.append(t)
        
        #if target == 'patient.person_neoplasm_cancer_status':
        if target == 'person_neoplasm_cancer_status':
            tumor = []
            split_list[0] = 'Tumor_Status'
            for item in split_list:
                tumor.append(item)
            #print('tumor status number: ', len(tumor)-1)
            id_status_table.append(tumor)
    return  np.array(id_status_table)


# after the clinical table, i will convert the word to 0,1, -1, and then remove -1, then sort the patient id. 
def patient_status_convertion(clinical_table):
    
    status = clinical_table[1,:][1:]
    
    tumor = [x == 'with tumor' for x in status]
    free =  [x == 'tumor free' for x in status]
    na =    [x == 'NA' for x in status]
    
    tumor1 = np.array(tumor)
 
    na1 = np.array(na)*-1    
    convert = np.array(tumor1+na1)
    #print(convert)
     
    clinical_table[1,:][1:] = convert 
    # it is a 2 x patient matrix, so just need to check the 2 row, to see if the tumor status is -1.
    remove_index = np.where(clinical_table[1,:] == '-1')[0]
    remove = tuple(remove_index)
    t = np.delete(clinical_table, remove, 1)
    '''
    sort the table with first row, with the first element
    '''
    t[0:,1:] = t[0:,1:][:,np.argsort(t[0,1:])]
    return t


'''
-----------------------------Sergio code IMPORTANT------------------------------------------
it will sort the table use first column without the first element. 
'''
#G[1:]=G[1:][np.argsort(G[1:,0])]

def clinic_main(address):
    a = id_status_table_read_rawdata(address)
    b = patient_status_convertion(a)
    return b

 

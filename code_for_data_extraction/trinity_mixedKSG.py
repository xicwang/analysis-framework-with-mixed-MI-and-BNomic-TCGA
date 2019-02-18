import clinical_table_survival as ct
import meth_table as met
import mutation_table as mut
import mRNA_table as mrt
import numpy as np
import mixed as mixed
from functools import reduce
import address_maker as am
'''
mRNA:

array([['gene', 'TCGA-02-0047-01', 'TCGA-02-0055-01', 'TCGA-02-2483-01',
        'TCGA-02-2486-02', 'TCGA-06-0125-01'],
       ['A2LD1', '5.78325757595018', '6.39255785191704',
        '5.11007922031769', '7.57387815167514', '6.82843356307862'],
       ['AARSD1', '8.3476784994892', '8.75567375704547',
        '9.29309247485167', '8.84854657884448', '8.92131671222251'],
       ['ABR', '12.5801945824145', '11.075729292993', '12.0024662166844',
        '12.1231435417502', '11.8752783447904'],
       ['ACMSD', '0.297837035886644', '0', '0', '0.871291692375117',
        '1.87448223326599'],
       ['ACTG2', '5.02575084746835', '14.3642604474962',
        '7.60136447421491', '7.76608427137458', '7.0219837830867'],
       ['CCND2', '12.8062438727636', '10.2033197361588', '12.648796278865',
        '11.6247620149163', '13.7088351977104']], 
      dtype='<U17')

methylation:

array([['Hybridization REF', 'TCGA-02-0001-01', 'TCGA-02-0007-01',
        'TCGA-02-0009-01'],
       ['A2BP1', '0.0289840260278', '0.559916910779', '0.452217888725'],
       ['AAMP', '0.393222232602', '0.440782024227', '0.468500624608'],
       ['ABAT', '0.0233988020594', '0.0249646780869', '0.0253641208924'],
       ['ACRBP', '0.684274258418', '0.713771266586', '0.630876899037']], 
      dtype='<U17')

mutation:
array([['Gene', 'TCGA-A1-A0SB-01', 'TCGA-A2-A1FZ-01', 'TCGA-A2-A1G0-01'],
       ['ABLIM1', '1', '0', '0'],
       ['ADAMTS20', '1', '0', '0'],
       ['ADAMTS7', '0', '1', '0'],
       ['ANKRD12', '0', '1', '0'],
       ['ARL4A', '0', '0', '1'],
       ['ARMC5', '0', '0', '1'],
       ['BOD1L1', '0', '0', '1'],
       ['CADM2', '0', '0', '0'],
       ['CHTF18', '0', '1', '0'],
       ['DTNB', '1', '1', '0']], 

array([['BCR_PATIENT_BARCODE', 'TCGA-CS-6665', 'TCGA-CS-6670',
        'TCGA-DB-A4XC', 'TCGA-DH-A66B', 'TCGA-DU-A76O', 'TCGA-E1-A7YN',
        'TCGA-FG-8187', 'TCGA-FG-A60K'],
       ['Tumor_Status', '1', '1', '0', '1', '1', '1', '0', '1']], 
      dtype='<U19')

mut_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/gdac.broadinstitute.org_BRCA.Mutation_Packager_Calls.Level_3.2016012800.0.0/'
exp_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/mRNA_test.txt'
meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/meth_test.txt'
clinic_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/clinical_test.txt'


test for real data, i chose PAAD as the test file, because it only contains 185 patient id, it is a small set. let's see how it works.

mut_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/PAAD/gdac.broadinstitute.org_PAAD.Mutation_Packager_Calls.Level_3.2016012800.0.0/'
exp_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/PAAD/PAAD.uncv2.mRNAseq_RSEM_normalized_log2.txt'
meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/PAAD/PAAD.meth.by_mean.data.txt'
clinic_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/PAAD/All_CDEs.txt'

mut_file = '/home/stevewang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/BRCA/gdac.broadinstitute.org_BRCA.Mutation_Packager_Calls.Level_3.2016012800.0.0/'
exp_file = '/home/stevewang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/BRCA/BRCA.uncv2.mRNAseq_RSEM_normalized_log2.txt'
meth_file = '/home/stevewang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/BRCA/BRCA.meth.by_mean.data.txt'
clinic_file = '/home/stevewang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/BRCA/All_CDEs.txt'

'''

def address_maker():
    mut_file = ' '
    exp_file = ''
    meth_file = '' 
    clinic_file = ''
    return mut_file, exp_file, meth_file, clinic_file

def common_table(mut_file, exp_file, meth_file, clinic_file):
    # first column is the gene name, first row is the patient id.  
    mutation = mut.main_for_mutation(mut_file)
    exp = mrt.expression_extraction(exp_file)
    meth = met.meth_extraction(meth_file)
    cli = ct.clinic_main(clinic_file)
   
     
    #print('mutation file contains ', mutation.shape[0]-1, ' genes and contains ', mutation.shape[1]-1, ' patients.') 
    #print('expression file contains ', exp.shape[0]-1, ' genes and contains ', exp.shape[1]-1, ' patients.')
    #print('methylation file contains ', meth.shape[0]-1, ' genes and contains ', meth.shape[1]-1, ' patients.') 
    
    
    #dimension is 1 x patient no.
    mut_patient = mutation[0:1]
    rna_patient = exp[0:1]
    met_patient = meth[0:1]
    cli_patient = cli[0:1]
    #this is needed in the next step:
    #common_patient = reduce(np.intersect1d, (a,b,c))
    ''' GET the common patient id between 4 databases.  this is important, I need this in the next step'''
    common_patient = reduce(np.intersect1d, (mut_patient, rna_patient, met_patient, cli_patient))
    
    mut_gene = mutation[1:,0:1]    
    met_gene = meth[1:,0:1]
    rna_gene = exp[1:,0:1]
    #this is needed in the next step:
    #common_gene = reduce(np.intersect1d, (e,f,g))
    ''' GET the common gene id between 3 databases, we only need 3, because tumor status clinical data doesn't has gene ids, and the order of the common gene is important, needed in the next step. '''
    common_gene = reduce(np.intersect1d, (mut_gene, met_gene, rna_gene))

    common_mutation =  mutation[np.in1d(mutation[:,0], common_gene)]
    common_exp = exp[np.in1d(exp[:,0], common_gene)]
    common_meth = meth[np.in1d(meth[:,0], common_gene)]

    intersect_mut_table = common_mutation[:,np.in1d(mut_patient, common_patient)]
    intersect_mRNA_table = common_exp[:,np.in1d(rna_patient, common_patient)]
    intersect_meth_table = common_meth[:,np.in1d(met_patient, common_patient)]
    
    #adding first row for three tables, patient ids:
    temp_mut = np.vstack((common_patient, intersect_mut_table))
    temp_mRNA = np.vstack((common_patient, intersect_mRNA_table))
    temp_met = np.vstack((common_patient, intersect_meth_table))

    #make the first column of three common table.
    c_gene = list(common_gene)
    g_len = len(c_gene)+1
    c_gene.insert(0, 'Gene')
    c_gene = np.array(c_gene)
    c_gene = c_gene.reshape(g_len,1)

    '''IMPORTANT: final step for making common table for three database: need to return these 3 tables
    
    array([['Gene', 'TCGA-02-0001-01', 'TCGA-02-0007-01', 'TCGA-02-0010-01'],
       ['AAMP', '1', '0', '1'],
       ['ACRBP', '0', '1', '0'],
       ['CCND2', '0', '0', '0']], 
      dtype='<U21')
    '''

    final_mut = np.column_stack((c_gene, temp_mut))
    final_mRNA = np.column_stack((c_gene, temp_mRNA))
    final_met = np.column_stack((c_gene, temp_met))
    
    '''I should return this as final table  
    looks like this:

        array([['TCGA-02-0001-01', 'TCGA-02-0007-01', 'TCGA-02-0010-01'],
       ['0', '1', '0']], 
       
    ''' 
    final_cli = cli[:,np.in1d(cli[0: 1], common_patient)]
    
    b = final_cli[1,:].astype('int')  
    print('final clinical contains ', len(b) , ' patients ', sum(b), 'long term, ', len(b)-sum(b), ' are short term survival.', 'the long term ratio is: ', sum(b)/len(b))
    return final_cli, final_mut, final_mRNA, final_met



# gene_table, and cli_table should be numpy array
def get_MI_between_status_and_each_three_table(cli_table, gene_table):
    
    tumor_status = cli_table[1,].astype(float)
    print(tumor_status.shape)
    gene_list = gene_table[:,0:1]
    MI_list = []
    i = 0
    value_table = gene_table[1:,1:]
    size = np.shape(value_table)
    print(size)
    row = size[0]
    column = size[1]
    # < column maybe wront
    while i < column:
        row_value= value_table[i].astype(float)
        ''' HERE IS THE CHANGE and different from the previous code''' 
        mi_score = mixed.Mixed_KSG(row_value, tumor_status, k=2)
        MI_list.append(mi_score)
        i+=1

        ''' ========================================================='''
    print('Finish MI score.')
    return gene_list, MI_list


def trinity_MI_between_status_and_all_three(final_cli, final_mut, final_mRNA, final_met):
    tumor_status = final_cli[1,].astype(float)
    gene_list = final_mut[:,0:1]
    MI_list = []
    b = final_mut[1:,1:].astype(float)
    c = final_mRNA[1:,1:].astype(float)
    d  = final_met[1:,1:].astype(float)
    x = np.dstack((b,c,d))
    size = np.shape(x)
    print('finish computing final table, combined 3 databases into one, final table dimension is: ', size)
    row = size[0]
    i=0
    while i < row:
        row_value= x[i].astype(float)
        ''' HERE IS THE CHANGE and different from the previous code''' 
        mi_score = mixed.Mixed_KSG(row_value, tumor_status, k=1)
        MI_list.append(mi_score)
        i+=1
    print('mutual information score finished.')
    return  gene_list, MI_list



def Step1_get_MI_list(cancer):
    #mut_file, exp_file, meth_file, clinic_file = am.address_maker(cancer)
    mut_file, exp_file, meth_file, clinic_file = am.test_address_maker()
    final_cli, final_mut, final_mRNA, final_met = common_table(mut_file, exp_file, meth_file, clinic_file)
    gene_list, MI_list = trinity_MI_between_status_and_all_three(final_cli, final_mut, final_mRNA, final_met)
    return gene_list, MI_list

    




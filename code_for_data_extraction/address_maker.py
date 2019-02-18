
def address_maker(cancer):
   
    exp_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    exp_file += cancer
    exp_file += '/'
    exp_file += cancer
    exp_file += '.uncv2.mRNAseq_RSEM_normalized_log2.txt'

    meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    meth_file += cancer
    meth_file += '/'
    meth_file += cancer
    meth_file += '.meth.by_mean.data.txt'

    mut_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    mut_file += cancer
    mut_file += '/'
    mut_file += 'gdac.broadinstitute.org_'
    mut_file += cancer
    mut_file += '.Mutation_Packager_Calls.Level_3.2016012800.0.0/'
   
    clinic_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/'
    clinic_file += cancer
    clinic_file += '/'
    clinic_file += 'All_CDEs.txt'

    return mut_file, exp_file, meth_file, clinic_file



def test_address_maker():
    
    mut_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/gdac.broadinstitute.org_BRCA.Mutation_Packager_Calls.Level_3.2016012800.0.0/'
    exp_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/mRNA_test.txt'
    meth_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/meth_test.txt'
    clinic_file = '/home/xicwang/2nd_pro/BroadInstitute_firehose/Trinity_BNomic/test_file/clinical_test.txt'
    return mut_file, exp_file, meth_file, clinic_file

    








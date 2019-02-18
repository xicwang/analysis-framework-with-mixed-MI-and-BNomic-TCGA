


import trinity_mixedKSG as tm
import PDFtoCDF as pc
import matplotlib.pyplot as plt
import numpy as np
import address_maker as am

''' ----------this short function could replace all the code before!!!!!!! check mRNA document for the older code '''
def updated_select_gene_by_rank(gene_list, MI_list, cut_off):
    MI_list = np.array(MI_list)
    # value = MI_list, but after sort the value in MI_list, index is the matched position in the orignial place, also =  gene list index, so next step I will need to also sort the gene name list to match the MI list. 
    index, value, probability = pc.cdf_genetor_with_index(MI_list)
    a = gene_list[1:][index]
    res =  a[probability >= cut_off]
    return res


def bn_for_tri_files(cancer, cut_off):
    #first I get the gene list with top 99.9% of the mutual information score
    
    mut_file, exp_file, meth_file, clinic_file = am.address_maker(cancer)
    #mut_file, exp_file, meth_file, clinic_file = am.test_address_maker()
    final_cli, final_mut, final_mRNA, final_met = tm.common_table(mut_file, exp_file, meth_file, clinic_file)
    gene_list, MI_list = tm.trinity_MI_between_status_and_all_three(final_cli, final_mut, final_mRNA, final_met)
    
    cut_off_gene_list = updated_select_gene_by_rank(gene_list, MI_list, cut_off)
    

    filtered_mut = final_mut[np.in1d(final_mut[:,0], cut_off_gene_list)]
    filtered_mRNA = final_mRNA[np.in1d(final_mRNA[:,0], cut_off_gene_list)]
    filtered_met = final_met[np.in1d(final_met[:,0], cut_off_gene_list)]
    
    # this name is the same if I use other table, ex. filtered_mRNA, filtered_met. 
    name = filtered_mut[:,0]
    first_column= make_first_column_in_bn(name)

    size = np.shape(filtered_mut)
    row = size[0]
    column = size[1]
    
    first_row = np.zeros(column-1)
    last_row = final_cli[1,:]
    i = 0
    while i < row:
        mut_row = filtered_mut[i,1:]
        mRNA_row = filtered_mRNA[i,1:]
        met_row = filtered_met[i,1:]
        tri_row = np.vstack((mut_row, mRNA_row, met_row))
        first_row = np.vstack((first_row, tri_row))
        i+=1
 
    res = np.vstack((first_row, last_row)) 
    res = np.delete(res, 0,0)
    
    
    bnfile = np.column_stack((first_column, res))
    bnfile = bnfile.T
    print('the file ready for write into bn file, the dimension is: ', np.shape(bnfile))
    return bnfile

def make_first_column_in_bn(gene_list):
    l = len(gene_list)
    i = 0
    new_row = []
    while i<l:
        gene_id = gene_list[i]
        mutation = gene_id + '_S'
        mRNA = gene_id + '_E'
        meth = gene_id + '_M'
        new_row.append(mutation)
        new_row.append(mRNA)
        new_row.append(meth)
        i+=1
    new_row.append('Survival')
    new_row = np.array(new_row)
    return new_row


def write_to_file(writefilename,target_list):
    np.savetxt(writefilename, target_list, delimiter=',', fmt='%s')



def main(cancer, cutoff):
    res = bn_for_tri_files(cancer, cutoff)
    writefilename = 'Tri_data_top_genes_for_'
    writefilename += cancer
    writefilename += '_bn_file_'
    writefilename += str(cutoff)
    writefilename += '.txt'
    write_to_file(writefilename, res)

def if __name__=="__main__":


    cancer = input('Please enter the cancer type: ')
    cutoff = input('What is the cutoff value: ')
    cutoff = float(cutoff)
    main(cancer, cutoff)



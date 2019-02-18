

# /home/xicwang/Rodin_Paper/BNOmics/uthsph-bnomics-78dbc62fbc53/dotfile.dot
#

import numpy as np

def readfile(filename):
    complexFile = open(filename)
    whole_list = []
    for line in complexFile:
        line = line.strip()
        split_list = line.split()
        #print(split_list)
        l = len(split_list)
        pair_list = []
        if l == 7:
            #need to remove first two characters, to only get the ID, for example '"EID2"'
            n1 = split_list[0][1:-1]
            n2 = split_list[2][1:-1]
            pair_list.append(n1)
            pair_list.append(n2)
            pair_list.append(line)
            whole_list.append(pair_list)    
    return whole_list
   

def find_target_parent(target, whole_list):
    parent_list = []
    file_list = []
    for item in whole_list:
        if target == item[1]:
            parent = item[0]
            parent_list.append(parent)
            file_list.append(item[2])
    return parent_list, file_list


def find_target_child(target, whole_list):
    child_list = []
    file_list = []
    for item in whole_list:
        if target == item[0]:
            child = item[1]
            child_list.append(child)
            file_list.append(item[2])
    return child_list, file_list


def find_child_parent(child_list, whole_list, target):
    child_parent_list = []
    child_parent_file = []
    for item in child_list: 
        for p in whole_list:
            if item == p[1]:
                parent = p[0]
                if parent != target:
                    child_parent_file.append(p[2])
                    child_parent_list.append(parent)
    return child_parent_list, child_parent_file


def markov_blanket_file(t_parent, t_child, t_child_parent):
    a
    return a


def find_parent_child_only(filename, target):
    f = readfile(filename)
    node_list = []
    file_list = []
    parent_list, parent_file = find_target_parent(target, f)
    child_list, child_file = find_target_child(target, f)
    node_list += parent_list
    node_list += child_list
    node_list.append(target)
    n_list = np.unique(node_list)
    file_list += parent_file
    file_list += child_file
    return n_list, file_list






def find_markov_blanket(filename, target):
    f = readfile(filename)
    node_list = []
    file_list = []
    parent_list, parent_file = find_target_parent(target, f)
    child_list, child_file = find_target_child(target, f)
    child_p_list, child_p_file = find_child_parent(child_list, f, target)
    node_list += parent_list
    node_list += child_list
    node_list += child_p_list
    node_list.append(target)
    n_list = np.unique(node_list)
    file_list += parent_file
    file_list += child_file
    file_list += child_p_file
    return n_list, file_list



def write_dot_file(node_list, file_list, writefilename):
    w = open(writefilename,'w')
    line = 'digraph G{'
    line += '\n'   
    line += 'ratio=fill;'
    line += '\n'
    line += 'node [shape=box, style=rounded];'
    line += '\n'
    w.write(line)
    for i in node_list:
        w.write(i)     
        w.write('\n')
    for k in file_list:
        w.write(k)
        w.write('\n')
    w.write('}')

def file_name_maker(cancer):

    filename = '/home/xicwang/Rodin_Paper/BNOmics/uthsph-bnomics-78dbc62fbc53/trinity_bn_dot_file/k5_0.995_9_19_2018_dot_file/'
    filename += cancer
    filename += '_0.995_K5_9_19_2018.dot'
    return filename

def write_file_name_maker(cancer):
    writefilename = '/home/xicwang/Rodin_Paper/BNOmics/uthsph-bnomics-78dbc62fbc53/markov_blanket/Trinity/'
    writefilename += cancer
    writefilename += '_tri_0.995_k5_9_19_18_MarBl_ParentChildOnly.dot'
    return writefilename

'''
import find_markov_blanket as fmb
cancer = 'GBM'
filename = fmb.file_name_maker(cancer)
writefilename = fmb.write_file_name_maker(cancer)
target = 'Tumor_Status'
fmb.main_markov_blanket(filename, target, writefilename)

dot -Tpdf dotfile.dot -o outpdf.pdf

filename = '/home/xicwang/Rodin_Paper/BNOmics/uthsph-bnomics-78dbc62fbc53/Trinity_survival_bn_dot_file/730_survival_k1_0.995_10_08_2018_bn_dot_file/GBMLGG_K1_0.995_10_08_2018_survival.dot'

writefilename = '/home/xicwang/Rodin_Paper/BNOmics/uthsph-bnomics-78dbc62fbc53/markov_blanket/Survival_markov_dot_file_Trinity/730_k1_0.995_dot_file_10_9_2018/GBMLGG_K1_0.995_10_08_2018_survival_markovB.dot'


'''

def main_markov_blanket(filename, target, writefilename):
    n_list, file_list = find_markov_blanket(filename, target)
    write_dot_file(n_list, file_list, writefilename)

def main():
    list = ['GBMLGG','KIPAN','LGG','LUAD','LUSC','OV','STES','THCA','UCEC','KIRC']
    for item in list:
        print('processing ', item, ' data...')
        cancer = item
        filename = file_name_maker(cancer)
        writefilename = write_file_name_maker(cancer)
        target = 'Tumor_Status'
        main_markov_blanket(filename, target, writefilename)

    return None


def main_for_parent_child_only():
    list = ['GBMLGG','KIPAN','LGG','LUAD','LUSC','OV','STES','THCA','UCEC','KIRC','BRCA', 'HNSC', 'GBM', 'PRAD']
    
    for item in list:
        print('processing ', item, ' data...')
        cancer = item
        filename = file_name_maker(cancer)
        writefilename = write_file_name_maker(cancer)
        target = 'Tumor_Status'
        n_list, file_list = find_parent_child_only(filename, target)
        write_dot_file(n_list, file_list, writefilename)

    return None








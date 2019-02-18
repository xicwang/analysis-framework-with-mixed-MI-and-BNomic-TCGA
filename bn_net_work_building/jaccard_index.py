

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


def find_target_parent_parent(parent_list, whole_list):
    parent_parent_list = []
    parent_parent_file = []
    for item in parent_list: 
        for p in whole_list:
            if item == p[1]:
                parent = p[0]
                parent_parent_file.append(p[2])
                parent_parent_list.append(parent)
    return parent_parent_list, parent_parent_file


def find_target_parent_children(parent_list, whole_list, target):
    parent_children_list = []
    parent_children_file = []
    for item in parent_list: 
        for p in whole_list:
            if item == p[0]:
                children = p[1]
                if children != target:
                    parent_children_file.append(p[2])
                    parent_children_list.append(children)
    return parent_children_list, parent_children_file



def find_child_children(child_list, whole_list):
    child_children_list = []
    child_children_file = []
    for item in child_list: 
        for p in whole_list:
            if item == p[0]:
                children = p[1]
                child_children_file.append(p[2])
                child_children_list.append(children)
    return child_children_list, child_children_file


def find_two_level_markov_blanket(filename, target):
    f = readfile(filename)
    node_list = []
    file_list = []
    parent_list, parent_file = find_target_parent(target, f)
    child_list, child_file = find_target_child(target, f)

    child_p_list, child_p_file = find_child_parent(child_list, f, target)
    child_c_list, child_c_file = find_child_children(child_list, f)

    parent_p_list, parent_p_file = find_target_parent_parent(parent_list, f)
    parent_c_list, parent_c_file = find_target_parent_children(parent_list, f, target)


    node_list += parent_list
    node_list += child_list
    node_list += child_p_list
    node_list += child_c_list
    node_list += parent_p_list
    node_list += parent_c_list
    node_list.append(target)
    n_list = np.unique(node_list)
    
    file_list += parent_file
    file_list += child_file
    file_list += child_p_file
    file_list += child_c_file
    file_list += parent_p_file
    file_list += parent_c_file
       
    return n_list, file_list


def compute_jaccard_index(set_1, set_2):
    x = set_1.intersection(set_2)
    print(x)
    n = len(x)
    print(n)
    print(len(set_1))
    print(len(set_2))
    return n / float(len(set_1) + len(set_2) - n) 



def get_jaccard_index_two_level(filename1, filename2, target):
    
    n_list1, file_list1 = find_two_level_markov_blanket(filename1, target)
    n_list2, file_list2 = find_two_level_markov_blanket(filename2, target)
    
    set_1 = set(n_list1)
    set_2 = set(n_list2)
    res = compute_jaccard_index(set_1, set_2)
    return res

def JI_whole_dot_file():


    return res































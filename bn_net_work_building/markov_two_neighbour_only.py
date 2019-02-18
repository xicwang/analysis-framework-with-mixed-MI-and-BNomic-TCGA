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




def find_child_parent(child_list, parent_list, whole_list, target):
    child_parent_list = []
    child_parent_file = []
    for item in child_list:
        for p in whole_list:
            if item == p[1]:
                parent = p[0]
                if parent != target and parent in parent_list:
                    child_parent_file.append(p[2])
                    child_parent_list.append(parent)
    return child_parent_list, child_parent_file

#for our paper, we only need parent and children, so not need to use the third method to find other connections. 

def find_markov_parent_and_children(filename, target):
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


def write_dot_file(node_list, file_list, writefilename):
    w = open(writefilename,'w')
    line = 'digraph G{'
    line += '\n'
    line += 'ratio=fill;'
    line += '\n'
    line += 'node [shape=box, style=rounded];'
    line += '\n'
    line += 'edge [arrowhead=none];'
    line+= '\n'
    
    w.write(line)
    for i in node_list:
        w.write(i)
        w.write('\n')
    for k in file_list:
        w.write(k)
        w.write('\n')
    w.write('}')


def main_markov_blanket(filename, target, writefilename):
    n_list, file_list = find_markov_parent_and_children(filename, target)
    write_dot_file(n_list, file_list, writefilename)




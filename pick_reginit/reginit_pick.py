#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re

#############################################
tb_fname = "tb_top.sv"
reg_string = "nreg_ncs"

f = open(tb_fname, 'r')

reg_list = []

for line in f:
    line = line.rstrip('\n')

    ## (nreg_ncs_***)でマッチさせてレジスタ名nreg_ncs_**をとりだす
    matchOB = re.search(r'\(.*(nreg_ncs_\w+)\s*\)', line)
    if matchOB:
        reg_list.append(matchOB.group(1))


#print(reg_list)

f.close()

###########################################

reg_core_fname = "register_core.sv"
f = open(reg_core_fname, 'r')

flg = False
state = 0

reg_dict = {}

for elem in reg_list:
    f.seek(0)
    for line in f:
        line = line.rstrip('\n')

        if state == 0:
            matchOB = re.search(r'if.*reset_n', line)
            if matchOB:
                state = 1
        elif state == 1:
            ## ***_nreg_ncs_*** <= #(P_DLY) 32'h01020304; でマッチさせ、32'h01020304　を抽出
            str_re = r".*{0}.*<=\D*(\d+'\w+)".format(elem)
            pattern = re.compile(str_re)
            matchOB = pattern.search(line) 

            if (matchOB):
                #print(matchOB.group(1))
                reg_dict[elem] = matchOB.group(1)
            elif re.search(r'else', line):
                state = 0
                

#print(reg_dict)


for elem in reg_dict.keys():
    print("wire {0} = {1};".format(elem, reg_dict[elem]))

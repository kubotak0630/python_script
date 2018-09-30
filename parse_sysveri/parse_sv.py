#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

class SvParser:
    def __init__(self, file_name):
        self._st_ary = [] ##statement
        self._enum_ary = []
        
        self.remove_comment(file_name, self._st_ary)

    def remove_comment(self, fname, st_ary):

        f = open('hoge2.sv', 'r')

        continue_flg = False
        for line in f:
            line = line.rstrip('\n')
            continue_flg = self._check_comment_out(line, continue_flg, st_ary)


        f.close()

    def show_debug(self):
    
        for elem in self._st_ary:
            print(elem)
        


    ##戻り値がTrueの時はコメントアウトが続いていることを示す remove_commnetから呼ばれる
    def _check_comment_out(self, str_line, continue_flg, st_ary):
        #for c in str_line:
        cmt_flg = continue_flg 
        ret_val = continue_flg
        removed_commnet = ''
        for i in range(len(str_line)):
            ## /*
            if i != 0 and cmt_flg == False and str_line[i-1] == '/' and str_line[i] == '*':
                cmt_flg = True
                ret_val = not(ret_val)
                ##すでに追加してある　/ を削除
                removed_commnet = removed_commnet[:-1]
            ## //
            elif i != 0 and cmt_flg == False and str_line[i-1] == '/' and str_line[i] == '/':
                ##すでに追加してある　/ を削除
                removed_commnet = removed_commnet[:-1]
                ret_val = False
                break
                
            ## */
            elif i != 0 and cmt_flg and str_line[i-1] == '*' and str_line[i] == '/':
                #print('find */ i={}'.format(i))
                cmt_flg = False
                ret_val = not(ret_val)
            elif cmt_flg == False:
                removed_commnet += str_line[i]

        if len(removed_commnet) != 0:
            st_ary.append(removed_commnet)

        return ret_val

    def extract_enum(self):

        enum_state_flg = False
        for line in self._st_ary:

            ## １行でenumが書かれているケース
            ## enum bit [1:0]{ val0 = 3'd0, val1 = 3'd1} hoge_val; 
            matchOB1 = re.search(r'.*enum.*;.*', line)
            if matchOB1:
                self._enum_ary.append(matchOB1.group(0))

            ## １行でenumがかかれていないケース
            ## typedef enum bit [2: 0] {
            #   REG0 = 3'b001,
            #   REG0 = 3'b010
            #  } hoge_reg;
            else:
                if enum_state_flg == False:

                    matchOB2 = re.search(r'.*enum.*', line)
                    if matchOB2:
                        enum_state_flg = True
                        str_temp = ''
                        str_temp += matchOB2.group(0)
                else:
                    str_temp += line

                    matchOB3 = re.search(r'.*;.*', line)
                    if matchOB3:
                        enum_state_flg = False
                        self._enum_ary.append(str_temp)



        ##debug pring
        '''
        for elem in self._enum_ary:
            print(elem)
        '''

        #(?:...)は正規表現をグループにまとめる拡張記法　　２’d１，２’b１，,8'h1,,2'o10(=8) 1
        for elem in self._enum_ary:
            hoge = re.findall(r'[\w]+\s*=\s*(?:[0-9]*\'(?:b|h|d|o))?[0-9a-hA-H]+', elem)

            print(hoge)

       



if __name__ == '__main__':
    parser = SvParser('hoge2.sv')

    parser.show_debug()
    parser.extract_enum()

    #test1 = '10'
    #print(int(test1,16))





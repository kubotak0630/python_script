# coding: utf-8 

import pandas as pd
import codecs #日本語をファイル出力するため必要
import openpyxl
import re

## True時は生成物のhtmlにCSSとJavaScriptを埋め込む設定
RELEASE_MODE = True


###  テーブルデータはdataframe構造 df で渡す
### dict = {'module':'ncs', 'addr':'00004600', 'reg_name': 'ncs_nreg_MONI0', 'val': 'A1006B1E', 'abnormal': False, 'df': df0}
#### df_ditc_ary = [dict0, dict1, dict2,.....]
def generate_html_core(df_ditc_ary):
    
    f = codecs.open('aaa.html', 'w', 'utf-8')


    f.write('<!DOCTYPE html>\n')
    f.write('<html lang="ja">\n')
    f.write('<head>\n')
    f.write('<meta charset="UTF-8">\n')
    f.write('<title>LogView</title>\n')
    if not RELEASE_MODE:
        f.write('<link rel="stylesheet" href="css/styles.css">\n')
    else:
        f.write('<style>\n')
        fp_css = codecs.open('css/styles.css', 'r', 'utf-8')
        for line in fp_css:
            f.write(line)
        fp_css.close()
        f.write('\n</style>\n')

    f.write('</head>\n')
    f.write('<body>\n')
    
    ## Summary  #################
    f.write('<div id=header>\n')
    f.write('<h1>Summary</h1>\n')
    f.write('<table id="summary_table">\n')
    
    ##table header
    f.write('<tr>\n')
    f.write('<th>addr</th>\n')    
    f.write('<th>module</th>\n')
    f.write('<th>reg_name</th>\n')
    f.write('<th>judge</th>\n')
    f.write('</tr>\n')
    
    ##table data
    for elem in df_ditc_ary:
        f.write('<tr>\n')
        judge = 'OK' if elem['abnormal'] == False else 'NG'
        f.write('<td>{:08X}</td>\n'.format(elem['addr']))
        f.write('<td>{}</td>\n'.format(elem['module']))
        f.write('<td><a href="#{}">{}</a></td>\n'.format(elem['reg_name'], elem['reg_name']))
        f.write('<td>{}</td>\n'.format(judge))
        f.write('<tr>\n')

    f.write('</table>\n')
    f.write('</div>\n')
    f.write('<hr color="#ccc" size="4">\n') #区切り線
    ## Register Dump ############
    f.write('<h1>Register Dump</h1>\n')
    f.write('<ul>\n')
    for elem in df_ditc_ary:
        df = elem['df']

        ##表の上の説明行
        #f.write('<li id="{}"><span class="empha">{}</span>&nbsp;<span class="empha">[{}]</span> &nbsp; <span class="empha">addr={:08X}</span>, <span class="empha">val={:08X}</span></li>\n'.format(elem['reg_name'], elem['module'], elem['reg_name'], elem['addr'], elem['val']))
        f.write('<li id="{}"><span class="empha">[{}] &nbsp;addr={:08X}, &nbsp;val={:08X} &nbsp;&nbsp;({})</span></li>\n'.format(elem['reg_name'], elem['reg_name'], elem['addr'], elem['val'], elem['module']))
        f.write('<table>\n')
        
        ##table header
        f.write('<tr>\n')
        for th in df.columns:
            f.write('<th>{}</th>\n'.format(th))
        f.write('</tr>\n')

        ##table data
        
        for elem_ary in df.values:
            f.write('<tr>\n')

            for td in elem_ary:
                if type(td) == int:
                    f.write('<td>{:X}</td>\n'.format(td))
                else:
                    f.write('<td>{}</td>\n'.format(td))
            f.write('</tr>\n')

        f.write('</table>\n')
        f.write('<br>\n')
    
    f.write('</ul>\n')
    if not RELEASE_MODE:
        f.write('<script type="text/javascript" src="test.js"></script>\n')
    else:
        f.write('<script type="text/javascript">\n')
        ##JSのファイルを書き出す
        fp_js = codecs.open('test.js', 'r', 'utf-8')
        for line in fp_js:
            f.write(line)
        fp_js.close()
        f.write('\n</script>\n')
    f.write('</body>\n')
    f.write('</html>\n')


    f.close()


class RegBitList_C():
    def __init__(self):
        self._regbit_list = []

    def add(self, reg_name, reg_addr, reg_val, module_name, regbit_name, bit_msb, bit_lsb, str_descript, nomal_val):
        
    
        if not self._already_exist(reg_addr):
            #クラス生成
            reg_obj = RegBit_C(reg_name, reg_addr, reg_val, module_name)
            reg_obj.set_row_info(regbit_name, bit_msb, bit_lsb, str_descript, nomal_val)
            
            #リストに追加
            self._regbit_list.append(reg_obj)

        else:
            self._regbit_list[-1].set_row_info(regbit_name, bit_msb, bit_lsb, str_descript, nomal_val)
        
       

    def create_html(self):

    
        ##DataFrameのリストを作成
        df_dict_ary =[]
        for elem in self._regbit_list:
            df = pd.DataFrame(elem._row_info_list, columns=['regbit_name', 'bit_def', 'value', 'description', '正常値'])
            df_dict_ary.append({'module':elem._module_name,
                                'addr': elem._addr,
                                'reg_name': elem._reg_name,
                                'val': elem._val_32bit,
                                'abnormal':elem.is_abnormal(),
                                'df': df})
        
        generate_html_core(df_dict_ary)

 

    ##reg_addrが既にself._regbit_list に登録されているかどうかを判定
    ## 登録されていなかったらFalse, 登録済みの場合はTrue
    def _already_exist(self, reg_addr):
        
        ret_val = False

        ##Noneの場合は登録済みとする
        if reg_addr == None:
            return True

        for regbit in self._regbit_list:
            if regbit.get_addr() == reg_addr:
                ret_val = True
                break
    
        return ret_val
    
    
### ひとつのレジスタ(ひとつのアドレス)を示すクラス
### bit毎に定義されたregbitの情報をself._row_info_list[] に保持する
class RegBit_C():
    ##addr, val_32bit はint型
    def __init__(self, reg_name, addr, val_32bit, module_name):
        self._reg_name = reg_name
        self._addr = addr
        self._val_32bit = val_32bit
        self._module_name = module_name
        self._row_info_list = []
    
    def get_addr(self):
        return self._addr

    def set_row_info(self, regbit_name, bit_msb, bit_lsb, str_descript, nomal_val):
        
        bit_data = self._get_bit_data(bit_msb, bit_lsb, self._val_32bit)
        str_temp = '[{}:{}]'.format(bit_msb, bit_lsb)
        self._row_info_list.append([regbit_name, str_temp, bit_data, str_descript, nomal_val])

    def _get_bit_data(self, msb, lsb, data32):

        ##マスクビットの作成
        mask_bit = 0
        for i in range(lsb, msb+1):
            mask_bit += (1 << i)

        #print('MASK_BIT=0x{:08X}'.format(mask_bit))
        #print('data={:X}'.format((data32 & mask_bit) >> lsb))
        return (data32 & mask_bit) >> lsb

    ##Normal値と違うレジスタがある場合はTrueを返す
    def is_abnormal(self):
        ret_val = False
        for elem in self._row_info_list:
            bit_data = elem[2]
            nomal_val = elem[4]
            if type(bit_data) == int and type(nomal_val) == int and bit_data != nomal_val:
                ret_val = True
                break

        return ret_val

def get_from_file(fp, seach_addr):

    fp.seek(0)

    ret_val = None
    ##下位4bitをidxにする
    idx = (int(seach_addr, 16) & 0xF) >> 2

    ##下位4bitを0で丸めた文字列を作る. ここで16進は大文字に固定
    new_key = '{:X}'.format(int(seach_addr, 16) & 0xFFFFFFF0)

    for line in fp:
        line = line.rstrip('\n')
        
        matchOB = re.match(r'.*{}\s*=\s*(.+)\s(.+)\s(.+)\s(.+)'.format(new_key), line)
        if matchOB:
            #print(matchOB.group(0))
            #print(matchOB.group(1), matchOB.group(2), matchOB.group(3), matchOB.group(4))
            ret_val = matchOB.group(idx+1)
            break
    
    if ret_val is None:
        print('error get_from_file(), not find\n')
        exit()

    return ret_val


if __name__ == '__main__':


    print("hello pandas")

    f = open('data.log')

    regbit_list = RegBitList_C()

    wb = openpyxl.load_workbook('log_data.xlsx')
    sheet = wb['NDC']


    ADDR_COL = 0
    REGNAME_COL = 1
    MODULE_COL = 2
    REGBIT_NAME_COL = 3
    BIT_MSB_COL = 4
    BIT_LSB_COL = 5
    DESCRIPTION_COL = 6
    NORMAL_VAL_COL = 7

    addr_col = sheet.columns[ADDR_COL]
    #now_addr
    str_addr = ''
    for cell_obj in sheet.columns[REGBIT_NAME_COL]:
        
        idx = cell_obj.row - 1 ##rowは1スタートのため
        ##2行目からスタートという前提をおく(暫定)
        if idx < 1:
            continue

        #print(cell_obj.value, addr_col[idx].value, type(addr_col[idx].value))
        #print(sheet.columns[ADDR_COL][idx].value, type(sheet.columns[ADDR_COL][idx].value))
        
        ##ファイルからアドレスに対応する32bitデータを取得
        #エクセルから取得した値が文字列(16進で文字列が含まれるとき)ではなくIntのときは文字列に変換とする
        addr = sheet.columns[ADDR_COL][idx].value
        if type(addr) == int:
            str_addr = str(addr)
        ##None(エクセルのセルを結合した場合はNoneとなる)は前の値をそのまま使う
        elif addr == None:
            pass
        else:
            str_addr = addr

        str_get_addr = get_from_file(f, str_addr)
        
        ## ******************
        regbit_list.add(sheet.columns[REGNAME_COL][idx].value,
                        int(str_addr, 16),
                        int(str_get_addr, 16),
                        sheet.columns[MODULE_COL][idx].value,
                        sheet.columns[REGBIT_NAME_COL][idx].value,
                        sheet.columns[BIT_MSB_COL][idx].value,
                        sheet.columns[BIT_LSB_COL][idx].value,
                        sheet.columns[DESCRIPTION_COL][idx].value,
                        sheet.columns[NORMAL_VAL_COL][idx].value)
        

    
    regbit_list.create_html()

    
    

    f.close()
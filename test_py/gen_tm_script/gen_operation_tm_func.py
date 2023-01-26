import os
import json
import sys
import binascii
import re
import os.path
from itertools import islice
sys.path.append('./')

def gen_init_data(data_name, data_file_path, set_mem_data):
    init_data = re.findall('\|(%s\w+)\|.*\n((\s+DCD\s0x\w+\n)+)' %data_name, set_mem_data)
    for i in range(len(init_data)):
        data_file = open("%s/%s.txt" %(data_file_path, init_data[i][0]), "w")       
        data_init_array=str(init_data[i][1]).replace('    DCD ','') + "END"
        data_init_array=str(data_init_array).replace('\n',', ') #this is for unix text file
        # data_init_array=str(data_init_array).replace('\r\n',', ') #this is for window text file
        # data_init_array=str(data_init_array).replace(', 	SPACE 512','')
        data_init_array=str(data_init_array).replace(', END','')
        data_file.write("%s = [%s]\n\n" %(init_data[i][0], data_init_array))

def set_mem_write(mod_name, mem_area, mem_size, tm_file):
    mem_list = []
    mem_base = mem_area[0][1]
    size_str = mem_size[0][1]
    mem_area_name = mod_name + "_MEMORY_BASE"
    mem_size_name = mod_name + "_MEMORY_SIZE"
    list_name = mod_name.lower() + "_list"
    tm_file.write('# %s memory area\n' %mod_name)
    tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
    tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
    tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
    tm_file.write('SCHEAP.sc_start(10)\n')    
    
    for i in range(len(mem_area)):
        mem_list.append(["%s.txt" %mem_area[i][0], mem_area[i][1]])
        # tm_file.write('## channel %s ##\n' %mem_area_dmai[i][0])
        # tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mem_area_dmai[i][0])
        # tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %mem_area_dmai[i][1] )
        # tm_file.write('SCHEAP.sc_start(10)\n')
    tm_file.write('%s = %s\n' %(list_name, mem_list))
    tm_file.write('for i in range(len(%s)):\n' %list_name)
    tm_file.write('\tfile_handle = open(input_path + %s[i][0], "r")\n' %list_name)
    tm_file.write('\tdata = re.findall("0x\w+", file_handle.read())\n')
    tm_file.write('\tdata = [int(x, 16) for x in data]\n')
    tm_file.write('\tbuffer = ConvertWordArrayToHexString(data, True)\n')
    tm_file.write('\tSCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", int(%s[i][1], 16), buffer)\n' %list_name)
    tm_file.write('\tSCHEAP.sc_start(10)\n')
    tm_file.write('\tfile_handle.close()\n')
    tm_file.write('\n')

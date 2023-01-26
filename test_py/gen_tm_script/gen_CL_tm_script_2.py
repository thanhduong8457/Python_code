#!/usr/bin/python

import os
import json
import sys
import binascii
import re
from itertools import islice
sys.path.append('./')

f = open("./tm_CL_2.list") #open particular tm_file
tm_idx = 0
for file in f:
    if "#" not in file:
        file = file.strip()
        tm_idx += 1
        if tm_idx < 10:
            idx = "0" + str(tm_idx)
        else:
            idx = str(tm_idx)
        #tm_name = "tp02" + "_" + idx + "_" + re.findall('.*/(.+?)$', tm)[0] #name of output file
        tm_name = "tp03_003" + "_" + re.findall('[0-9]_(.+?)$',file)[0].lower() #name of output file
        tm_name = tm_name.strip()
        tm_name = tm_name.replace("_new","")
        #Generate pattern
        print(tm_name)

        tm_file = open("./CL_python_pat_2/%s.py" %(tm_name), "w")

        tm_file.write('###############################\n')
        tm_file.write('# TM : %s  \n' %tm_name)
        tm_file.write('###############################\n')
        tm_file.write('\n')
        
        with open("./header_info.txt") as header:
            head_info = header.read()
        tm_file.write(head_info)

        tm_file.write('\n')
        tm_file.write('#################\n')
        tm_file.write('# SET ENV       #\n')
        tm_file.write('#################\n')
        tm_file.write('\n')
        
        #create mem data array
        tm_file.write("# DATA INIT ARRAY\n")
        with open("../03_CMD_LIST/%s/set_mem.txt" %file) as mem_info: #get data to allocate memory
            start = 0
            end = 0
            count = 0
            init_array = []            
  
            for x in mem_info:
                if x.find("AREA") > 0:
                    start_name = x.find("AREA") + 6
                    end_name = x.find("|", start_name)
                    name_mem = x[start_name:end_name]
                if x.find("DCD") > 0:
                    if (x.find(";") < x.find("DCD")) and (x.find(";") != -1):
                        continue
                    elif x.find(";HuyTruong") >= 0:
                        continue
                    else:
                        cmd = x.find("DCD")
                        if cmd >= 0:
                            start_x = x.find("0x")
                            end_x = start_x + 10
                            addr = x[start_x:end_x]
                            init_array.append(addr)
                            data_init_array = str(init_array).replace('\'','')
                elif x.find("DCW") > 0:
                    if x.find(";") > 0:
                        continue
                    else:
                        start_x = x.find("DCW") + 4
                        end_x = start_x + 6
                        addr = x[start_x:end_x]
                        init_array.append(addr)
                        data_init_array = str(init_array).replace('\'','')               
                if (x.find(";;") >= 0) and ("source" in name_mem):
                    tm_file.write("%s = %s" %(name_mem,data_init_array) )
                    tm_file.write("\n")
                    init_array = []
                elif (x.find("END") >= 0):
                    tm_file.write("%s = %s" %(name_mem,data_init_array) )
                    tm_file.write("\n")
                    init_array = []
        
        #Locate data from array to mem area
        tm_file.write('\n')
        tm_file.write('\n')
        tm_file.write('# CREATE MEMORY AREA\n')
        with open("../03_CMD_LIST/%s/area.txt" %file) as area_info: #get addr of each mem area
            read_area_info = area_info.read()
            tm_file.write('# Descriptor memory area\n')
            tm_file.write('CL_MEMORY_BASE = 0x01000000\n')
            if "_SASL_" in file:
                tm_file.write('CL_MEMORY_SIZE = 0x00100000\n')
            else:
                tm_file.write('CL_MEMORY_SIZE = 0x00040000\n')
            tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", CL_MEMORY_BASE, CL_MEMORY_SIZE)\n')
            tm_file.write('SCHEAP.sc_start(10)\n')
            if ('Descriptor' in read_area_info):
                tm_file.write('buffer = ConvertWordArrayToHexString(Descriptor, True)\n')
            if ('descriptor' in read_area_info):
                tm_file.write('buffer = ConvertWordArrayToHexString(descriptor, True)\n')
            tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", CL_MEMORY_BASE, buffer)\n')
            tm_file.write('SCHEAP.sc_start(10)\n')
            tm_file.write('\n')

            if('sourcei0' in read_area_info):
                tm_file.write('# SOURCEi0 memory area\n')
                tm_file.write('SOURCEi0_MEMORY_BASE = 0xf3ac0008\n')
                tm_file.write('SOURCEi0_MEMORY_SIZE = 0x00400000\n')
                tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", SOURCEi0_MEMORY_BASE, SOURCEi0_MEMORY_SIZE)\n')
                tm_file.write('SCHEAP.sc_start(10)\n')
                name_ch = "sourcei0"
                tm_file.write('## channel %s ##\n' %name_ch)
                tm_file.write('buffer = ConvertHalfWordArrayToHexString(%s, True)\n' %name_ch)
                tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", SOURCEi0_MEMORY_BASE, buffer)\n' )
                tm_file.write('SCHEAP.sc_start(10)\n')
                tm_file.write('\n')

            if('sourcei1' in read_area_info):
                tm_file.write('# SOURCEi1 memory area\n')
                tm_file.write('SOURCEi1_MEMORY_BASE = 0xf36bf008\n')
                tm_file.write('SOURCEi1_MEMORY_SIZE = 0x00400000\n')
                tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", SOURCEi1_MEMORY_BASE, SOURCEi1_MEMORY_SIZE)\n')
                tm_file.write('SCHEAP.sc_start(10)\n')
                name_ch = "sourcei1"
                tm_file.write('## channel %s ##\n' %name_ch)
                tm_file.write('buffer = ConvertHalfWordArrayToHexString(%s, True)\n' %name_ch)
                tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", SOURCEi1_MEMORY_BASE, buffer)\n' )
                tm_file.write('SCHEAP.sc_start(10)\n')
                tm_file.write('\n')

            if('sourcei2' in read_area_info):
                tm_file.write('# SOURCEi2 memory area\n')
                tm_file.write('SOURCEi2_MEMORY_BASE = 0xf32be008\n')
                tm_file.write('SOURCEi2_MEMORY_SIZE = 0x00400000\n')
                tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", SOURCEi2_MEMORY_BASE, SOURCEi2_MEMORY_SIZE)\n')
                tm_file.write('SCHEAP.sc_start(10)\n')
                name_ch = "sourcei2"
                tm_file.write('## channel %s ##\n' %name_ch)
                tm_file.write('buffer = ConvertHalfWordArrayToHexString(%s, True)\n' %name_ch)
                tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", SOURCEi2_MEMORY_BASE, buffer)\n' )
                tm_file.write('SCHEAP.sc_start(10)\n')
                tm_file.write('\n')

            if('sourcei3' in read_area_info):
                tm_file.write('# SOURCEi3 memory area\n')
                tm_file.write('SOURCEi3_MEMORY_BASE = 0xf2ebd008\n')
                tm_file.write('SOURCEi3_MEMORY_SIZE = 0x00400000\n')
                tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", SOURCEi3_MEMORY_BASE, SOURCEi3_MEMORY_SIZE)\n')
                tm_file.write('SCHEAP.sc_start(10)\n')
                name_ch = "sourcei3"
                tm_file.write('## channel %s ##\n' %name_ch)
                tm_file.write('buffer = ConvertHalfWordArrayToHexString(%s, True)\n' %name_ch)
                tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", SOURCEi3_MEMORY_BASE, buffer)\n' )
                tm_file.write('SCHEAP.sc_start(10)\n')
                tm_file.write('\n')

        
        tm_file.write('# Set clock\n')
        tm_file.write('SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral", "clk", 800000000)\n')
        tm_file.write('SCHEAP.sc_start(10)\n')
        tm_file.write('\n')
        tm_file.write('# De-assert reset\n')
        tm_file.write('SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral", "preset", 0)\n')
        tm_file.write('SCHEAP.sc_start(10)\n')
        tm_file.write('\n')

        tm_file.write('#################\n')
        tm_file.write('# RUNS TEST     #\n')
        tm_file.write('#################\n')
        tm_file.write('\n')
        
        with open("../03_CMD_LIST/%s/set_reg.txt" %file) as reg_info: #get data of reg setting
            tm_file.write('# Active module setting\n')
            for x in reg_info:
                if x.find(";IOW") > 0:
                    continue
                elif x.find(";IOR") > 0:
                    continue
                elif x.find(";HuyTruong") >= 0:
                    continue

                elif x.find(";IMP_MSK_CHECK") >= 0:
                    continue

                elif x.find(";IMPSC_CHECK") >= 0:
                    continue

                elif x.find("IOW") > 0:
                    #get base addr of regs setting
                    if x.find("IMPCNN_SRC") > 0:
                        start_reg = x.find("IMPCNN_SRC")
                        reg_addr = "0xFF9E0018"
                    elif x.find("IMPCNN_SACL") > 0:
                        start_reg = x.find("IMPCNN_SACL")
                        reg_addr = "0xFF9E0104"
                    elif x.find("IMPCNN_SCLP") > 0:
                        start_reg = x.find("IMPCNN_SCLP")
                        reg_addr = "0xFF9E0108"
                    elif x.find("IMP_CNN_BASE") > 0:
                        reg_info = re.findall('(IMP_CNN_BASE.\+.\w+).\s*(\w+)', x)
                        start_reg = x.find(reg_info[0][1])
                        reg_addr = reg_info[0][0]
                    else:
                        start_reg = x.find("0x")
                        end_reg = start_reg + 10
                        reg_addr = x[start_reg:end_reg]                        
                        reg_addr=re.sub('0xFFAA','0xFF9E',reg_addr)                        
                    #get data to allocate regs
                    start_data = x.find("0x",start_reg+2)
                    end_data = start_data + 10
                    wdata = x[start_data:end_data]
                    if "IMP_CNN_BASE" in x:
                        wdata = reg_info[0][1]
                    if (reg_addr == "0xFF9E0808"):
                        tm_file.write('SCHEAP.IMP_CNN_WriteHiddenRegister("imp_cnn", %s, %s)\n' %(reg_addr, wdata) )
                    elif "IMP_CNN_BASE" in x:
                        tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD, iodef.%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                    else:
                        tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD,%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                    if (reg_addr == "0xFF9E0108") or ("0x0108" in x):
                        tm_file.write('SCHEAP.sc_start(10000000)\n')
                    else:
                        tm_file.write('SCHEAP.sc_start(10)\n')
                elif x.find(" IOR") > 0:
                    #get base addr of regs setting
                    start_reg = x.find("0x")
                    end_reg = start_reg + 10
                    reg_addr = x[start_reg:end_reg]
                    reg_addr=re.sub('0xFFAA','0xFF9E',reg_addr)
                    reg_addr=re.sub('0xffaa','0xFF9E',reg_addr) 
                    #get data to allocate regs
                    start_data = x.find("0x",start_reg+2)
                    end_data = start_data + 10
                    rdata = x[start_data:end_data]
                    if (reg_addr == '0xFF9E0810' or reg_addr == '0xFF9E0814'or reg_addr == '0xFF9E0818' or reg_addr == '0xFF9E081C' or reg_addr == '0xFF9E0820'):
                        tm_file.write('ReadHidReg_Result = SCHEAP.IMP_CNN_ReadHiddenRegister("imp_cnn", %s)\n' %(reg_addr))
                        tm_file.write('SCHEAP.sc_start(10)\n')
                        tm_file.write('if (ReadHidReg_Result != %s):\n' %(rdata))
                        tm_file.write('\tprint("Wrong value of Hidden register, Read data: %s, Expected: %s" %(hex(ReadHidReg_Result),hex({})))\n'.format(rdata))
                        tm_file.write('\tSCHEAP.DummyMasterRvc_SetTMFail("dummy_master")\n')
                        tm_file.write('\tSCHEAP.sc_start(1000)\n')
                    else:    
                        tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, rdata) )
                        tm_file.write('SCHEAP.sc_start(10)\n')
                        tm_file.write('SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s)\n' %rdata)
                        tm_file.write('SCHEAP.sc_start(10)\n')
                elif (x.find("IMP_MSK_CHECK IMPCNN_SR") > 0):
                    sr_data = re.findall('(0x\w{8}).\s*(\w+).\s*(\w+).\s*(\w+)',x)
                    # bit_check = int(sr_data[0][0],16)
                    # count = 0
                    # i = 0
                    # for j in range(0,32):
                    #     if (bit_check >> i != 1):
                    #       i=+j
                    #       count += 1
                    tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    tm_file.write('MaskCheck = SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s, %s)\n' %(sr_data[0][0], sr_data[0][1]))
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    if sr_data[0][2] == 'EQ':
                        tm_file.write('while (MaskCheck == 1):\n')
                    if sr_data[0][2] == 'NEQ':
                        tm_file.write('while (MaskCheck != 1):\n')
                    tm_file.write('    SCHEAP.sc_start(100000)\n')
                    tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    tm_file.write('    SCHEAP.sc_start(10)\n')
                    tm_file.write('    MaskCheck = SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s, %s)\n' %(sr_data[0][0], sr_data[0][1]))
                    tm_file.write('    SCHEAP.sc_start(10)\n')
                elif(x.find("IMPSC_CHECK0 IMP_CNN_BASE") > 0):
                    sr_data = re.findall('(0x\w{8}).\s*(\w+).\s*(\w+)',x)
                    bit_check = int(sr_data[0][0],16)
                    i = 0
                    while (bit_check >> i != 1):
                        if (bit_check == 0x0):
                            break
                        i += 1
                    tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    # if "0x00004000, EQ, 0" in x:
                    #     tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", 14) == 1):\n')
                    if sr_data[0][1] == 'EQ':
                        tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", %d) == 1):\n' %i)
                    elif sr_data[0][1] == 'NEQ':
                        tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", %d) != 1):\n' %i)
                    tm_file.write('    SCHEAP.sc_start(100000)\n')
                    tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    tm_file.write('    SCHEAP.sc_start(10)\n')  
            tm_file.write('\n')

        tm_file.write('SCHEAP.DummyMasterRvc_SetTMPass("dummy_master")\n')
        tm_file.write('SCHEAP.sc_start(10000)\n')

        
        tm_file.close()

f.close()

print("********************")
print("*Finish generate TM*")
print("********************")


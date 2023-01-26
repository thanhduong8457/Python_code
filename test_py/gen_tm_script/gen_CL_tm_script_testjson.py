#!/usr/bin/python

import os
import json
import sys
import binascii
import re
import os.path
import tarfile
from itertools import islice
sys.path.append('./')

    
tm_list = open("./tm_CL_testjson.list") #get TM path
for tm in tm_list:
    if "#" not in tm:
        tm_path = tm.strip()
        tm_name = "tp03" + "_" + "003" + "_" + re.findall('._(.+?)$', tm)[0] #name of output file
        tm_name = tm_name.strip().lower()
        tm_name = tm_name.replace("_new","")
        dir = "003_CL"
        if not os.path.isdir("./input/3_Operation/%s/%s" %(dir, tm_name)):
            os.mkdir("./input/3_Operation/%s/%s" %(dir, tm_name))

        #TM GENERATION
        # if not os.path.isfile("../%s/test.json" %tm_path) and os.path.isfile("../%s/test.json.tar.bz2" %tm_path):
            # tar = tarfile.open("../%s/test.json.tar.bz2" %tm_path, "r:bz2")  
            # tar.extractall("../%s/" %tm_path)
            # tar.close()
            
        # if not os.path.isfile("../%s/test.json" %tm_path) and os.path.isfile("../%s/test.json.tar.gz" %tm_path):
            # tar = tarfile.open("../%s/test.json.tar.gz" %tm_path, "r:gz")
            # tar.extractall("../%s/" %tm_path)
            # tar.close()
        
        with open("../03_CMD_LIST/%s/test.json" %tm_path) as input:
            tm_file = open("./CL_python_pat_testjson/%s.py" %tm_name, "w")
            tm_file.write('\n')
            tm_file.write('###############################\n')
            tm_file.write('# TM : %s  \n' %tm_path)
            tm_file.write('###############################\n')
            tm_file.write('\n')
            with open("./header_info.txt") as header:
                head_info = header.read()
            tm_file.write(head_info)
            
            read_input_tm = json.loads(input.read())
            cnnip_tests = read_input_tm["cnnip_tests"]
            env = cnnip_tests[0]["environment"]
            runs = cnnip_tests[0]["runs"]
        
            tm_file.write('\n')
            tm_file.write('#################\n')
            tm_file.write('# SET ENV       #\n')
            tm_file.write('#################\n')
            tm_file.write('\n')
        
            #env include fixed_memory, heap_memory
            fixed_mem = env["fixed_memory"]
            heap_mem = env["heap_memory"]

            dmai_list_init = []
            dma3dc_list_init = []
            dmao_list_init = []
            dumparea_list_init = []
            dmarf_list_init = []
        
            #create mem data array
            tm_file.write("# DATA INIT ARRAY\n")
            for element in fixed_mem:
                mod_name = element["name"]
                mem_base = element["start"]
                size_str = element["size"]
        
                size_hex = int(size_str,16)
                size_hex_str = hex(size_hex)[2:]
                
                if "sections" in element:
                    for mod in element["sections"]:
                        data_file = open("./input/3_Operation/%s/%s/%s.txt" %(dir, tm_name, mod["name"]), "w")

                        if (element["name"] == "DMAO"):
                            dmao_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                            dmao_list = str(dmao_list_init).replace('u','')
                            channel_size = int(mod["size"],16)
                            num_data_channel = channel_size >> 2                                    
                            data_init = mod["init"]["fill_u32"]
                            init_array = []
                            for i in range(num_data_channel):
                                init_array.append(data_init)
                            data_init_array = str(init_array).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        elif (element["name"] == "DUMPAREA"):
                            dumparea_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                            dumparea_list = str(dumparea_list_init).replace('u','')
                            channel_size = int(mod["size"],16)
                            num_data_channel = channel_size >> 2                                    
                            data_init = mod["init"]["fill_u32"]
                            init_array = []
                            for i in range(num_data_channel):
                                init_array.append(data_init)
                            data_init_array = str(init_array).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        elif (element["name"] == "DMARDESA"):
                            channel_size = int(mod["size"],16)
                            num_data_channel = channel_size >> 2                                    
                            data_init = mod["init"]["fill_u32"]
                            init_array = []
                            for i in range(num_data_channel):
                                init_array.append(data_init)
                            data_init_array = str(init_array).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        elif (element["name"] == "DMA3DC"):
                            dma3dc_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                            dma3dc_list = str(dma3dc_list_init).replace('u','')
                            data_init = mod["init"]["data_u32"]
                            data_init_array = str(data_init).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        elif (element["name"] == "DMAI"):
                            dmai_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                            dmai_list = str(dmai_list_init).replace('u','')
                            data_init = mod["init"]["data_u32"]
                            data_init_array = str(data_init).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        elif (element["name"] == "DMARF"):
                            dmarf_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                            dmarf_list = str(dmarf_list_init).replace('u','')
                            data_init = mod["init"]["data_u32"]
                            data_init_array = str(data_init).replace('\'','')
                            data_init_array = str(data_init_array).replace('u','')
                            data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                        #tm_file.write('\n')
                elif mod_name == "Descriptor":
                    with open("../03_CMD_LIST/%s/set_mem.txt" %tm_path) as des_mem:
                        read_input_tm = des_mem.read()
                        start = read_input_tm.find(';   Descriptor List')
                        end = read_input_tm.find('END', start)
                        descriptor_data = read_input_tm[start:end]
        
                        init_array = []
                        with open ("tmp","w") as f_tmp:
                            f_tmp.write(descriptor_data)
                        with open ("tmp","r") as f_tmp:
                            for x in f_tmp:
                                if x.find(";DCD") > 0:
                                    continue                                        
                                elif x.find(";HuyTruong") >= 0:
                                    continue
                                elif x.find("DCD") > 0:
                                    start_x = x.find("DCD") + 4
                                    end_x = x.find("DCD") + 14
                                    addr = x[start_x:end_x]
                                    init_array.append(addr)
                        if os.path.exists("tmp"):
                            os.remove("tmp")
                    data_init_array = str(init_array).replace('\'','')
                    tm_file.write('%s = %s\n' %(mod_name, data_init_array) )
                    tm_file.write('\n')
        
            #Locate data from array to mem area
            tm_file.write('input_path = "../../../../linux/pat/input/3_Operation/%s/%s/"\n' %(dir, tm_name))
            tm_file.write('# SET MEMORY AREA\n')
            for element in fixed_mem:
                mod_name = element["name"]
                mem_base = element["start"]
                size_str = element["size"]
                if mod_name == "Descriptor":
                    name = "CL"
                else:
                    name = mod_name
                mem_area_name = name + "_MEMORY_BASE"
                mem_size_name = name + "_MEMORY_SIZE"
                list_name = name.lower() + "_list"
                size_hex = int(size_str,16)
        
                if "sections" in element:
                    tm_file.write('# %s memory area\n' %mod_name)
                    tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
                    tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
                    tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
                    tm_file.write('SCHEAP.sc_start(10)\n') 
                    if mod_name == "DMAI":
                        tm_file.write('dmai_list = %s\n' %dmai_list)
                    elif mod_name == "DMA3DC":
                        tm_file.write('dma3dc_list = %s\n' %dma3dc_list)
                    elif mod_name == "DMAO":
                        tm_file.write('dmao_list = %s\n' %dmao_list)
                    elif mod_name == "DUMPAREA":
                        tm_file.write('dumparea_list = %s\n' %dumparea_list)
                    elif mod_name == "DMARF":
                        tm_file.write('dmarf_list = %s\n' %dmarf_list)
                    tm_file.write('for i in range(len(%s)):\n' %list_name)
                    tm_file.write('\tfile_handle = open(input_path + %s[i][0], "r")\n' %list_name)
                    tm_file.write('\tdata = re.findall("0x\w+", file_handle.read())\n')
                    tm_file.write('\tdata = [int(x, 16) for x in data]\n')
                    tm_file.write('\tbuffer = ConvertWordArrayToHexString(data, True)\n')
                    tm_file.write('\tSCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s + int(%s[i][1], 16), buffer)\n' %(mem_area_name, list_name))
                    tm_file.write('\tSCHEAP.sc_start(10)\n')
                    tm_file.write('\tfile_handle.close()\n')
                elif mod_name == "Descriptor":
                    tm_file.write('# %s memory area\n' %mod_name)
                    tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
                    tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
                    tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    
                    tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mod_name)
                    tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %(mem_area_name) )
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    tm_file.write('\n')
               
            #tm_file.write(head_info)        
        
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
        
            with open("../03_CMD_LIST/%s/set_reg.txt" %tm_path) as reg_info: #get data of reg setting
                tm_file.write('# Active module setting\n')
                for x in reg_info:
                    if x.find(";IOW") > 0:
                        continue
                    elif x.find(";IOR") > 0:
                        continue
                    elif x.find(";HuyTruong") >= 0:
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
                        if (reg_addr == "0xFF9E0808") or ("0x0808" in reg_addr):
                            tm_file.write('SCHEAP.IMP_CNN_WriteHiddenRegister("imp_cnn", iodef.%s, %s)\n' %(reg_addr, wdata) )
                            #tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master,iodef.WRITE_CMD,0xFF9E0808, 0x4,0x00000001, 0x0, 0x0)\n')
                        elif "IMP_CNN_BASE" in x:
                            tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD, iodef.%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                        else:
                            tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD, %s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                        if (reg_addr == "0xFF9E0108") or ("0x0108" in x):
                            tm_file.write('SCHEAP.sc_start(1000000)\n')
                        else:
                            tm_file.write('SCHEAP.sc_start(10)\n')                            
                    elif x.find(" IOR") > 0:
                        #get base addr of regs setting
                        start_reg = x.find("0x")
                        end_reg = start_reg + 10
                        reg_addr = x[start_reg:end_reg]
                        reg_addr=re.sub('0xFFAA','0xFF9E',reg_addr) 
                        #get data to allocate regs
                        start_data = x.find("0x",start_reg+2)
                        end_data = start_data + 10
                        rdata = x[start_data:end_data]
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

        
            tm_file.write('## Dump DMAO area\n')
            tm_file.write('count_fail = 0\n')
            if (dir == "08_DMR_random") or (dir == "08_DMR_SPMC"):
                pass
            else: #Others use DMO data
                result = open("../03_CMD_LIST/%s/result.txt.l" %tm_path)
                #read_result = result.read()
                for element in fixed_mem:
                    mod_name = element["name"]
                    mem_base = element["start"]
                    size_str = element["size"]
                    result_addr_base = mem_base[2:]
                    if "sections" in element:
                        len_dmao = len(element["sections"])
                        for mod in element["sections"]:
                            if (element["name"] == "DMAO"):
                                offset = mod["offset"]
                                size_ch = mod["size"]
                                name_ch = mod["name"]
                                num_data = int(size_ch,16) >> 4
                                mod_num_data = int(size_ch,16)%16
                                if mod_num_data > 0:
                                    num_data += 1
                                else:
                                    num_data = num_data
                                if tm_path == "06_ARI/ari_eol_eot_x1y1":
                                    num_data = 8
                                elif tm_path == "06_ARI/ari_eol_eot_x1y1_s16":
                                    num_data = 16
                                s = ""
                                for y in range(0, num_data):
                                    line = result.readline()
                                    lower_data = line[9:].strip().replace(' ','').replace('\n','').lower()
                                    s += lower_data
                                exp_data_ch = s

                                tm_file.write('base_address = %s_MEMORY_BASE + %s\n' %(element["name"], offset) )
                                tm_file.write('exp_result_ch = "%s"\n' %exp_data_ch)
                                tm_file.write('result_ch = ""\n')
                                tm_file.write('for y in range (0, %d):\n' %num_data)
                                if mod_num_data > 0:
                                    tm_file.write('    if y == %d:\n' %(num_data-1))
                                    tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), %d)\n' %mod_num_data)
                                    tm_file.write('    else:\n')
                                    tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                                else:
                                    tm_file.write('    buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                                tm_file.write('    result_ch = result_ch + binascii.hexlify(buffer) \n')
                                tm_file.write('    SCHEAP.sc_start(10)\n')
                                #tm_file.write('print("[0x%s]: %s") % (format(base_address, \'08X\'), binascii.hexlify(result_ch))\n')
                                tm_file.write('if exp_result_ch == result_ch:\n')
                                tm_file.write('    print("#### CHANNEL DATA MATCHING #####")\n')
                                tm_file.write('#    print("[0x%s]: %s") % (format(base_address, \'08X\'), result_ch)\n')
                                tm_file.write('else:\n')
                                tm_file.write('    print("#### CHANNEL DATA MISMATCHED #####")\n')
                                tm_file.write('    count_fail += 1\n')
                                tm_file.write('    print("channel %s is fail:")\n' %name_ch)
                                tm_file.write('#    print("exp_result_ch: %s" %exp_result_ch)\n')
                                tm_file.write('#    print("result_ch: %s" %result_ch)\n')
                                tm_file.write('\n')
                result.close()

            tm_file.write('\n')

            #tm_file.write('\n\n')
            tm_file.write('if count_fail > 0:\n')
            tm_file.write('    SCHEAP.DummyMasterRvc_SetTMFail("dummy_master")\n')
            tm_file.write('    SCHEAP.sc_start(10000)\n')
            tm_file.write('else:\n')
            tm_file.write('    SCHEAP.DummyMasterRvc_SetTMPass("dummy_master")\n')
            tm_file.write('    SCHEAP.sc_start(10000)\n')
                                                
            tm_file.close()
        
            #Finish gen pattern
            print(tm_name)
        
tm_list.close()


print("********************")
print("*Finish generate TM*")
print("********************")


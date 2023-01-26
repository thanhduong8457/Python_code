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

f = open("./tm.list") #open particular tm_file
for file in f:
    if "#" not in file:
        file = file.strip()
        if file == "tm_list_04_dmi":
            dir = "004_DMI"
            idx = "004"
        elif file == "tm_list_04_dmi_eco":
            dir = "004_DMI_ECO"
            idx = "004"
        elif file == "tm_list_04_dmi_v4h":
            dir = "004_DMI_v4h"
            idx = "004"
        elif file == "tm_list_05_dmc":
            dir = "005_DMC"
            idx = "005"
        elif file == "tm_list_05_dmc_v4h":
            dir = "005_DMC_v4h"
            idx = "005"
        elif file == "tm_list_06_ari_phuoct":
            dir = "006_ARI_PhuocT"
            idx = "006"
        elif file == "tm_list_06_ari_v4h":
            dir = "006_ARI_v4h"
            idx = "006"
        elif file == "tm_list_06_ari":
            dir = "006_ARI"
            idx = "006"
        elif file == "tm_list_07_dmo":
            dir = "007_DMO"
            idx = "007"
        elif file == "tm_list_07_dmo_v4h":
            dir = "007_DMO_v4h"
            idx = "007"
        elif file == "tm_list_08_dmr_v4h":
            dir = "008_DMR_v4h"
            idx = "008"
        elif file == "tm_list_08_dmr_v4h_cpr":
            dir = "008_DMR_v4h_cpr"
            idx = "008"
        elif file == "tm_list_10_conv_iloop":
            dir = "010_CONV_Iloop"
            idx = "010"
        elif file == "tm_list_10_conv_mixmode":
            dir = "010_CONV_mixmode"
            idx = "010"
        elif file == "tm_list_11_prefcnt":
            dir = "011_PERFCNT"
            idx = "011"
        elif file == "tm_list_12_dmd":
            dir = "012_DMD"
            idx = "012"
        elif file == "tm_list_13_registerdb":
            dir = "013_RegisterDB"
            idx = "013"   
        
        tm_list = open("./%s" %file) #get TM path
        for tm in tm_list:
            if "#" not in tm:
                tm_path = tm.strip()
                tm_name = "tp03" + "_" + idx + "_" + re.findall('.*/(.+?)$', tm)[0] #name of output file
                tm_name = tm_name.strip()

                if not os.path.isdir("./input/3_Operation/%s/%s" %(dir, tm_name)):
                    os.mkdir("./input/3_Operation/%s/%s" %(dir, tm_name))



                #TM GENERATION
                if not os.path.isfile("../%s/test.json" %tm_path) and os.path.isfile("../%s/test.json.tar.bz2" %tm_path):
                    tar = tarfile.open("../%s/test.json.tar.bz2" %tm_path, "r:bz2")  
                    tar.extractall("../%s/" %tm_path)
                    tar.close()
                    
                if not os.path.isfile("../%s/test.json" %tm_path) and os.path.isfile("../%s/test.json.tar.gz" %tm_path):
                    tar = tarfile.open("../%s/test.json.tar.gz" %tm_path, "r:gz")
                    tar.extractall("../%s/" %tm_path)
                    tar.close()
                
                with open("../%s/test.json" %tm_path) as input:
                    tm_file = open("./python_pat/%s/%s.py" %(dir, tm_name), "w")
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
                    dmai_1_list_init = []
                    dmai_2_list_init = []
                    dma3dc_0_list_init = []
                    dma3dc_1_list_init = []
                    dmao_0_list_init = []
                    dmao_1_list_init = []
                    dmardesa_list_init = []

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
                                # elif (element["name"] == "DMARDESA"):
                                #     channel_size = int(mod["size"],16)
                                #     num_data_channel = channel_size >> 2                                    
                                #     data_init = mod["init"]["fill_u32"]
                                #     init_array = []
                                #     for i in range(num_data_channel):
                                #         init_array.append(data_init)
                                #     data_init_array = str(init_array).replace('\'','')
                                #     data_init_array = str(data_init_array).replace('u','')
                                #     data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMARDESA"):
                                    dmardesa_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dmardesa_list = str(dmardesa_list_init).replace('u','')
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
                                elif (element["name"] == "DMAI_1"):
                                    dmai_1_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dmai_1_list = str(dmai_1_list_init).replace('u','')
                                    data_init = mod["init"]["data_u32"]
                                    data_init_array = str(data_init).replace('\'','')
                                    data_init_array = str(data_init_array).replace('u','')
                                    data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMAI_2"):
                                    dmai_2_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dmai_2_list = str(dmai_2_list_init).replace('u','')
                                    data_init = mod["init"]["data_u32"]
                                    data_init_array = str(data_init).replace('\'','')
                                    data_init_array = str(data_init_array).replace('u','')
                                    data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMA3DC_0"):
                                    dma3dc_0_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dma3dc_0_list = str(dma3dc_0_list_init).replace('u','')
                                    data_init = mod["init"]["data_u32"]
                                    data_init_array = str(data_init).replace('\'','')
                                    data_init_array = str(data_init_array).replace('u','')
                                    data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMA3DC_1"):
                                    dma3dc_1_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dma3dc_1_list = str(dma3dc_1_list_init).replace('u','')
                                    data_init = mod["init"]["data_u32"]
                                    data_init_array = str(data_init).replace('\'','')
                                    data_init_array = str(data_init_array).replace('u','')
                                    data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMAO_0"):
                                    dmao_0_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dmao_0_list = str(dmao_0_list_init).replace('u','')
                                    # data_init = mod["init"]["data_u8"]
                                    # data_init_array = str(data_init).replace('\'','')
                                    data_init_array = str(data_init_array).replace('u','')
                                    data_file.write('%s = %s\n' %(mod["name"], data_init_array) )
                                elif (element["name"] == "DMAO_1"):
                                    dmao_1_list_init.append(["%s.txt" %mod["name"],mod["offset"]])
                                    dmao_1_list = str(dmao_1_list_init).replace('u','')
                                    # data_init = mod["init"]["data_u8"]
                                    # data_init_array = str(data_init).replace('\'','')
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
                            with open("../%s/set_mem.txt" %tm_path) as des_mem:
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
                                            start_x = x.find(";HuyTruong") + 16
                                            end_x = x.find(";HuyTruong") + 27
                                            addr = x[start_x:end_x]
                                            init_array.append(addr)
                                        elif x.find("DCD") > 0:
                                            start_x = x.find("DCD") + 4
                                            #end_x = x.find(";")# + 1
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
                            elif (mod_name == "DMA3DC") and (element["sections"] != []):
                                tm_file.write('dma3dc_list = %s\n' %dma3dc_list)
                            elif (mod_name == "DMAI_1"):
                                tm_file.write('dmai_1_list = %s\n' %dmai_1_list)
                            elif (mod_name == "DMAI_2"):
                                tm_file.write('dmai_2_list = %s\n' %dmai_2_list)
                            elif (mod_name == "DMA3DC_0"):
                                tm_file.write('dma3dc_0_list = %s\n' %dma3dc_0_list)
                            elif (mod_name == "DMA3DC_1"):
                                tm_file.write('dma3dc_1_list = %s\n' %dma3dc_1_list)
                            elif mod_name == "DMAO":
                                tm_file.write('dmao_list = %s\n' %dmao_list)
                            elif mod_name == "DMAO_0":
                                tm_file.write('dmao_0_list = %s\n' %dmao_0_list)
                            elif mod_name == "DMAO_1":
                                tm_file.write('dmao_1_list = %s\n' %dmao_1_list)
                            elif mod_name == "DUMPAREA":
                                tm_file.write('dumparea_list = %s\n' %dumparea_list)
                            elif mod_name == "DMARDESA":
                                tm_file.write('dmardesa_list = %s\n' %dmardesa_list)
                            elif mod_name == "DMARF":
                                tm_file.write('dmarf_list = %s\n' %dmarf_list)

                            if (element["sections"] != []):
                                tm_file.write('for i in range(len(%s)):\n' %list_name)
                                tm_file.write('\tfile_handle = open(input_path + %s[i][0], "r")\n' %list_name)
                                tm_file.write('\tdata = re.findall("0x\w+", file_handle.read())\n')
                                tm_file.write('\tdata = [int(x, 16) for x in data]\n')
                                tm_file.write('\tbuffer = ConvertWordArrayToHexString(data, True)\n')
                                tm_file.write('\tSCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s + int(%s[i][1], 16), buffer)\n' %(mem_area_name, list_name))
                                tm_file.write('\tSCHEAP.sc_start(10)\n')
                                tm_file.write('\tfile_handle.close()\n')
                            tm_file.write('\n')
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
                    
                    tm_file.write('# Active module setting\n')  
                    with open("../%s/set_reg.txt" %tm_path) as set_reg_data:
                        if ("IOW IMP_CNN_BASE + 0x0808, 0x00000001") in set_reg_data.read():
                            tm_file.write('SCHEAP.IMP_CNN_WriteHiddenRegister("imp_cnn", iodef.IMP_CNN_BASE + 0x0808, 0x00000001)\n')
                            tm_file.write('SCHEAP.sc_start(10)\n')
                            tm_file.write('\n')
                    set_reg_data.close()
                                                        
                    tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD,iodef.REG_IMP_CNN_SACL, 0x4, 0x01000000, 0x0, 0x0)\n' )
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD,iodef.REG_IMP_CNN_SCLP, 0x4, 0x00000001, 0x0, 0x0)\n' )
                    tm_file.write('SCHEAP.sc_start(100000)\n')
                    tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, 0x00040000, 0x0, 0x0)\n')
                    tm_file.write('SCHEAP.sc_start(10)\n')
                    tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", 14) == 1):\n' )
                    tm_file.write('    SCHEAP.sc_start(100000)\n')
                    tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, 0x00040000, 0x0, 0x0)\n')
                    tm_file.write('    SCHEAP.sc_start(10)\n')
                    #if tm_path == "07_DMO/dmolength_spmcfast_128x4095":
                    #    tm_file.write('SCHEAP.sc_start(1000000000)\n')
                    #else:
                    #    tm_file.write('SCHEAP.sc_start(1000000)\n')
                    tm_file.write('\n')
                
                    tm_file.write('## Dump DMAO area\n')
                    tm_file.write('count_fail = 0\n')
                    if (dir == "08_DMR_random") or (dir == "08_DMR_SPMC"):
                        pass
                    else: #Others use DMO data
                        if os.path.isfile("../%s/result.txt.l_" %tm_path):
                            result = open("../%s/result.txt.l_" %tm_path)
                        else:    
                            result = open("../%s/result.txt.l" %tm_path)
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
                                        temp = 0
                                        # for y in range(0, num_data):
                                        #     line = result.readline()
                                        #     lower_data = line[9:].strip().replace(' ','').replace('\n','').lower()
                                        #     s += lower_data
                                        for line in result:
                                            if line[0] == '6':
                                                lower_data = line[9:].strip().replace(' ','').replace('\n','').lower()
                                                s += lower_data
                                                temp += 1
                                                if temp == num_data:
                                                    break
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
                                        tm_file.write('#    print("channel %s is fail:")\n' %name_ch)
                                        tm_file.write('#    print("exp_result_ch: %s" %exp_result_ch)\n')
                                        tm_file.write('#    print("result_ch: %s" %result_ch)\n')
                                        tm_file.write('\n')
                        result.close()
    
                    tm_file.write('\n')
                    #check output of DMARF operation
                    if idx == "008":
                        with open("../%s/set_reg.txt" %tm_path) as dmr_out:
                            lut_data_array = []
                            wb_data_array = []
                            wb_addr_array = []
                            i = 0
                            for line in dmr_out:
                                if ("IOR     IMP_CNN_BASE") in line:
                                    if line.find("+ 0x00007") > 0: ##LUT buffer
                                        #get base_addr
                                        start_addr = line.find("0x")
                                        end_addr = start_addr + 10
                                        lut_base_addr = "0x7100"
                                        #if i == 0:   #just get the initial addr
                                        #    lut_base_addr = line[start_addr:end_addr]
                                        #    i += 1
                                        #get expected data    
                                        start_data = end_addr + 2
                                        end_data = start_data + 10
                                        lut_data = line[start_data:end_data]
                                        lut_data_array.append(lut_data)
                                    else:   ##Weight buffer
                                        #get base_addr
                                        start_addr = line.find("0x")
                                        end_addr = start_addr + 10
                                        if (dir == "08_DMR_SPMC"):
                                            wb_addr = line[start_addr:end_addr]
                                            wb_addr_array.append(wb_addr)
                                        else:
                                            wb_base_addr = "0x8000"
                                        #if i == 0:   #just get the initial addr
                                        #    wb_base_addr = line[start_addr:end_addr]
                                        #    i += 1
                                        #get expected data    
                                        start_data = end_addr + 2
                                        end_data = start_data + 10
                                        wb_data = line[start_data:end_data]
                                        wb_data_array.append(wb_data)
                            #dmr_data_out = str(dmr_data_array).replace('\'','')
                            #dmr_data_out = dmr_data_array
                            if len(lut_data_array) > 0:
                                tm_file.write("LUT_BASE_ADDR = %s\n" %lut_base_addr)
                                tm_file.write("LUT_EXP_DATA = %s\n\n" %lut_data_array)
                            if len(wb_data_array) > 0:
                                if (dir == "08_DMR_SPMC"):
                                    tm_file.write("WB_EXP_ADDR = %s\n" %wb_addr_array)
                                else:
                                    tm_file.write("WB_BASE_ADDR = %s\n" %wb_base_addr)
                                tm_file.write("WB_EXP_DATA = %s\n\n" %wb_data_array)
                            #dmr_out.close()
                            if len(lut_data_array) > 0:
                                tm_file.write('n = 0\n')
                                tm_file.write('for i in LUT_EXP_DATA:\n')
                                tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master", iodef.READ_CMD, iodef.IMP_CNN_BASE + LUT_BASE_ADDR + 0x4*n, 0x4, int(LUT_EXP_DATA[n],16), 0x0, 0x0)\n')
                                tm_file.write('    SCHEAP.sc_start(50)\n')
                                tm_file.write('    SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", int(LUT_EXP_DATA[n],16) )\n')
                                tm_file.write('    SCHEAP.sc_start(50)\n')
                                tm_file.write('    n += 1\n\n')
                            if len(wb_data_array) > 0:
                                tm_file.write('n = 0\n')
                                tm_file.write('for i in WB_EXP_DATA:\n')
                                if (dir == "08_DMR_SPMC"):
                                    tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master", iodef.READ_CMD, iodef.IMP_CNN_BASE + int(WB_EXP_ADDR[n],16), 0x4, int(WB_EXP_DATA[n],16), 0x0, 0x0)\n')
                                else:
                                    tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master", iodef.READ_CMD, iodef.IMP_CNN_BASE + WB_BASE_ADDR + 0x4*n, 0x4, int(WB_EXP_DATA[n],16), 0x0, 0x0)\n')
                                tm_file.write('    SCHEAP.sc_start(50)\n')
                                tm_file.write('    SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", int(WB_EXP_DATA[n],16) )\n')
                                tm_file.write('    SCHEAP.sc_start(50)\n')
                                tm_file.write('    n += 1\n\n')
                                        
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
f.close()

print("********************")
print("*Finish generate TM*")
print("********************")


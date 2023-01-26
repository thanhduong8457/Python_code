#!/usr/bin/python

import os
import json
import sys
import binascii
import re
import os.path
#import tarfile
from gen_operation_tm_func import *
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
        # if file == "tm_list_10_conv_iloop":
        #     dir = "010_CONV_Iloop"
        #     idx = "010"
        if file == "tm_list_10_conv_mixmode":
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
        elif file == "tm_list_14_multi_layer":
            dir = "014_Multi_Layer"
            idx = "014"

        tm_list = open("./%s" %file) #get TM path
        for tm in tm_list:
            if "#" not in tm:
                tm_path = tm.strip()
                tm_name = "tp03" + "_" + idx + "_" + re.findall('.*/(.+?)$', tm)[0] #name of output file
                tm_name = tm_name.strip()

                if not os.path.isdir("./input/3_Operation/%s/%s" %(dir, tm_name)):
                    os.mkdir("./input/3_Operation/%s/%s" %(dir, tm_name))

                #TM GENERATION
                with open("../%s/set_mem.txt" %tm_path) as set_mem:
                    tm_file = open("./python_pat/%s/%s.py" %(dir,tm_name), "w")
                    tm_file.write('\n')
                    tm_file.write('###############################\n')
                    tm_file.write('# TM : %s  \n' %tm_path)
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
                    read_set_mem = set_mem.read()
                    
                    #Descriptor
                    start = read_set_mem.find(';   Descriptor List')
                    end = read_set_mem.find('END', start)
                    descriptor_data = read_set_mem[start:end]
                    init_array = []
                    with open ("tmp","w") as f_tmp:
                        f_tmp.write(descriptor_data)
                    with open ("tmp","r") as f_tmp:
                        for x in f_tmp:
                            if x.find(";DCD") > 0:
                                continue                                        
                            elif x.find(";HuyTruong") >= 0:
                                continue
                                # start_x = x.find(";HuyTruong") + 16
                                # end_x = x.find(";HuyTruong") + 27
                                # addr = x[start_x:end_x]
                                # init_array.append(addr)
                            elif x.find("DCD") > 0:
                                start_x = x.find("DCD") + 4
                                end_x = start_x + 10
                                addr = x[start_x:end_x]
                                init_array.append(addr)
                    if os.path.exists("tmp"):
                        os.remove("tmp")
                    data_init_array = str(init_array).replace('\'','')
                    tm_file.write('Descriptor = %s\n' %data_init_array)
                    tm_file.write('\n')
                    
                    dmai_list = []
                    dma3dc_list = []
                    dmao_list = []
                    dmard_list = []
                    dumparea_list = []
                    input_path = "./input/3_Operation/" + dir + "/" + tm_name

                    #DMARF
                    gen_init_data("DMA.*F", input_path, read_set_mem)

                    #DMAI
                    gen_init_data("DMA.*I", input_path, read_set_mem)

                    #DMA3DC
                    gen_init_data("DMA.*3DC", input_path, read_set_mem)
                    
                    #DMAO
                    gen_init_data("DMA.*O", input_path, read_set_mem)
                    
                    #DMARD
                    gen_init_data("DMA.*D", input_path, read_set_mem)
                    
                    #DUMPAREA for DMARD
                    gen_init_data("DUMPAREA", input_path, read_set_mem)

                    tm_file.write('input_path = "../../../../linux/pat/input/3_Operation/%s/%s/"\n' %(dir, tm_name))
                    tm_file.write('# SET MEMORY AREA\n')
                    cl_size = ""
                    dmai_size = ""
                    dma3dc_size = ""
                    dmao_size = ""

                    # if os.path.isfile("../%s/do_json.h_iloop" %tm_path):
                    #     pre, ext = os.path.splitext("do_json.h_iloop")
                    #     os.rename("do_json.h_iloop", pre + '.h')
                    # if os.path.isfile("../%s/do_json.h" %tm_path):
                    #     with open("../%s/do_json.h" %tm_path) as size:
                    #         read_size = size.read()
                    #         cl_size = re.findall('(cl_size).*(0x\w+)', read_size)
                    #         dmai_size = re.findall('(dmaisize).*(0x\w+)', read_size)
                    #         dma3dc_size = re.findall('(dma3dcsize).*(0x\w+)', read_size)
                    #         dmao_size = re.findall('(dmaosize).*(0x\w+)', read_size)

                    # with open("../%s/area.txt" %tm_path) as area:
                    #     #print(cl_size)
                    #     #print(dmai_size)
                    #     #print(dma3dc_size)
                    #     #print(dmao_size)
                    #     mem_area = area.read()
                    #     mem_area_descriptor = re.findall('(Descriptor).*(0x\w{8})', mem_area)
                    #     mem_area_dmai = re.findall('(DMA.*I\w+).*(0x\w{8})', mem_area)
                    #     mem_area_dma3dc = re.findall('(DMA.*3DC\w+).*(0x\w{8})', mem_area)
                    #     mem_area_dmao = re.findall('(DMA.*O\w+).*(0x\w{8})', mem_area)
                    #     mem_area_dmarf = re.findall('(DMA.*F\w+).*(0x\w{8})', mem_area)
                    #     mem_area_dmard = re.findall('(DMA.*RD\w+).*(0x\w{8})', mem_area)
                    #     mem_area_dumparea = re.findall('(DUMPAREA.*\w+).*(0x\w{8})', mem_area)
                    #     #print(mem_area_descriptor)
                    #     # print(mem_area_dmai)
                    #     # print(mem_area_dma3dc)
                    #     # print(mem_area_dmao)
                    #     # Descriptor memory area
                    #     mod_name = "Descriptor"
                    #     mem_base = mem_area_descriptor[0][1]
                    #     size_str = cl_size[0][1]
                    #     if ('cl_size = 0x10000 * 4' in read_size) :
                    #         size_str = '0x40000'
                    #     #print(size_str)
                    #     mem_area_name = "CL_MEMORY_BASE"
                    #     mem_size_name = "CL_MEMORY_SIZE"
                    #     tm_file.write('# %s memory area\n' %mod_name)
                    #     tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
                    #     tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
                    #     tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
                    #     tm_file.write('SCHEAP.sc_start(10)\n')
                        
                    #     tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mod_name)
                    #     tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %(mem_area_name) )
                    #     tm_file.write('SCHEAP.sc_start(10)\n')
                    #     tm_file.write('\n')
                        
                    #     dmarf_size = [["DMARF","0x00040000"]]
                    #     #DMARDESA memory area
                    #     if not mem_area_dmarf == []:
                    #         set_mem_write("DMARF", mem_area_dmarf, dmarf_size, tm_file)

                    #     #DMAI memory area
                    #     set_mem_write("DMAI", mem_area_dmai, dmai_size, tm_file)
                        
                    #     #DMA3DC memory area
                    #     set_mem_write("DMA3DC", mem_area_dma3dc, dma3dc_size, tm_file)

                    #     dmard_size = [["DMARD","0x00000800"]]
                    #     #DMARDESA memory area
                    #     if not mem_area_dmard == []:
                    #         set_mem_write("DMARDESA", mem_area_dmard, dmard_size, tm_file)
                    #         # mod_name = "DMARDESA00"
                    #         # mem_base = mem_area_dmard[0][1]
                    #         # size_str = "0x00000800"
                    #         # mem_area_name = "DMARDESA_MEMORY_BASE"
                    #         # mem_size_name = "DMARDESA_MEMORY_SIZE"
                    #         # tm_file.write('# %s memory area\n' %mod_name)
                    #         # tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
                    #         # tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
                    #         # tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
                    #         # tm_file.write('SCHEAP.sc_start(10)\n')
                    #         # # for i in range(len(mem_area_dmard)):        
                    #         # #     tm_file.write('## channel %s ##\n' %mem_area_dmard[i][0])
                    #         # #     tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mem_area_dmard[i][0])
                    #         # #     tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %mem_area_dmard[i][1] )
                    #         # #     tm_file.write('SCHEAP.sc_start(10)\n')
                    #         # # tm_file.write('\n')
                    #         # for i in range(len(mem_area_dmard)):
                    #         #     dmard_list.append(["%s.txt" %mem_area_dmard[i][0], mem_area_dmard[i][1]])
                    #         #     # tm_file.write('## channel %s ##\n' %mem_area_dmai[i][0])
                    #         #     # tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mem_area_dmai[i][0])
                    #         #     # tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %mem_area_dmai[i][1] )
                    #         #     # tm_file.write('SCHEAP.sc_start(10)\n')
                    #         # tm_file.write('dmard_list = %s\n' %dmard_list)
                    #         # tm_file.write('for i in range(len(dmard_list)):\n')
                    #         # tm_file.write('\tfile_handle = open(input_path + dmard_list[i][0], "r")\n')
                    #         # tm_file.write('\tdata = re.findall("0x\w+", file_handle.read())\n')
                    #         # tm_file.write('\tdata = [int(x, 16) for x in data]\n')
                    #         # tm_file.write('\tbuffer = ConvertWordArrayToHexString(data, True)\n')
                    #         # tm_file.write('\tSCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", int(dmard_list[i][1], 16), buffer)\n')
                    #         # tm_file.write('\tSCHEAP.sc_start(10)\n')
                    #         # tm_file.write('\tfile_handle.close()\n')
                    #         # tm_file.write('\n')

                    #     #DMAO memory area
                    #     set_mem_write("DMAO", mem_area_dmao, dmao_size, tm_file)
                    #     # mod_name = "DMAO"
                    #     # mem_base = mem_area_dmao[0][1]
                    #     # size_str = dmao_size[0][1]
                    #     # mem_area_name = "DMAO_MEMORY_BASE"
                    #     # mem_size_name = "DMAO_MEMORY_SIZE"
                    #     # tm_file.write('# %s memory area\n' %mod_name)
                    #     # tm_file.write('%s = %s\n' %(mem_area_name, mem_base) )
                    #     # tm_file.write('%s = %s\n' %(mem_size_name, size_str) )
                    #     # tm_file.write('SCHEAP.DummyPeripheralRvc_CreateMemoryArea("dummy_peripheral", %s, %s)\n' %(mem_area_name, mem_size_name) )
                    #     # tm_file.write('SCHEAP.sc_start(10)\n')        

                    #     # for i in range(len(mem_area_dmao)):
                    #     #     dmao_list.append(["%s.txt" %mem_area_dmao[i][0], mem_area_dmao[i][1]])
                    #     #     # tm_file.write('## channel %s ##\n' %mem_area_dmai[i][0])
                    #     #     # tm_file.write('buffer = ConvertWordArrayToHexString(%s, True)\n' %mem_area_dmai[i][0])
                    #     #     # tm_file.write('SCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", %s, buffer)\n' %mem_area_dmai[i][1] )
                    #     #     # tm_file.write('SCHEAP.sc_start(10)\n')
                    #     # tm_file.write('dmao_list = %s\n' %dmao_list)
                    #     # tm_file.write('for i in range(len(dmao_list)):\n')
                    #     # tm_file.write('\tfile_handle = open(input_path + dmao_list[i][0], "r")\n')
                    #     # tm_file.write('\tdata = re.findall("0x\w+", file_handle.read())\n')
                    #     # tm_file.write('\tdata = [int(x, 16) for x in data]\n')
                    #     # tm_file.write('\tbuffer = ConvertWordArrayToHexString(data, True)\n')
                    #     # tm_file.write('\tSCHEAP.DummyPeripheralRvc_SetMemory("dummy_peripheral", int(dmao_list[i][1], 16), buffer)\n')
                    #     # tm_file.write('\tSCHEAP.sc_start(10)\n')
                    #     # tm_file.write('\tfile_handle.close()\n')
                    #     # tm_file.write('\n')

                    #     dumparea_size = [["DUMPAREA","0x00040000"]]
                    #     #DUMPAREA memory area
                    #     if not mem_area_dumparea == []:
                    #         set_mem_write("DUMPAREA", mem_area_dumparea, dumparea_size, tm_file)
                                              
                    #     tm_file.write('# Set clock\n')
                    #     tm_file.write('SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral", "clk", 800000000)\n')
                    #     tm_file.write('SCHEAP.sc_start(10)\n')
                    #     tm_file.write('\n')
                    #     tm_file.write('# De-assert reset\n')
                    #     tm_file.write('SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral", "preset", 0)\n')
                    #     tm_file.write('SCHEAP.sc_start(10)\n')
                    #     tm_file.write('\n')
                                    
                    #     tm_file.write('#################\n')
                    #     tm_file.write('# RUNS TEST     #\n')
                    #     tm_file.write('#################\n')
                    #     tm_file.write('\n')

                    #     # tm_file.write('# Active module setting\n')
                        
                    #     # with open("../%s/set_reg.txt" %tm_path) as set_reg_data:
                    #     #     if ("IOW IMP_CNN_BASE + 0x0808") in set_reg_data.read():
                    #     #         tm_file.write('SCHEAP.IMP_CNN_WriteHiddenRegister("imp_cnn", iodef.IMP_CNN_BASE + 0x0808, 0x00000001)\n')
                    #     #         tm_file.write('SCHEAP.sc_start(10)\n')
                    #     #         tm_file.write('\n')
                    #     # set_reg_data.close()
                        
                    #     # tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD,iodef.REG_IMP_CNN_SACL, 0x4, 0x01000000, 0x0, 0x0)\n' )
                    #     # tm_file.write('SCHEAP.sc_start(10)\n')
                    #     # tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD,iodef.REG_IMP_CNN_SCLP, 0x4, 0x00000001, 0x0, 0x0)\n' )
                    #     # tm_file.write('SCHEAP.sc_start(100000)\n')
                    #     # tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, 0x00040000, 0x0, 0x0)\n')
                    #     # tm_file.write('SCHEAP.sc_start(10)\n')
                    #     # tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", 14) == 1):\n' )
                    #     # tm_file.write('    SCHEAP.sc_start(100000)\n')
                    #     # tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, 0x00040000, 0x0, 0x0)\n')
                    #     # tm_file.write('    SCHEAP.sc_start(10)\n')
                    #     #if tm_path == "07_DMO/dmolength_spmcfast_128x4095":
                    #     #    tm_file.write('SCHEAP.sc_start(1000000000)\n')
                    #     #else:
                    #     #    tm_file.write('SCHEAP.sc_start(1000000)\n')
                    #     # tm_file.write('\n')
                    #     HiddenReg = ['IMP_CNN_BASE + 0x00000240', 'IMP_CNN_BASE + 0x00000244', 'IMP_CNN_BASE + 0x00000248', 'IMP_CNN_BASE + 0x0000024c', 'IMP_CNN_BASE + 0x00000250', 'IMP_CNN_BASE + 0x00000254', 'IMP_CNN_BASE + 0x00000258', 'IMP_CNN_BASE + 0x0000025c', 'IMP_CNN_BASE + 0x00000260', 'IMP_CNN_BASE + 0x00000264', 'IMP_CNN_BASE + 0x00000800', 'IMP_CNN_BASE + 0x00000804', 'IMP_CNN_BASE + 0x00000808', 'IMP_CNN_BASE + 0x00000810', 'IMP_CNN_BASE + 0x00000814', 'IMP_CNN_BASE + 0x0000081C', 'IMP_CNN_BASE + 0x00000820', 'IMP_CNN_BASE + 0x00000830', 'IMP_CNN_BASE + 0x00000834', 'IMP_CNN_BASE + 0x00000838', 'IMP_CNN_BASE + 0x0000083C', 'IMP_CNN_BASE + 0x00000920', 'IMP_CNN_BASE + 0x00000924', 'IMP_CNN_BASE + 0x00000928', 'IMP_CNN_BASE + 0x0000092c', 'IMP_CNN_BASE + 0x00000940']
                    #     with open("../%s/set_reg.txt" %tm_path) as reg_info: #get data of reg setting
                    #         tm_file.write('# Active module setting\n')
                    #         for x in reg_info:
                    #             if x.find(";IOW") > 0:
                    #                 continue
                    #             elif x.find(";IOR") > 0:
                    #                 continue
                    #             elif x.find(";HuyTruong") >= 0:
                    #                 continue
                    #             elif x.find("IOW") > 0:
                    #                 #get base addr of regs setting
                    #                 if x.find("IMPCNN_SRC") > 0:
                    #                     start_reg = x.find("IMPCNN_SRC")
                    #                     reg_addr = "0xFF9E0018"
                    #                 elif x.find("IMPCNN_SACL") > 0:
                    #                     start_reg = x.find("IMPCNN_SACL")
                    #                     reg_addr = "0xFF9E0104"
                    #                 elif x.find("IMPCNN_SCLP") > 0:
                    #                     start_reg = x.find("IMPCNN_SCLP")
                    #                     reg_addr = "0xFF9E0108"
                    #                 elif x.find("IMP_CNN_BASE") > 0:
                    #                     reg_info = re.findall('(IMP_CNN_BASE.\+.\w+).\s*(\w+)', x)
                    #                     start_reg = x.find(reg_info[0][1])
                    #                     reg_addr = reg_info[0][0]
                    #                 else:
                    #                     start_reg = x.find("0x")
                    #                     end_reg = start_reg + 10
                    #                     reg_addr = x[start_reg:end_reg]                        
                    #                     reg_addr=re.sub('0xFFAA','0xFF9E',reg_addr)                        
                    #                 #get data to allocate regs
                    #                 start_data = x.find("0x",start_reg+2)
                    #                 end_data = start_data + 10
                    #                 wdata = x[start_data:end_data]
                    #                 if "IMP_CNN_BASE" in x:
                    #                     wdata = reg_info[0][1]
                    #                 if (reg_addr == "0xFF9E0808") or ("0x0808" in reg_addr):
                    #                     tm_file.write('SCHEAP.IMP_CNN_WriteHiddenRegister("imp_cnn", iodef.IMP_CNN_BASE + 0x0808, 0x00000001)\n')
                    #                     #tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master,iodef.WRITE_CMD,0xFF9E0808, 0x4,0x00000001, 0x0, 0x0)\n')
                    #                 elif "IMP_CNN_BASE" in x:
                    #                     tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD, iodef.%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                    #                 else:
                    #                     tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.WRITE_CMD, %s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, wdata) )
                    #                 if (reg_addr == "0xFF9E0108") or ("0x0108" in x):
                    #                     tm_file.write('SCHEAP.sc_start(1000000)\n')
                    #                 else:
                    #                     tm_file.write('SCHEAP.sc_start(10)\n')                            
                    #             elif x.find(" IOR") > 0:
                    #                 #get base addr of regs setting
                    #                 if x.find("IMP_CNN_BASE") > 0:
                    #                     reg_info = re.findall('(IMP_CNN_BASE.\+.\w+).\s*(\w+)', x)
                    #                     start_reg = x.find(reg_info[0][1])
                    #                     reg_addr = reg_info[0][0]
                    #                 else:
                    #                     start_reg = x.find("0x")
                    #                     end_reg = start_reg + 10
                    #                     reg_addr = x[start_reg:end_reg]
                    #                     reg_addr=re.sub('0xFFAA','0xFF9E',reg_addr) 
                    #                     reg_addr=re.sub('0xffaa','0xFF9E',reg_addr) 
                    #                 #get data to allocate regs
                    #                 start_data = x.find("0x",start_reg+2)
                    #                 end_data = start_data + 10
                    #                 rdata = x[start_data:end_data]
                    #                 if reg_addr in HiddenReg:
                    #                     if "IMP_CNN_BASE" in x:
                    #                         rdata = reg_info[0][1] 
                    #                         tm_file.write('ReadHidReg_Result = SCHEAP.IMP_CNN_ReadHiddenRegister("imp_cnn", iodef.%s)\n' %(reg_addr))
                    #                         tm_file.write('SCHEAP.sc_start(10)\n')
                    #                         tm_file.write('if (ReadHidReg_Result != %s):\n' %(rdata))
                    #                         tm_file.write('\tprint("Wrong value of Hidden register iodef.{}, Read data: %s, Expected: %s" %(hex(ReadHidReg_Result),hex({})))\n'.format(reg_addr, rdata))
                    #                         tm_file.write('\tSCHEAP.DummyMasterRvc_SetTMFail("dummy_master")\n')
                    #                         tm_file.write('\tSCHEAP.sc_start(1000)\n')
                    #                 else:
                    #                     if "IMP_CNN_BASE" in x:
                    #                         rdata = reg_info[0][1]                                    
                    #                         tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD, iodef.%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, rdata) )
                    #                     else:
                    #                         tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,%s, 0x4, %s, 0x0, 0x0)\n' %(reg_addr, rdata) )
                    #                     tm_file.write('SCHEAP.sc_start(10)\n')
                    #                     tm_file.write('SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s)\n' %rdata)
                    #                     tm_file.write('SCHEAP.sc_start(10)\n')
                    #             elif (x.find("IMP_MSK_CHECK IMPCNN_SR") > 0):
                    #                 sr_data = re.findall('(0x\w{8}).\s*(\w+).\s*(\w+).\s*(\w+)',x)
                    #                 tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    #                 tm_file.write('SCHEAP.sc_start(10)\n')
                    #                 tm_file.write('MaskCheck = SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s, %s)\n' %(sr_data[0][0], sr_data[0][1]))
                    #                 tm_file.write('SCHEAP.sc_start(10)\n')
                    #                 if sr_data[0][2] == 'EQ':
                    #                     tm_file.write('while (MaskCheck == 1):\n')
                    #                 if sr_data[0][2] == 'NEQ':
                    #                     tm_file.write('while (MaskCheck != 1):\n')
                    #                 tm_file.write('    SCHEAP.sc_start(100000)\n')
                    #                 tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    #                 tm_file.write('    SCHEAP.sc_start(10)\n')
                    #                 tm_file.write('    MaskCheck = SCHEAP.DummyMasterRvc_CheckReceivedData32("dummy_master", %s, %s)\n' %(sr_data[0][0], sr_data[0][1]))
                    #                 tm_file.write('    SCHEAP.sc_start(10)\n')  
                    #             elif(x.find("IMPSC_CHECK0 IMP_CNN_BASE") > 0):
                    #                 sr_data = re.findall('(0x\w{8}).\s*(\w+).\s*(\w+)',x)
                    #                 bit_check = int(sr_data[0][0],16)
                    #                 i = 0
                    #                 while (bit_check >> i != 1):
                    #                     if (bit_check == 0x0):
                    #                       break
                    #                     i += 1
                    #                 tm_file.write('SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    #                 tm_file.write('SCHEAP.sc_start(10)\n')
                    #                 # if "0x00004000, EQ, 0" in x:
                    #                 #     tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", 14) == 1):\n')
                    #                 if sr_data[0][1] == 'EQ':
                    #                     tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", %d) == 1):\n' %i)
                    #                 elif sr_data[0][1] == 'NEQ':
                    #                     tm_file.write('while (SCHEAP.DummyMasterRvc_ReadBitReg("dummy_master", %d) != 1):\n' %i)
                    #                 tm_file.write('    SCHEAP.sc_start(100000)\n')
                    #                 tm_file.write('    SCHEAP.DummyMasterRvc_IssueAXITransaction("dummy_master",iodef.READ_CMD,iodef.REG_IMP_CNN_SR, 0x4, %s, 0x0, 0x0)\n' %sr_data[0][0])
                    #                 tm_file.write('    SCHEAP.sc_start(10)\n')  
                    #         tm_file.write('\n')
                        

                        # if os.path.isfile("../%s/result.txt.l_" %tm_path):
                        #     result = open("../%s/result.txt.l_" %tm_path)
                        # else:    
                        #     result = open("../%s/result.txt.l" %tm_path)                        
                        # read_result = result.read()
                        # tm_file.write('count_fail = 0\n')
                        # if not mem_area_dmard == []:
                        #     tm_file.write('## Dump DMARDESA00 result\n')
                        #     dmard_data = re.findall('\|(DMA.*RD\w+)\|.*\n((\s+DCD\s0x\w+\n)+)',read_set_mem)
                        #     dmard_result = re.findall('(7\w{7}.*)', read_result)
                        #     pre_num_data = 0
                        #     for i in range(len(mem_area_dmard)): 
                        #         offset = mem_area_dmard[i][1]
                        #         size_ch = dmard_data[i][1].count("0x")*4
                        #         name_ch = mem_area_dmard[i][0]
                        #         num_data = size_ch >> 4
                        #         mod_num_data = size_ch%16
                        #         if mod_num_data > 0:
                        #             num_data += 1
                        #         else:
                        #             num_data = num_data

                        #         s = ""            
                        #         for y in range(pre_num_data, pre_num_data + num_data):
                        #             lower_data = re.sub('(7\w{7})','', dmard_result[y])
                        #             lower_data = lower_data.replace(' ','').lower()
                        #             s += lower_data
                        #         exp_data_ch = s
                        #         pre_num_data += num_data

                        #         tm_file.write('base_address = %s\n' %offset )
                        #         tm_file.write('exp_result_ch = "%s"\n' %exp_data_ch)
                        #         tm_file.write('result_ch = ""\n')
                        #         tm_file.write('for y in range (0, %d):\n' %num_data)
                        #         if mod_num_data > 0:
                        #             tm_file.write('    if y == %d:\n' %(num_data-1))
                        #             tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), %d)\n' %mod_num_data)
                        #             tm_file.write('    else:\n')
                        #             tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                        #         else:
                        #             tm_file.write('    buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                        #         tm_file.write('    result_ch = result_ch + binascii.hexlify(buffer) \n')
                        #         tm_file.write('    SCHEAP.sc_start(10)\n')
                        #         #tm_file.write('print("[0x%s]: %s") % (format(base_address, \'08X\'), binascii.hexlify(result_ch))\n')
                        #         tm_file.write('if exp_result_ch == result_ch:\n')
                        #         tm_file.write('    print("#### CHANNEL DATA MATCHING #####")\n')
                        #         tm_file.write('#    print("[0x%s]: %s") % (format(base_address, \'08X\'), result_ch)\n')
                        #         tm_file.write('else:\n')
                        #         tm_file.write('    print("#### CHANNEL DATA MISMATCHED #####")\n')
                        #         tm_file.write('    count_fail += 1\n')
                        #         tm_file.write('    print("channel %s is fail:")\n' %name_ch)
                        #         tm_file.write('#    print("exp_result_ch: %s" %exp_result_ch)\n')
                        #         tm_file.write('#    print("result_ch: %s" %result_ch)\n')
                        #         tm_file.write('\n')
                                
                        # tm_file.write('## Dump DMAO area\n')                        
                        # name = "DMAO"
                        # dmao_data = re.findall('\|(DMA.*O\w+)\|.*\n((\s+DCD\s0x\w+\n)+)',read_set_mem)                        
                        # dmao_result = re.findall('(6\w{7}.*)', read_result)
                        # pre_num_data = 0
                        # for i in range(len(mem_area_dmao)): 
                        #     offset = mem_area_dmao[i][1]
                        #     size_ch = dmao_data[i][1].count("0x")*4
                        #     name_ch = mem_area_dmao[i][0]
                        #     num_data = size_ch >> 4
                        #     mod_num_data = size_ch%16
                        #     if mod_num_data > 0:
                        #         num_data += 1
                        #     else:
                        #         num_data = num_data

                        #     s = ""            
                        #     for y in range(pre_num_data, pre_num_data + num_data):
                        #         lower_data = re.sub('(6\w{7})','',dmao_result[y])
                        #         lower_data = lower_data.replace(' ','').lower()
                        #         s += lower_data
                        #     exp_data_ch = s
                        #     pre_num_data += num_data

                        #     tm_file.write('base_address = %s\n' %offset )
                        #     tm_file.write('exp_result_ch = "%s"\n' %exp_data_ch)
                        #     tm_file.write('result_ch = ""\n')
                        #     tm_file.write('for y in range (0, %d):\n' %num_data)
                        #     if mod_num_data > 0:
                        #         tm_file.write('    if y == %d:\n' %(num_data-1))
                        #         tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), %d)\n' %mod_num_data)
                        #         tm_file.write('    else:\n')
                        #         tm_file.write('        buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                        #     else:
                        #         tm_file.write('    buffer = SCHEAP.DummyPeripheralRvc_GetMemory("dummy_peripheral", base_address + (16 * y), 16)\n')
                        #     tm_file.write('    result_ch = result_ch + binascii.hexlify(buffer) \n')
                        #     tm_file.write('    SCHEAP.sc_start(10)\n')
                        #     #tm_file.write('print("[0x%s]: %s") % (format(base_address, \'08X\'), binascii.hexlify(result_ch))\n')
                        #     tm_file.write('if exp_result_ch == result_ch:\n')
                        #     tm_file.write('    print("#### CHANNEL DATA MATCHING #####")\n')
                        #     tm_file.write('#    print("[0x%s]: %s") % (format(base_address, \'08X\'), result_ch)\n')
                        #     tm_file.write('else:\n')
                        #     tm_file.write('    print("#### CHANNEL DATA MISMATCHED #####")\n')
                        #     tm_file.write('    count_fail += 1\n')
                        #     tm_file.write('    print("channel %s is fail:")\n' %name_ch)
                        #     tm_file.write('#    print("exp_result_ch: %s" %exp_result_ch)\n')
                        #     tm_file.write('#    print("result_ch: %s" %result_ch)\n')
                        #     tm_file.write('\n')
                        
                        # result.close()

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
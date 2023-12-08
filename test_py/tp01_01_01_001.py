import sys
import os
sys.path.append('./')
from iodef import *  # load address define
# from common_func import *
import simmode # indicate simmode is LT/AT
SCHEAP.DummyMasterRvc_SetSimMode("dummy_master", simmode.SIM_MODE)
SCHEAP.setFreq(1000, "MHz")

SCHEAP.DummyPeripheralRvc_EnableDumpMessage("dummy_peripheral", 1)
SCHEAP.DummyMasterRvc_EnableDumpMessage("dummy_master", 1)

SCHEAP.RSW_WRAPPER_MessageLevel("rsw","info|error|warning|fatal")
SCHEAP.RSW_WRAPPER_DumpRegisterRW("rsw","true")
SCHEAP.RSW_WRAPPER_DumpInterrupt("rsw","true")
SCHEAP.RSW_WRAPPER_EnableRegisterMessage("rsw","true")


#*******************************************
#- 1. Set clocks frequency
#*******************************************
SCHEAP.sc_start(10)

SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk",     300000000) #Set clk 
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_PCLK",    100000000) #Set PCLK
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_PCLK_sec",100000000) #Set PCLK_sec
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_ACLK0",   400000000) #Set clk 
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_ACLK1",    400000000) #Set clk
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx0", 78125000) #Set clk_phy_tx0 2.5Gbps
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx1", 78125000) #Set clk_phy_tx1
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx2", 78125000) #Set clk_phy_tx2
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx3", 78125000) #Set clk_phy_tx3
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx4", 78125000) #Set clk_phy_tx4
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx5", 78125000) #Set clk_phy_tx5
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx6", 78125000) #Set clk_phy_tx6
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx7", 78125000) #Set clk_phy_tx7
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx8", 78125000) #Set clk_phy_tx8
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx9", 78125000) #Set clk_phy_tx9
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx10", 78125000) #Set clk_phy_tx10
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_tx11", 78125000) #Set clk_phy_tx11
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx0", 78125000) #Set clk_phy_rx0
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx1", 78125000) #Set clk_phy_rx1
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx2", 78125000) #Set clk_phy_rx2
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx3", 78125000) #Set clk_phy_rx3
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx4", 78125000) #Set clk_phy_rx4
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx5", 78125000) #Set clk_phy_rx5
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx6", 78125000) #Set clk_phy_rx6
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx7", 78125000) #Set clk_phy_rx7
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx8", 78125000) #Set clk_phy_rx8
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx9", 78125000) #Set clk_phy_rx9
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx10", 78125000) #Set clk_phy_rx10
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_rx11", 78125000) #Set clk_phy_rx11
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_clk_phy_common", 78125000)

#SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","x_apreset_rsw2",0x1)
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_x_apreset",0x1)
SCHEAP.sc_start(20)
#SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","x_apreset_rsw2",0x0)
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_x_apreset",0x0)
SCHEAP.sc_start(20)

#SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","x_apreset_rsw2",0x1)
SCHEAP.DummyPeripheralRvc_SetOutputPort("dummy_peripheral","DP_x_apreset",0x1)
SCHEAP.sc_start(20)
'''#***********************************************************************
#  TESTING_CONTENT: Normal Accessing (W: 8 bits; R: 8/16/32 bits)
#***********************************************************************'''
rsw_reg_ins = RSW_reg()

# read write 32
# read write 32
# read write 32
# read write 32
#*******************************************
# 1. check the initial value
#*******************************************
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET] ,0x4,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL])
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET] ,0x4,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL])
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET] ,0x4,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL])
SCHEAP.sc_start(50)

#*******************************************
# 2. write the value 0xFF with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)  
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x3)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0xFFFFFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x1)
 
#*******************************************
# 3. write the value 0x0 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)

 #*******************************************
# 4. write the value 0x55 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET],0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x1)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0x55555555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x1)

#*******************************************
# 5. write the value 0xAA with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET],0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x2)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET],0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET],0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x4, 0xAAAAAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)


# read write 16
# read write 16
# read write 16
# read write 16
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET] ,0x2,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET] ,0x2,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET] ,0x2,0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)

#*******************************************
# 2. write the value 0xFF with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)  
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0xFFFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
 
#*******************************************
# 3. write the value 0x0 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)

 #*******************************************
# 4. write the value 0x55 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0x5555, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)

#*******************************************
# 5. write the value 0xAA with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x2, 0xAAAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)


# read write 8
# read write 8
# read write 8
# read write 8
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master",0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0) #enable source port1 (ether1)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)

#*******************************************
# 2. write the value 0xFF with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)  
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0xFF, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
 
#*******************************************
# 3. write the value 0x0 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start(50)

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0x0, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)

 #*******************************************
# 4. write the value 0x55 with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0x55, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)

#*******************************************
# 5. write the value 0xAA with each byte 
#*******************************************
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.INIT_VAL], 0x0, 0x0) # reset to initial value

SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0MC'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0,rsw_reg_ins.GWCA_reg['GW0TSCN'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x1, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_IssueTransaction("dummy_master", 0x0, rsw_reg_ins.GWCA_reg['GW0COC'][rsw_reg_ins.OFFSET], 0x1, 0xAA, 0x0, 0x0)
SCHEAP.sc_start (50)
SCHEAP.DummyMasterRvc_ReadReceivedData("dummy_master", 0x0)
 
#***********************************************
#- . SetTMPass
#***********************************************

SCHEAP.sc_start(50)
SCHEAP.DummyMasterRvc_SetTMPass("dummy_master")
SCHEAP.sc_start(50)

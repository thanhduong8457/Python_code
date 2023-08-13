import common

global Fixed_format

Fixed_format = True

def subject_point(Book2, subject):
    my_point = 0
    if subject == "TO":
        if (True == Fixed_format):
            TO_index = 26
        else:
            TO_index = Book2.find_colum_index_with_content("TO")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=TO_index + 1).value
    elif subject == "VA":
        if (True == Fixed_format):
            VA_index = 27
        else:
            VA_index = Book2.find_colum_index_with_content("VA")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=VA_index + 1).value
    elif subject == "LI":
        if (True == Fixed_format):
            LI_index = 28
        else:
            LI_index = Book2.find_colum_index_with_content("LI")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=LI_index + 1).value
    elif subject == "HO":
        if (True == Fixed_format):
            HO_index = 29
        else:
            HO_index = Book2.find_colum_index_with_content("HO")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=HO_index + 1).value
    elif subject == "SI":
        if (True == Fixed_format):
            SI_index = 30
        else:
            SI_index = Book2.find_colum_index_with_content("SI")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=SI_index + 1).value
    elif subject == "SU":
        if (True == Fixed_format):
            SU_index = 31
        else:
            SU_index = Book2.find_colum_index_with_content("SU")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=SU_index + 1).value
    elif subject == "DI":
        if (True == Fixed_format):
            DI_index = 32
        else:
            DI_index = Book2.find_colum_index_with_content("DI")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=DI_index + 1).value
    elif subject == "GDCD":
        if (True == Fixed_format):
            GDCD_index = 33
        else:
            GDCD_index = Book2.find_colum_index_with_content("GDCD")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=GDCD_index + 1).value
    elif subject == "NN":
        if (True == Fixed_format):
            NN_index = 34
        else:
            NN_index = Book2.find_colum_index_with_content("NN")
        my_point = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=NN_index + 1).value

    elif subject == "KVƯT":
        temp_index = 0
        if (True == Fixed_format):
            temp_index = 7
        else:
            temp_index = Book2.find_colum_index_with_content("KVƯT")
        
        cell_value = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=temp_index + 1).value

        if (cell_value == "2NT" or cell_value == "KV2-NT"):
            my_point = 0.5
        elif(cell_value == "1" or cell_value == "KV1"):
            my_point = 0.75
        elif(cell_value == "2" or cell_value == "KV2"):
            my_point = 0.25
        elif(cell_value == "3" or cell_value == "KV3"):
            my_point = 0

    elif subject == "ĐTƯT":
        temp_index = 0
        if (True == Fixed_format):
            temp_index = 6
        else:
            temp_index = Book2.find_colum_index_with_content("ĐTƯT")

        cell_value = Book2.current_sheet.cell(row=Book2.listSheet[Book2.current_sheet.title].index_row, column=temp_index + 1).value

        if (cell_value == "01" or cell_value == "02" or cell_value == "03" or cell_value == "04"):
            my_point = 2
        elif(cell_value == "05" or cell_value == "06" or cell_value == "07"):
            my_point = 1
        else:
            my_point = 0

    if isinstance(my_point, (int, float)):
        return my_point
    else:
        return 0

def caculate_ut_point(Book2, CMND_map1):
    return (subject_point(Book2,"KVƯT") + subject_point(Book2,"ĐTƯT"))
            
def caculate_point(Book2, CMND, major):
    point = 0
    max_point = 0
    max_point_add_gap = 0
    khoi_hight_point = ""
    heso = 1
    sum_of_heso = 0
    for khoi in major.maToHop:
        # print("khoi",khoi.name,"and subject is",khoi.list_subject)
        for each_subject in khoi.list_subject:
            heso = khoi.he_so[each_subject]
            sum_of_heso += heso
            point += subject_point(Book2, each_subject)*heso
            # print("with subject", each_subject,", he so is", heso," and point is", point)

        point = 3 * (point/sum_of_heso)

        if (max_point < point):
            max_point = point
            max_point_add_gap = max_point + khoi.gap_point
            khoi_hight_point = khoi.name
        point = 0
        sum_of_heso = 0
    
    print("in major id",major.major_id,"with khoi",khoi.name,"student id",CMND,"khoi high point is",khoi_hight_point,"max point is", round(max_point, 2))
    return khoi_hight_point, max_point, max_point_add_gap

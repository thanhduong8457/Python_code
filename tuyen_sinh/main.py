##############################################################
# Created by Thanh Duong
##############################################################
import sys
import common
import common_func
import time
start = time.process_time()

global Fixed_format
Fixed_format = True

targets = 100
culumn_khoi_trung_tuyen = 22
culumn_diem = 23
culumn_diem_add_gap = 24

##############################################################
# main function
##############################################################
def main(argv):
    toHop_THTP = common.ExcelHandler("toHop_THTP.xlsx")
    toHop_THTP.chosse_current_sheet('Sheet1')

    # Book1 = common.ExcelHandler("Book1.xlsx")
    # Book1.chosse_current_sheet('Sheet1')

    Book2 = common.ExcelHandler("Book2.xlsx")
    Book2.chosse_current_sheet("Sheet1")

    # new_workbook = openpyxl.Workbook()
    name_new_workbook = "ExampleOutput.xlsx"
    # new_workbook.save(name_new_workbook)
    # print("Excel file", name_new_workbook, "has been created.")
    output_file = common.ExcelHandler(name_new_workbook)

    # ##########################################################
    # # Create a new Workbook and crist sheet contain all majors
    # ##########################################################
    # row_data_header = []
    # for row in Book1.current_sheet.iter_rows(min_row=1, max_row=1, values_only=True):
    #     # Append each cell value to the list
    #     for cell_value in row:
    #         row_data_header.append(cell_value)

    # # print(row_data_header)

    list_id_major = []

    index_maNganh = 0
    if (False == Fixed_format):
        index_maNganh = toHop_THTP.find_colum_index_with_content("maNganh")

    for col in toHop_THTP.current_sheet.iter_rows(2, toHop_THTP.current_sheet.max_row):
        sheet_name = col[index_maNganh].value
        # if sheet_name not in output_file.workbook.sheetnames:
        if sheet_name in output_file.workbook.sheetnames: # delete this line
            if sheet_name not in list_id_major:
                list_id_major.append(sheet_name)
        #     output_file.add_sheet(sheet_name)
        #     output_file.chosse_current_sheet(sheet_name)
        #     column_temp = 1
        #     for temptemp in row_data_header:
        #         cell = output_file.current_sheet.cell(row = 1, column = column_temp)
        #         cell.value = temptemp
        #         column_temp += 1

    # output_file.remove_sheet("Sheet")

    # ##########################################################
    # # start to arange to major
    # ##########################################################

    # ma_nganh_index = Book1.find_colum_index_with_content("Mã ngành")
    # ma_PTXT_index = Book1.find_colum_index_with_content("Mã PTXT")

    # # Book1.print_data_collum(ma_nganh_index)
    # # Book1.print_data_collum(CMND_index)
    
    # for row in Book1.current_sheet.iter_rows(2, Book1.current_sheet.max_row):
    #     sheet_name = row[ma_nganh_index].value
    #     # fill_data = col[CMND_index].value
    #     if (row[ma_PTXT_index].value != '100'):
    #         continue

    #     print("process for", sheet_name)

    #     # list_data = []
    #     # for my_colum in Book1.current_sheet.iter_cols(2, Book1.current_sheet.max_column):
    #     #     list_data.append(row[my_colum].value)

    #     row_data = []
    #     for cell in row[0:]:  # Start from the second column (index 1)
    #         if (cell.value != ''):
    #             row_data.append(cell.value)

    #     if sheet_name in output_file.workbook.sheetnames:
    #         # print(f"Add student with ID number {fill_data} to sheet '{sheet_name}'")
    #         output_file.chosse_current_sheet(sheet_name)
    #         output_file.listSheet[sheet_name].index_row += 1
    #         column_temp = 1
    #         for temptemp in row_data:
    #             cell = output_file.current_sheet.cell(row = output_file.listSheet[sheet_name].index_row, column = column_temp)
    #             cell.value = temptemp
    #             column_temp += 1
    #     else:
    #         print(f"Sheet '{sheet_name}' does not exist in the Excel file.")

    ##########################################################
    # get the list Khoi and its subject contain
    ##########################################################
    list_major = []
    maTohop_index = 2
    mon1_index = 5
    mon2_index = 6
    mon3_index = 7
    maNganh_index = 0
    toHopGoc_index = 3
    heSoM1_index = 8
    heSoM2_index = 9
    heSoM3_index = 10
    gap_point_index = 11
    if (False == Fixed_format):
        maTohop_index = toHop_THTP.find_colum_index_with_content("maTohop")
        mon1_index = toHop_THTP.find_colum_index_with_content("mon1")
        mon2_index = toHop_THTP.find_colum_index_with_content("mon2")
        mon3_index = toHop_THTP.find_colum_index_with_content("mon3")
        maNganh_index = toHop_THTP.find_colum_index_with_content("maNganh")
        toHopGoc_index = toHop_THTP.find_colum_index_with_content("toHopGoc")
        heSoM1_index = toHop_THTP.find_colum_index_with_content("heSoM1")
        heSoM2_index = toHop_THTP.find_colum_index_with_content("heSoM2")
        heSoM3_index = toHop_THTP.find_colum_index_with_content("heSoM3")
        gap_point_index = toHop_THTP.find_colum_index_with_content("gap_point")

    for each_id_major in list_id_major:
        mMajor = common.ClassMajor(each_id_major)
        for row in toHop_THTP.current_sheet.iter_rows(2, toHop_THTP.current_sheet.max_row):
            mIDMajor = row[maNganh_index].value
            if each_id_major != mIDMajor:
                continue 
            # print("processing for",each_id_major)
            mKhoi_value = row[maTohop_index].value
            mClassKhoi = common.ClassKhoi(mKhoi_value)
            mClassKhoi.list_subject.append(row[mon1_index].value) # add mon 1
            mClassKhoi.list_subject.append(row[mon2_index].value) # add mon 2
            mClassKhoi.list_subject.append(row[mon3_index].value) # add mon 3
            mClassKhoi.he_so[row[mon1_index].value] = row[heSoM1_index].value
            mClassKhoi.he_so[row[mon2_index].value] = row[heSoM2_index].value
            mClassKhoi.he_so[row[mon3_index].value] = row[heSoM3_index].value
            mClassKhoi.gap_point = row[gap_point_index].value
            mMajor.add_khoi(mClassKhoi)
            if row[toHopGoc_index].value == "x" or row[toHopGoc_index].value == "X":
                mMajor.update_primary_khoi(mClassKhoi)

        list_major.append(mMajor)
    
    # for mIDMajor in list_major:
    #     mIDMajor.print_info()

    ##########################################################
    # caculate point
    ##########################################################

    Book2.chosse_current_sheet("Sheet1")
    
    CMND_index_map2 = 3
    if (False == Fixed_format):
        CMND_index_map2 = Book2.find_colum_index_with_content("CMND")

    temp_val = 0

    for temp_major in list_major:

        temp_val += 1

        max_point = 0
        max_point_add_gap = 0
        ut_point = 0
        final_point = 0
        khoi_hight_point = ""

        print(temp_major.major_id)

        output_file.chosse_current_sheet(temp_major.major_id)

        CMND_index_map1 = 1
        if (False == Fixed_format):
            CMND_index_map1 = output_file.find_colum_index_with_content("Số CMND")

        for row1_index, row1 in enumerate(output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2):
            cell = output_file.current_sheet.cell(row = 1, column = culumn_khoi_trung_tuyen)
            cell.value = "khoi_trung_tuyen"
            cell = output_file.current_sheet.cell(row = 1, column = culumn_diem)
            cell.value = "final_point"
            cell = output_file.current_sheet.cell(row = 1, column = culumn_diem_add_gap)
            cell.value = "final_point_add_gap"
            CMND_map1 = row1[CMND_index_map1]
            # print(CMND_map1)
            Book2.listSheet[Book2.current_sheet.title].index_row = 1
            for row2 in Book2.current_sheet.iter_rows(2, Book2.current_sheet.max_row):
                CMND_map2 = row2[CMND_index_map2].value
                # print(CMND_map2)
                Book2.listSheet[Book2.current_sheet.title].inc_index_row()
                if CMND_map1 == CMND_map2:
                    # print("after",Book2.listSheet[Book2.current_sheet.title].index_row - 1,"times, found",CMND_map1)
                    khoi_hight_point, max_point, max_point_add_gap = common_func.caculate_point(Book2, CMND_map1, temp_major)
                    ut_point = common_func.caculate_ut_point(Book2, CMND_map1)

                    final_point = max_point + ((30 - max_point)/7.5)*ut_point
                    final_point = round(final_point,2)

                    print("student id",CMND_map1,"with khoi",khoi_hight_point,"has point",final_point)

                    cell = output_file.current_sheet.cell(row = row1_index, column = culumn_khoi_trung_tuyen)
                    cell.value = khoi_hight_point

                    cell = output_file.current_sheet.cell(row = row1_index, column = culumn_diem)
                    cell.value = final_point

                    final_point = max_point_add_gap + ((30 - max_point_add_gap)/7.5)*ut_point
                    final_point = round(final_point,2)

                    cell = output_file.current_sheet.cell(row = row1_index, column = culumn_diem_add_gap)
                    cell.value = final_point

                    output_file.sort_inc_base_on_column_index(culumn_diem_add_gap)
                    output_file.save_file()
                    break

        
        if temp_val == 2:
            break

##############################################################
#
##############################################################
    CMND_index_map1 = 1
    if (False == Fixed_format):
        CMND_index_map1 = output_file.find_colum_index_with_content("Số CMND")

    current_student_id = ""
    current_student_NV = ""

    temp_target = 0

    sheet_checked = []

    for each_sheet in list_id_major:
        sheet_checked.append(each_sheet)
        output_file.chosse_current_sheet(each_sheet)

        for row_index, row in enumerate(output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2):
            current_student_id = row[CMND_index_map1].value
            current_student_NV = row[CMND_index_map1].value

            for each_other_sheet in list_id_major:
                if each_other_sheet in sheet_checked:
                    continue
                output_file.chosse_current_sheet(each_other_sheet)

                for row_other_sheet_index, row_other_sheet in enumerate(output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2):
                    if current_student_id == row_other_sheet[CMND_index_map1].value:
                        if (current_student_NV < row_other_sheet[CMND_index_map1].value) and (row_other_sheet_index + 1 < targets):
                            output_file.remove_row_index_with_sheet(each_sheet, row_index)
                            temp_target -= 1
                            break
                        else:
                            output_file.remove_row_index_with_sheet(each_other_sheet, row_other_sheet_index)
                            break

        temp_target += 1
        if (temp_target == targets):
            break

    output_file.save_file()
    
    print(time.process_time() - start)

##############################################################
# call main function
##############################################################
if __name__ == '__main__':
    main(sys.argv[1:])
    
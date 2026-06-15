##############################################################
# Created by Thanh Duong
##############################################################
import sys
import common
import common_func
import time
import openpyxl
start = time.process_time()

# Whether column indices are hardcoded (True) or auto-discovered from headers (False)
FIXED_FORMAT = True

# Target number of accepted students per major
TARGETS = 100

# 1-based output column positions written into ExampleOutput.xlsx
COL_KHOI_TRUNG_TUYEN = 22   # best subject combination name
COL_DIEM            = 23   # final admission score
COL_DIEM_ADD_GAP    = 24   # final score including gap bonus

##############################################################
# main function
##############################################################
def main(argv):
    toHop_THTP = common.ExcelHandler("toHop_THTP.xlsx")
    toHop_THTP.chosse_current_sheet('Sheet1')

    Book1 = common.ExcelHandler("Book1.xlsx")
    Book1.chosse_current_sheet('Sheet1')

    Book2 = common.ExcelHandler("Book2.xlsx")
    Book2.chosse_current_sheet("Sheet1")

    new_workbook = openpyxl.Workbook()
    name_new_workbook = "ExampleOutput.xlsx"
    new_workbook.save(name_new_workbook)
    print("Excel file", name_new_workbook, "has been created.")
    output_file = common.ExcelHandler(name_new_workbook)

    # ##########################################################
    # # Create a new Workbook and crist sheet contain all majors
    # ##########################################################
    # Flatten the single header row into a list
    row_data_header = [
        v
        for row in Book1.current_sheet.iter_rows(min_row=1, max_row=1, values_only=True)
        for v in row
    ]

    list_id_major = []

    index_maNganh = 0
    if not FIXED_FORMAT:
        index_maNganh = toHop_THTP.find_colum_index_with_content("maNganh")

    for col in toHop_THTP.current_sheet.iter_rows(2, toHop_THTP.current_sheet.max_row):
        sheet_name = col[index_maNganh].value
        if sheet_name not in output_file.workbook.sheetnames:
            if sheet_name not in list_id_major:
                list_id_major.append(sheet_name)
            output_file.add_sheet(sheet_name)
            output_file.chosse_current_sheet(sheet_name)
            for col_idx, header_val in enumerate(row_data_header, start=1):
                output_file.current_sheet.cell(row=1, column=col_idx, value=header_val)

    output_file.remove_sheet("Sheet")
    output_file.save_file()

    ##########################################################
    # start to arange to major
    ##########################################################

    ma_nganh_index = Book1.find_colum_index_with_content("Mã ngành")
    ma_PTXT_index  = Book1.find_colum_index_with_content("Mã PTXT")

    for row in Book1.current_sheet.iter_rows(2, Book1.current_sheet.max_row):
        sheet_name = row[ma_nganh_index].value
        if row[ma_PTXT_index].value != '100':
            continue

        print(f"Distributing student to major: {sheet_name}")

        row_data = [cell.value for cell in row if cell.value != '']

        if sheet_name in output_file.workbook.sheetnames:
            output_file.chosse_current_sheet(sheet_name)
            output_file.listSheet[sheet_name].index_row += 1
            for col_idx, val in enumerate(row_data, start=1):
                output_file.current_sheet.cell(
                    row=output_file.listSheet[sheet_name].index_row,
                    column=col_idx,
                    value=val,
                )
        else:
            print(f"Sheet '{sheet_name}' does not exist in the output file.")

    output_file.save_file()
    ##########################################################
    # get the list Khoi and its subject contain
    ##########################################################
    list_major = []
    maTohop_index  = 2
    mon1_index     = 5
    mon2_index     = 6
    mon3_index     = 7
    maNganh_index  = 0
    toHopGoc_index = 3
    heSoM1_index   = 8
    heSoM2_index   = 9
    heSoM3_index   = 10
    gap_point_index = 11
    if not FIXED_FORMAT:
        maTohop_index   = toHop_THTP.find_colum_index_with_content("maTohop")
        mon1_index      = toHop_THTP.find_colum_index_with_content("mon1")
        mon2_index      = toHop_THTP.find_colum_index_with_content("mon2")
        mon3_index      = toHop_THTP.find_colum_index_with_content("mon3")
        maNganh_index   = toHop_THTP.find_colum_index_with_content("maNganh")
        toHopGoc_index  = toHop_THTP.find_colum_index_with_content("toHopGoc")
        heSoM1_index    = toHop_THTP.find_colum_index_with_content("heSoM1")
        heSoM2_index    = toHop_THTP.find_colum_index_with_content("heSoM2")
        heSoM3_index    = toHop_THTP.find_colum_index_with_content("heSoM3")
        gap_point_index = toHop_THTP.find_colum_index_with_content("gap_point")

    for each_id_major in list_id_major:
        mMajor = common.ClassMajor(each_id_major)
        for row in toHop_THTP.current_sheet.iter_rows(2, toHop_THTP.current_sheet.max_row):
            if each_id_major != row[maNganh_index].value:
                continue
            mClassKhoi = common.ClassKhoi(row[maTohop_index].value)
            mClassKhoi.list_subject = [
                row[mon1_index].value,
                row[mon2_index].value,
                row[mon3_index].value,
            ]
            mClassKhoi.he_so = {
                row[mon1_index].value: row[heSoM1_index].value,
                row[mon2_index].value: row[heSoM2_index].value,
                row[mon3_index].value: row[heSoM3_index].value,
            }
            mClassKhoi.gap_point = row[gap_point_index].value
            mMajor.add_khoi(mClassKhoi)
            if row[toHopGoc_index].value in ("x", "X"):
                mMajor.update_primary_khoi(mClassKhoi)

        list_major.append(mMajor)

    ##########################################################
    # caculate point
    ##########################################################

    Book2.chosse_current_sheet("Sheet1")

    CMND_index_map1 = 1
    if not FIXED_FORMAT:
        CMND_index_map1 = output_file.find_colum_index_with_content("Số CMND")

    CMND_index_map2 = 3
    if not FIXED_FORMAT:
        CMND_index_map2 = Book2.find_colum_index_with_content("CMND")

    # Build a CMND → row-values dict ONCE so each student lookup is O(1)
    # instead of an O(N) scan through every Book2 row per student.
    book2_lookup = common_func.build_score_lookup(Book2, CMND_index_map2)

    for temp_major in list_major:
        print(f"Calculating scores for major: {temp_major.major_id}")
        output_file.chosse_current_sheet(temp_major.major_id)

        # Write result column headers ONCE per sheet (not on every student row)
        output_file.current_sheet.cell(row=1, column=COL_KHOI_TRUNG_TUYEN).value = "khoi_trung_tuyen"
        output_file.current_sheet.cell(row=1, column=COL_DIEM).value = "final_point"
        output_file.current_sheet.cell(row=1, column=COL_DIEM_ADD_GAP).value = "final_point_add_gap"

        for row1_index, row1 in enumerate(
            output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2
        ):
            cmnd = row1[CMND_index_map1]
            row2_values = book2_lookup.get(cmnd)
            if row2_values is None:
                continue  # student not found in Book2 — skip

            best_khoi, max_point, max_point_add_gap = common_func.calculate_point(row2_values, temp_major)
            ut_point = common_func.calculate_ut_point(row2_values)

            final_point = max_point + ((30 - max_point) / 7.5) * ut_point
            final_point = round(final_point, 2)
            print(f"  Student {cmnd} | khoi={best_khoi} | score={final_point}")

            output_file.current_sheet.cell(row=row1_index, column=COL_KHOI_TRUNG_TUYEN).value = best_khoi
            output_file.current_sheet.cell(row=row1_index, column=COL_DIEM).value = final_point

            final_point_gap = max_point_add_gap + ((30 - max_point_add_gap) / 7.5) * ut_point
            final_point_gap = round(final_point_gap, 2)
            output_file.current_sheet.cell(row=row1_index, column=COL_DIEM_ADD_GAP).value = final_point_gap

        output_file.sort_inc_base_on_column_index(COL_DIEM_ADD_GAP)
        output_file.save_file()

    # ------------------------------------------------------------------
    # Deduplication: if a student appears in multiple major sheets,
    # keep them in their preferred sheet and remove from others.
    # Cap processing once TARGETS sheets have been handled.
    # ------------------------------------------------------------------
    CMND_index_map1 = 1
    if not FIXED_FORMAT:
        CMND_index_map1 = output_file.find_colum_index_with_content("Số CMND")

    temp_target = 0
    sheet_checked = []

    for each_sheet in list_id_major:
        sheet_checked.append(each_sheet)
        output_file.chosse_current_sheet(each_sheet)

        for row_index, row in enumerate(
            output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2
        ):
            # values_only=True already returns plain Python values — no .value needed
            current_student_id = row[CMND_index_map1]
            current_student_NV = row[CMND_index_map1]  # NOTE: same as ID (original logic preserved)

            for each_other_sheet in list_id_major:
                if each_other_sheet in sheet_checked:
                    continue
                output_file.chosse_current_sheet(each_other_sheet)

                for row_other_sheet_index, row_other_sheet in enumerate(
                    output_file.current_sheet.iter_rows(min_row=2, values_only=True), start=2
                ):
                    if current_student_id == row_other_sheet[CMND_index_map1]:  # fixed: was .value
                        if (
                            current_student_NV < row_other_sheet[CMND_index_map1]
                            and row_other_sheet_index + 1 < TARGETS
                        ):
                            output_file.remove_row_index_with_sheet(each_sheet, row_index)
                            temp_target -= 1
                            break
                        else:
                            output_file.remove_row_index_with_sheet(each_other_sheet, row_other_sheet_index)
                            break

        temp_target += 1
        if temp_target == TARGETS:
            break

    output_file.save_file()
    print(f"Done. Elapsed CPU time: {time.process_time() - start:.2f}s")

##############################################################
# call main function
##############################################################
if __name__ == '__main__':
    main(sys.argv[1:])
    
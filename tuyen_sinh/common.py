import openpyxl

class ClassKhoi:
    def __init__(self, name):
        self.name = name
        self.list_subject = []
        self.he_so = {}
        self.gap_point = 0
    
    def print_info(self):
        print("the Subject Combination is", self.name)
        print("list subject is", self.list_subject)

class ClassMajor:
    def __init__(self, major_id):
        self.major_id = major_id
        self.maToHop = []
        self.primary_khoi = ClassKhoi("None")

    def add_khoi(self, khoi):
        """Add a subject combination to this major. Silently ignores duplicates by name."""
        for existing in self.maToHop:
            if existing.name == khoi.name:
                print(f"Combination '{khoi.name}' already exists in major '{self.major_id}'")
                return
        self.maToHop.append(khoi)

    def update_primary_khoi(self, primary_khoi):
        self.primary_khoi = primary_khoi

    def print_info(self):
        print(f"Major ID: {self.major_id}")
        print(f"Primary khoi: {self.primary_khoi.name}")
        print("Subject combinations:")
        for khoi in self.maToHop:
            print(f"\t{khoi.name} | subjects={khoi.list_subject} | he_so={khoi.he_so} | gap={khoi.gap_point}")
        print()

# NOTE: Student class removed — it was unused and its __init__ called ClassMajor()
# without the required major_id argument, making it uninstantiable.

class ExcelHandler:
    class SheetIndexMapping:
        def __init__(self):
            self.index_colum = 1
            self.index_row = 1
            self.max_index_colum = 1
            self.max_index_row = 1
        
        def inc_index_column(self):
            self.index_colum += 1
            if(self.max_index_colum < self.index_colum):
                self.max_index_colum = self.index_colum

        def inc_index_row(self):
            self.index_row += 1
            if(self.max_index_row < self.index_row):
                self.max_index_row = self.index_row

    def __init__(self, name_file):
        self.name_file = name_file
        print(f"Opening Excel file: {name_file}")
        self.workbook = openpyxl.load_workbook(self.name_file)
        self.current_sheet = self.workbook.active
        self.listSheet = {
            name: ExcelHandler.SheetIndexMapping()
            for name in self.workbook.sheetnames
        }

    def chosse_current_sheet(self, sheet_name):
        """Switch current_sheet to sheet_name (must be a string title)."""
        if sheet_name not in self.workbook.sheetnames:
            print(f"Sheet '{sheet_name}' does not exist.")
            return
        self.current_sheet = self.workbook[sheet_name]
        self.workbook.active = self.current_sheet

    def print_info(self):
        print(f"File name: {self.name_file}")
        print(f"Current sheet: {self.current_sheet.title}")
    
    def print_data_collum(self, my_collum_value):
        for col in self.current_sheet.iter_rows(1, self.current_sheet.max_row):
            print(col[my_collum_value].value)

    def print_data_row(self, my_row_value):
        for col in self.current_sheet.iter_cols(1, self.current_sheet.max_column):
            print(my_row_value[col].value)
    
    def add_sheet(self, sheet_name_to_add):
        self.workbook.create_sheet(sheet_name_to_add)
        self.listSheet[sheet_name_to_add] = ExcelHandler.SheetIndexMapping()
        print(f"Created sheet: {sheet_name_to_add}")

    def remove_sheet(self, sheet_name_to_remove):
        if sheet_name_to_remove in self.workbook.sheetnames:
            self.workbook.remove(self.workbook[sheet_name_to_remove])
            print(f"Sheet '{sheet_name_to_remove}' removed.")
        else:
            print(f"Sheet '{sheet_name_to_remove}' does not exist.")
    
    def find_colum_index_with_content(self, content):
        for idx, col in enumerate(self.current_sheet.iter_cols(1, self.current_sheet.max_column)):
            if col[0].value == content:
                print(f"Found column '{content}' at index {idx} in sheet '{self.current_sheet.title}'")
                return idx
        return None

    def find_row_index_with_content(self, content):
        for idx, row in enumerate(self.current_sheet.iter_rows(1, self.current_sheet.max_row)):
            if row[0].value == content:
                return idx
        return None
    
    def save_file(self):
        self.workbook.save(self.name_file)

    def sort_inc_base_on_column_index(self, column_index):
        """Sort sheet rows descending by column_index (1-based). Rows with None sort last."""
        data_rows = list(self.current_sheet.iter_rows(min_row=2, values_only=True))
        max_col = self.current_sheet.max_column
        padded_rows = [row + (None,) * (max_col - len(row)) for row in data_rows]

        # Key: (is_none, negated_value) → None values sink to end; real values sort descending
        def sort_key(row):
            val = row[column_index - 1]
            return (val is None, -(val if isinstance(val, (int, float)) else 0))

        sorted_rows = sorted(padded_rows, key=sort_key)

        for row in self.current_sheet.iter_rows(
            min_row=2, max_row=self.current_sheet.max_row, min_col=1, max_col=max_col
        ):
            for cell in row:
                cell.value = None

        for row_idx, data_row in enumerate(sorted_rows, start=2):
            for col_idx, value in enumerate(data_row, start=1):
                self.current_sheet.cell(row=row_idx, column=col_idx, value=value)
    
    def remove_row_index(self, row_index_to_remove):
        # Delete the specified row
        self.current_sheet.delete_rows(row_index_to_remove)

    def remove_row_index_with_sheet(self, sheet_name_to_remove_row, row_index_to_remove):
        """Delete a row in a named sheet, then restore the previously active sheet."""
        saved_title = self.current_sheet.title  # save by title (string), not object
        self.chosse_current_sheet(sheet_name_to_remove_row)
        self.current_sheet.delete_rows(row_index_to_remove)
        self.chosse_current_sheet(saved_title)
        
import common

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Set True to use hardcoded column indices; False to discover them from headers.
FIXED_FORMAT = True

# 0-based column indices for each subject / priority field inside Book2.
# Original code used column = index + 1 (1-based openpyxl); here we store the
# 0-based index so row_values[index] works with values_only=True rows.
SUBJECT_COLUMN_MAP = {
    "TO":   26,
    "VA":   27,
    "LI":   28,
    "HO":   29,
    "SI":   30,
    "SU":   31,
    "DI":   32,
    "GDCD": 33,
    "NN":   34,
    "KVƯT": 7,
    "ĐTƯT": 6,
}

# Priority-region (KVƯT) bonus points by category code
_KVUT_SCORE_MAP = {
    "2NT": 0.5, "KV2-NT": 0.5,
    "1":   0.75, "KV1":   0.75,
    "2":   0.25, "KV2":   0.25,
    "3":   0.0,  "KV3":   0.0,
}

# ---------------------------------------------------------------------------
# New efficient API (operates on pre-fetched row tuples)
# ---------------------------------------------------------------------------

def build_score_lookup(book2, cmnd_col_index):
    """
    Pre-build a dict mapping CMND value → row-values tuple from Book2.

    This replaces the original O(N) linear scan per student with an O(1) lookup.

    Args:
        book2:           ExcelHandler wrapping the scores workbook.
        cmnd_col_index:  0-based column index of the CMND field in Book2.

    Returns:
        dict[cmnd -> tuple of cell values (0-based)]
    """
    lookup = {}
    for row in book2.current_sheet.iter_rows(min_row=2, values_only=True):
        cmnd = row[cmnd_col_index]
        if cmnd is not None:
            lookup[cmnd] = row
    return lookup


def subject_point_from_row(row_values, subject):
    """
    Return a student's score for *subject* from a pre-fetched row tuple.

    Args:
        row_values:  tuple of plain Python values from iter_rows(values_only=True).
        subject:     subject code, e.g. "TO", "VA", "KVƯT".

    Returns:
        float score, or 0.0 when the column is absent or the value is non-numeric.
    """
    col = SUBJECT_COLUMN_MAP.get(subject)
    if col is None or col >= len(row_values):
        return 0.0

    value = row_values[col]

    if subject == "KVƯT":
        return _KVUT_SCORE_MAP.get(str(value), 0.0) if value is not None else 0.0

    if subject == "ĐTƯT":
        if value in ("01", "02", "03", "04"):
            return 2.0
        if value in ("05", "06", "07"):
            return 1.0
        return 0.0

    return float(value) if isinstance(value, (int, float)) else 0.0


def calculate_ut_point(row_values):
    """Return total priority bonus points (KVƯT + ĐTƯT) for a student row."""
    return (
        subject_point_from_row(row_values, "KVƯT")
        + subject_point_from_row(row_values, "ĐTƯT")
    )


def calculate_point(row_values, major):
    """
    Compute the best weighted admission score across all subject combinations
    (tổ hợp / khối) for a student.

    Score formula per khoi:
        point = 3 × (Σ subject_score × he_so) / (Σ he_so)
    Maximum possible score is 30 (all subjects = 10, equal weights).

    Args:
        row_values:  tuple of plain Python values for the student from Book2.
        major:       ClassMajor instance with its maToHop list.

    Returns:
        (best_khoi_name, max_point, max_point_add_gap)
    """
    max_point = 0.0
    max_point_add_gap = 0.0
    best_khoi_name = ""

    for khoi in major.maToHop:
        sum_of_heso = sum(khoi.he_so.get(s, 1) for s in khoi.list_subject)
        if sum_of_heso == 0:
            continue
        weighted_sum = sum(
            subject_point_from_row(row_values, s) * khoi.he_so.get(s, 1)
            for s in khoi.list_subject
        )
        point = 3.0 * (weighted_sum / sum_of_heso)

        if point > max_point:
            max_point = point
            max_point_add_gap = max_point + khoi.gap_point
            best_khoi_name = khoi.name

    return best_khoi_name, max_point, max_point_add_gap


# ---------------------------------------------------------------------------
# Legacy wrappers — kept for backward compatibility
# ---------------------------------------------------------------------------

def subject_point(Book2, subject):
    """Legacy: read subject score via Book2's tracked row index (original API)."""
    col = SUBJECT_COLUMN_MAP.get(subject)
    if col is None:
        return 0

    row_idx = Book2.listSheet[Book2.current_sheet.title].index_row
    value = Book2.current_sheet.cell(row=row_idx, column=col + 1).value

    if subject == "KVƯT":
        return _KVUT_SCORE_MAP.get(str(value), 0.0) if value is not None else 0.0

    if subject == "ĐTƯT":
        if value in ("01", "02", "03", "04"):
            return 2.0
        if value in ("05", "06", "07"):
            return 1.0
        return 0.0

    return float(value) if isinstance(value, (int, float)) else 0


def caculate_ut_point(Book2, CMND_map1):
    """Legacy wrapper — use calculate_ut_point(row_values) for new code."""
    return subject_point(Book2, "KVƯT") + subject_point(Book2, "ĐTƯT")


def caculate_point(Book2, CMND, major):
    """Legacy wrapper — use calculate_point(row_values, major) for new code."""
    row_idx = Book2.listSheet[Book2.current_sheet.title].index_row
    row_values = tuple(
        Book2.current_sheet.cell(row=row_idx, column=c).value
        for c in range(1, Book2.current_sheet.max_column + 1)
    )
    return calculate_point(row_values, major)

"""
Unit tests for common_func.py and the ClassMajor / ClassKhoi data classes.

Run with:
    cd /Users/thanhduong/Embeded_Project/Python_code/tuyen_sinh
    python -m pytest test_common_func.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(__file__))

import common
import common_func


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_row(col_values: dict, length: int = 40) -> tuple:
    """Build a row-values tuple of *length* with specific 0-based indices set."""
    row = [None] * length
    for col, val in col_values.items():
        row[col] = val
    return tuple(row)


def make_major(khoi_name, subjects, he_so_values, gap=0):
    """Create a ClassMajor with a single ClassKhoi for testing."""
    major = common.ClassMajor("TEST001")
    khoi = common.ClassKhoi(khoi_name)
    khoi.list_subject = list(subjects)
    khoi.he_so = dict(zip(subjects, he_so_values))
    khoi.gap_point = gap
    major.add_khoi(khoi)
    return major


# ---------------------------------------------------------------------------
# subject_point_from_row
# ---------------------------------------------------------------------------

class TestSubjectPointFromRow:

    def test_numeric_subject_returns_float(self):
        row = make_row({26: 8.5})   # TO is at column index 26
        assert common_func.subject_point_from_row(row, "TO") == 8.5

    def test_integer_subject_returned_as_float(self):
        row = make_row({27: 7})     # VA
        assert common_func.subject_point_from_row(row, "VA") == pytest.approx(7.0)

    def test_none_value_returns_zero(self):
        row = make_row({})          # all None
        assert common_func.subject_point_from_row(row, "TO") == 0.0

    def test_string_value_returns_zero(self):
        row = make_row({26: "abc"})
        assert common_func.subject_point_from_row(row, "TO") == 0.0

    def test_unknown_subject_returns_zero(self):
        row = make_row({26: 9.0})
        assert common_func.subject_point_from_row(row, "UNKNOWN") == 0.0

    # KVƯT (priority region)
    def test_kvut_kv1(self):
        assert common_func.subject_point_from_row(make_row({7: "KV1"}), "KVƯT") == 0.75

    def test_kvut_kv2nt(self):
        assert common_func.subject_point_from_row(make_row({7: "2NT"}), "KVƯT") == 0.5

    def test_kvut_kv2nt_alt(self):
        assert common_func.subject_point_from_row(make_row({7: "KV2-NT"}), "KVƯT") == 0.5

    def test_kvut_kv2(self):
        assert common_func.subject_point_from_row(make_row({7: "KV2"}), "KVƯT") == 0.25

    def test_kvut_kv3_returns_zero(self):
        assert common_func.subject_point_from_row(make_row({7: "KV3"}), "KVƯT") == 0.0

    def test_kvut_none_returns_zero(self):
        assert common_func.subject_point_from_row(make_row({}), "KVƯT") == 0.0

    # ĐTƯT (priority category)
    def test_dtut_group1_codes(self):
        for code in ("01", "02", "03", "04"):
            assert common_func.subject_point_from_row(make_row({6: code}), "ĐTƯT") == 2.0

    def test_dtut_group2_codes(self):
        for code in ("05", "06", "07"):
            assert common_func.subject_point_from_row(make_row({6: code}), "ĐTƯT") == 1.0

    def test_dtut_other_returns_zero(self):
        assert common_func.subject_point_from_row(make_row({6: "08"}), "ĐTƯT") == 0.0

    def test_dtut_none_returns_zero(self):
        assert common_func.subject_point_from_row(make_row({}), "ĐTƯT") == 0.0


# ---------------------------------------------------------------------------
# calculate_ut_point
# ---------------------------------------------------------------------------

class TestCalculateUtPoint:

    def test_no_priority_at_all(self):
        row = make_row({7: "KV3", 6: "08"})
        assert common_func.calculate_ut_point(row) == 0.0

    def test_region_only(self):
        row = make_row({7: "KV1", 6: "08"})
        assert common_func.calculate_ut_point(row) == pytest.approx(0.75)

    def test_category_only(self):
        row = make_row({7: "KV3", 6: "01"})
        assert common_func.calculate_ut_point(row) == pytest.approx(2.0)

    def test_combined(self):
        row = make_row({7: "KV1", 6: "01"})   # 0.75 + 2.0
        assert common_func.calculate_ut_point(row) == pytest.approx(2.75)


# ---------------------------------------------------------------------------
# calculate_point
# ---------------------------------------------------------------------------

class TestCalculatePoint:
    """
    Score formula per khoi:
        point = 3 × Σ(score × he_so) / Σ(he_so)
    Maximum = 30 (all subjects score 10, any equal weights).
    """

    def test_equal_weights_three_subjects(self):
        # TO=8, VA=6, LI=7 → avg=7 → 3*7=21
        row = make_row({26: 8.0, 27: 6.0, 28: 7.0})
        major = make_major("A00", ["TO", "VA", "LI"], [1, 1, 1])
        name, max_pt, max_pt_gap = common_func.calculate_point(row, major)
        assert name == "A00"
        assert max_pt == pytest.approx(21.0)
        assert max_pt_gap == pytest.approx(21.0)   # gap=0

    def test_maximum_possible_score(self):
        row = make_row({26: 10.0, 27: 10.0, 28: 10.0})
        major = make_major("A00", ["TO", "VA", "LI"], [1, 1, 1])
        _, max_pt, _ = common_func.calculate_point(row, major)
        assert max_pt == pytest.approx(30.0)

    def test_gap_point_applied_to_max(self):
        row = make_row({26: 8.0, 27: 6.0, 28: 7.0})   # point=21
        major = make_major("A00", ["TO", "VA", "LI"], [1, 1, 1], gap=0.5)
        _, max_pt, max_pt_gap = common_func.calculate_point(row, major)
        assert max_pt_gap == pytest.approx(max_pt + 0.5)

    def test_picks_highest_scoring_khoi(self):
        # A00 (TO/VA/LI = 5 each) → 15; B03 (HO/SI/SU = 9 each) → 27
        row = make_row({26: 5.0, 27: 5.0, 28: 5.0,
                        29: 9.0, 30: 9.0, 31: 9.0})
        major = common.ClassMajor("TEST002")
        k1 = common.ClassKhoi("A00")
        k1.list_subject = ["TO", "VA", "LI"]
        k1.he_so = {"TO": 1, "VA": 1, "LI": 1}
        k1.gap_point = 0
        k2 = common.ClassKhoi("B03")
        k2.list_subject = ["HO", "SI", "SU"]
        k2.he_so = {"HO": 1, "SI": 1, "SU": 1}
        k2.gap_point = 0
        major.add_khoi(k1)
        major.add_khoi(k2)

        name, max_pt, _ = common_func.calculate_point(row, major)
        assert name == "B03"
        assert max_pt == pytest.approx(27.0)

    def test_all_zero_scores_return_empty_name(self):
        row = make_row({})    # all None → all zeros
        major = make_major("A00", ["TO", "VA", "LI"], [1, 1, 1])
        name, max_pt, max_pt_gap = common_func.calculate_point(row, major)
        # max_point stays 0 and the khoi that achieves 0 is NOT counted as "best"
        assert max_pt == 0.0

    def test_empty_major_returns_zero(self):
        row = make_row({26: 9.0})
        major = common.ClassMajor("EMPTY")
        name, max_pt, max_pt_gap = common_func.calculate_point(row, major)
        assert name == ""
        assert max_pt == 0.0
        assert max_pt_gap == 0.0


# ---------------------------------------------------------------------------
# build_score_lookup
# ---------------------------------------------------------------------------

class TestBuildScoreLookup:

    def test_lookup_returns_correct_row(self, tmp_path):
        """Smoke-test build_score_lookup with a real (tiny) openpyxl workbook."""
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        # Row 1 = header; row 2 = data
        ws.append(["col0", "col1", "col2", "CMND"])
        ws.append(["a", "b", "c", "123456"])
        ws.append(["d", "e", "f", "789012"])

        path = str(tmp_path / "test_book2.xlsx")
        wb.save(path)

        handler = common.ExcelHandler(path)
        handler.chosse_current_sheet("Sheet1")
        lookup = common_func.build_score_lookup(handler, cmnd_col_index=3)

        assert "123456" in lookup
        assert lookup["123456"][0] == "a"
        assert "789012" in lookup


# ---------------------------------------------------------------------------
# ClassMajor.add_khoi  (the critical bug-fix)
# ---------------------------------------------------------------------------

class TestClassMajorAddKhoi:

    def test_first_khoi_added(self):
        major = common.ClassMajor("M001")
        major.add_khoi(common.ClassKhoi("A00"))
        assert len(major.maToHop) == 1

    def test_duplicate_name_not_added(self):
        """Original bug: is_add flag was never reset, so after one duplicate
        no further khoi could be added. Fixed by removing is_add entirely."""
        major = common.ClassMajor("M001")
        major.add_khoi(common.ClassKhoi("A00"))
        major.add_khoi(common.ClassKhoi("A00"))   # duplicate
        assert len(major.maToHop) == 1

    def test_new_khoi_after_duplicate_still_added(self):
        """Regression: with the old bug, adding a duplicate permanently broke
        subsequent additions of distinct khoi names."""
        major = common.ClassMajor("M001")
        major.add_khoi(common.ClassKhoi("A00"))
        major.add_khoi(common.ClassKhoi("A00"))   # duplicate — should be ignored
        major.add_khoi(common.ClassKhoi("B00"))   # new — must be added
        assert len(major.maToHop) == 2

    def test_multiple_distinct_khoi_added(self):
        major = common.ClassMajor("M002")
        for name in ("A00", "B00", "D01"):
            major.add_khoi(common.ClassKhoi(name))
        assert len(major.maToHop) == 3

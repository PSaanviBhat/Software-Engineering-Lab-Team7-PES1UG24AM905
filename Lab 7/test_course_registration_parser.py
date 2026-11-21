from hypothesis import given, strategies as st
from course_registration_parser import (
    format_course_code,
    total_credits,
    parse_student_record,
)


@given(st.text() | st.none())
def test_format_course_code_no_crash(s):
    """Fuzz test format_course_code to ensure it never crashes on any input."""
    try:
        format_course_code(s)
    except Exception as e:
        assert False, f"format_course_code crashed with: {e}"


@given(st.text() | st.none())
def test_total_credits_no_crash(s):
    """Fuzz test total_credits to ensure it never crashes on any input."""
    try:
        total_credits(s)
    except Exception as e:
        assert False, f"total_credits crashed with: {e}"


@given(st.text() | st.none())
def test_parse_student_record_no_crash(s):
    """Fuzz test parse_student_record to ensure it never crashes on any input."""
    try:
        parse_student_record(s)
    except Exception as e:
        assert False, f"parse_student_record crashed with: {e}"

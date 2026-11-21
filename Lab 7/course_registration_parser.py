"""Course Registration Parser Module.

Provides robust functions to parse user-entered course codes, credit totals,
and student records with comprehensive defensive input validation.
"""


def format_course_code(code):
    """Format a course code like 'cs 301' into 'CS301'.

    Safely handles any input type including None, empty strings, single words,
    multiple words, or non-string objects without raising exceptions.

    Args:
        code (Any): Raw course code input string.

    Returns:
        str: Standardized uppercase formatted course code (e.g. 'CS301'),
        or empty string '' if input is invalid or cannot be parsed.
    """
    if code is None or not isinstance(code, str):
        return ""
    parts = code.strip().split()
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0].upper()
    dept = parts[0].upper()
    number = "".join(parts[1:])
    return dept + number


def total_credits(text):
    """Calculate the sum of comma-separated course credit values.

    Defensively filters out empty values, non-numeric strings, negative
    values, and handles non-string inputs or None safely.

    Args:
        text (Any): Comma-separated credit values string (e.g. '4,3,4').

    Returns:
        int: Total sum of valid positive integer credits, or 0 on invalid input.
    """
    if text is None or not isinstance(text, str):
        return 0
    total = 0
    for credit in text.split(","):
        cleaned = credit.strip()
        if not cleaned:
            continue
        try:
            val = int(cleaned)
            if val > 0:
                total += val
        except (ValueError, TypeError):
            continue
    return total


def parse_student_record(line):
    """Parse 'SRN|name|status' line into a structured dictionary.

    Safely handles missing fields, extra delimiters, non-string types, and None.

    Args:
        line (Any): Raw student record input line.

    Returns:
        dict: Dictionary containing 'srn', 'name', and 'status'.
    """
    if line is None or not isinstance(line, str):
        return {"srn": "", "name": "", "status": "unknown"}
    parts = line.split("|")
    srn = parts[0].strip().upper() if len(parts) > 0 else ""
    name = parts[1].strip() if len(parts) > 1 else ""
    status = parts[2].strip().lower() if len(parts) > 2 else "unknown"
    return {"srn": srn, "name": name, "status": status}


def main():
    """Run interactive demonstration of course registration parser functions."""
    print("==== Running format_course_code ====")
    try:
        value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    except EOFError:
        value = "cs 301"
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    try:
        value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    except EOFError:
        value = "4,3,4"
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    try:
        value = input(
            "Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): "
        )
    except EOFError:
        value = "pes1ug23cs001|Asha|regular"
    print("Student record:", parse_student_record(value))


if __name__ == "__main__":
    main()

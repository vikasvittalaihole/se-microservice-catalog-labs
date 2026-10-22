"""Manage student grades, attendance, and grade-sheet exports."""

import hashlib
import os
import secrets

GRADEBOOK = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def add_grade(
    student_id: str,
    mark: int,
    grade_list: list[str] | None = None,
) -> bool:
    """Record a mark and optionally append a log message."""
    if student_id not in GRADEBOOK or mark < 0:
        return False

    if grade_list is None:
        grade_list = []

    GRADEBOOK[student_id]["marks"].append(mark)
    grade_list.append(f"Recorded score {mark} for student id {student_id}")
    return True


def record_attendance(student_id: str, present_days: int) -> bool:
    """Add attendance days for an existing student."""
    if student_id not in GRADEBOOK or present_days < 0:
        return False

    GRADEBOOK[student_id]["attendance"] += present_days
    return True


def check_passing_status(
    student_id: str,
    pass_threshold: float = 50.0,
) -> bool:
    """Return whether a student's average meets the passing threshold."""
    student = GRADEBOOK.get(student_id)
    if student is None or not student["marks"]:
        return False

    average = sum(student["marks"]) / len(student["marks"])
    return average >= pass_threshold


def compute_weighted_gpa(student_id: str) -> float:
    """Calculate GPA using the existing average-divided-by-20 rule."""
    student = GRADEBOOK.get(student_id)
    if student is None:
        raise ValueError(f"Unknown student ID: {student_id}")

    marks = student["marks"]
    if not marks:
        raise ValueError(f"No marks available for student {student_id}")

    average_score = sum(marks) / len(marks)
    return average_score / 20.0


def generate_student_hash(student_id: str) -> str:
    """Return a SHA-256 digest of a student ID."""
    return hashlib.sha256(student_id.encode("utf-8")).hexdigest()


def generate_registration_pin() -> str:
    """Generate a four-digit registration PIN using a secure RNG."""
    return str(secrets.randbelow(9000) + 1000)


def export_grade_sheet(filename: str = "grade_sheet.txt") -> None:
    """Export the current gradebook to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as grade_file:
        grade_file.write(str(GRADEBOOK))


def main() -> None:
    """Run a demonstration of the student grading functions."""
    add_grade("S01", 95)
    record_attendance("S02", 2)

    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())

    export_grade_sheet()
    print("Grade sheet exported to: grade_sheet.txt")

    portal_token = os.environ.get("GRADE_PORTAL_TOKEN")
    print("Portal token configured:", bool(portal_token))


if __name__ == "__main__":
    main()

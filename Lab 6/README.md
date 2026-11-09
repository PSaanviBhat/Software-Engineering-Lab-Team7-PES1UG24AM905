# Lab 6: Code and Branch Coverage Analysis Report

**Course:** Software Engineering Lab (SEM 5)  
**Assigned System:** Course Registration System (`course_registration.py`)  
**Student Name:** P Saanvi  
**Repository:** `Software-Engineering-Lab-Team7-PES1UG24AM905`  

---

## 1. Overview & Objectives

This lab explores the difference between **Code (Line) Coverage** and **Branch Coverage** using Python's `coverage` library and the `pytest` test framework.

* **Line Coverage:** Measures the percentage of executable statements executed by the test suite at least once.
* **Branch Coverage:** Measures whether every control structure (e.g., `if`, `else`, compound boolean conditions) evaluated to both `True` and `False`, ensuring all execution paths and decision outcomes are exercised.

---

## 2. Coverage Summary

| Metric | Initial Baseline | Code Coverage Suite | Branch Coverage Suite | Target | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Line / Statement Coverage** | **38%** (20 missed) | **100%** (0 missed) | **100%** (0 missed) | $\ge 90\%$ | **Exceeded (100%)** |
| **Branch Coverage** | **32%** (6 partial) | **100%** (0 partial) | **100%** (0 partial) | $\ge 90\%$ | **Exceeded (100%)** |
| **Total Test Cases** | 2 tests | 13 tests | 31 tests | - | All Passed |

---

## 3. Test Files and Deliverables

* [`CodeCoverageTest_course_registration.py`](CodeCoverageTest_course_registration.py): 13 targeted tests verifying every statement in the application.
* [`CodeCoverageTest_course_registration_application.py`](CodeCoverageTest_course_registration_application.py): Exact naming alias per handout specification.
* [`BranchCoverageTest_course_registration.py`](BranchCoverageTest_course_registration.py): 31 exhaustive tests evaluating both True and False outcomes across every decision branch and boundary condition.
* [`BranchCoverageTest_course_registration_application.py`](BranchCoverageTest_course_registration_application.py): Exact naming alias per handout specification.
* [`test_course_registration.py`](test_course_registration.py): Standard runner including all test cases.
* [`code_coverage_report.txt`](code_coverage_report.txt) & [`code_coverage_terminal.png`](code_coverage_terminal.png): Terminal analysis output for line coverage.
* [`branch_coverage_report.txt`](branch_coverage_report.txt) & [`branch_coverage_terminal.png`](branch_coverage_terminal.png): Terminal analysis output for branch coverage.

---

## 4. Branch Analysis Matrix for `course_registration.py`

### 4.1 Function: `can_register(student_status, current_credits, course_credits, prerequisites_met)`
| Branch Condition | True Path Tested | False Path Tested | Test Function(s) |
| :--- | :--- | :--- | :--- |
| `student_status not in MAX_CREDITS` | Unknown status (`"alumni"`) raises `ValueError` | Valid statuses (`"regular"`, `"probation"`, `"honors"`) | `test_can_register_status_invalid_branch`, `test_can_register_regular_exact_boundary_branch` |
| `course_credits <= 0` | `0` or `-3` raises `ValueError` | `course_credits = 4` (> 0) | `test_can_register_credits_zero_branch`, `test_can_register_credits_negative_branch` |
| `not prerequisites_met` | `prerequisites_met = False` returns `"prerequisites missing"` | `prerequisites_met = True` | `test_can_register_prerequisites_missing_branch` |
| `current_credits + course_credits > MAX_CREDITS[status]` | Sum > Limit returns `"credit limit exceeded"` | Sum $\le$ Limit returns `"registered"` (tested at exact boundary and below limit) | `test_can_register_regular_limit_exceeded_branch`, `test_can_register_probation_limit_exceeded_branch`, `test_can_register_honors_limit_exceeded_branch`, `test_can_register_regular_exact_boundary_branch` |

### 4.2 Function: `waitlist_position(enrolled, capacity, waitlist_length)`
| Branch Condition | True Path Tested | False Path Tested | Test Function(s) |
| :--- | :--- | :--- | :--- |
| `capacity <= 0` | Capacity `0` or `-5` raises `ValueError` | Capacity `30` (> 0) | `test_waitlist_capacity_zero_branch`, `test_waitlist_capacity_negative_branch` |
| `enrolled < capacity` | `enrolled=29, capacity=30` returns `0` | `enrolled=30` (exact capacity) and `enrolled=35` (over capacity) | `test_waitlist_seat_available_branch`, `test_waitlist_exact_capacity_branch`, `test_waitlist_over_capacity_branch` |
| `waitlist_length >= 10` | Boundary `10` and `15` returns `-1` (waitlist full) | Boundary `9`, `4`, `0` returns `waitlist_length + 1` | `test_waitlist_full_exact_ten_branch`, `test_waitlist_full_greater_than_ten_branch`, `test_waitlist_under_ten_boundary_nine_branch`, `test_waitlist_under_ten_general_branch` |

### 4.3 Function: `late_fee(days_late, credits, has_waiver)`
| Branch Condition | True Path Tested | False Path Tested | Test Function(s) |
| :--- | :--- | :--- | :--- |
| `days_late <= 0` | `0` and `-4` returns `0` | Days late `> 0` | `test_late_fee_zero_days_branch`, `test_late_fee_negative_days_branch` |
| `has_waiver` | `has_waiver = True` returns `0` | `has_waiver = False` calculates fee | `test_late_fee_waiver_true_branch` |
| `days_late <= 7` | `7` (boundary) and `3` sets `fee = 500` | `8` (boundary) and `12` calculates `500 + (days - 7) * 100` | `test_late_fee_within_7_days_exact_boundary`, `test_late_fee_within_7_days_less_than_7`, `test_late_fee_beyond_7_days_boundary_eight`, `test_late_fee_beyond_7_days_without_surcharge` |
| `credits > 20` | `21`, `22`, `24` credits adds `+250` surcharge | `16`, `18`, `20` (boundary) leaves fee unchanged | `test_late_fee_within_7_days_with_extra_credits`, `test_late_fee_beyond_7_days_with_surcharge_uncapped`, `test_late_fee_exact_2000_cap_boundary` |
| `fee > 2000` | Fee calculated $> 2000$ (e.g. 2550) capped at `2000` | Fee $\le 2000$ (tested at exact boundary `2000` and below `1050`, `500`) | `test_late_fee_capped_at_2000_branch`, `test_late_fee_exact_2000_cap_boundary`, `test_late_fee_beyond_7_days_with_surcharge_uncapped` |

---

## 5. Execution Instructions

To reproduce the coverage analysis locally:

```bash
# 1. Run line coverage
coverage run -m pytest CodeCoverageTest_course_registration.py
coverage report -m

# 2. Run branch coverage
coverage run --branch -m pytest BranchCoverageTest_course_registration.py
coverage report -m
```

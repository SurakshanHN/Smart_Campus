import os
import sys

# optional heavy imports, warn if missing
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False

#  SHARED IN-MEMORY DATA STORE
students      = []          # list of dicts  – registration records
enrollments   = {}          # {student_name: [(course, credits), ...]}
event_sets    = {}          # {event_name: set_of_names}
student_ids   = []          # list of int IDs for sort/search demo

RECORDS_FILE  = "student_records.txt"
PERF_CSV      = "student_performance.csv"

#  HELPERS
def separator(title=""):
    width = 60
    print("\n" + "═" * width)
    if title:
        print(f"  {title}")
        print("─" * width)


def pause():
    input("\n  ↩  Press ENTER to return to menu...")


#  MODULE 1 – Student Registration & Grade Evaluation  (Lab 1)
def module_registration():
    separator("MODULE 1 · Student Registration & Grade Evaluation")

    while True:
        print("\n  [1] Register a new student")
        print("  [2] View all registered students")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            name  = input("  Enter student name : ").strip()
            if not name:
                print("  X Name cannot be empty.")
                continue
            try:
                score = float(input("  Enter exam score (0-100): "))
            except ValueError:
                print("  X Invalid score.")
                continue

            if score >= 90:
                grade, remark = "A", "Excellent"
            elif score >= 75:
                grade, remark = "B", "Very Good"
            elif score >= 60:
                grade, remark = "C", "Good"
            elif score >= 40:
                grade, remark = "D", "Average"
            else:
                grade, remark = "F", "Needs Improvement"

            student = {"name": name, "score": score, "grade": grade, "remark": remark}
            students.append(student)

            sid = 100 + len(students)
            student_ids.append(sid)
            student["id"] = sid

            print(f"\n  ── Student Report ──────────────")
            print(f"  Name   : {name}")
            print(f"  Score  : {score}")
            print(f"  Grade  : {grade}")
            print(f"  Remark : {remark}")
            print(f"  Assigned ID: {sid}")

        elif choice == "2":
            if not students:
                print("  (No students registered yet.)")
            else:
                print(f"\n  {'ID':<6} {'Name':<20} {'Score':<7} {'Grade':<6} Remark")
                print("  " + "-" * 55)
                for s in students:
                    print(f"  {s['id']:<6} {s['name']:<20} {s['score']:<7} {s['grade']:<6} {s['remark']}")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 2 – Course Enrollment Management  (Lab 2)
def module_enrollment():
    separator("MODULE 2 · Course Enrollment Management")
    MAX_COURSES = 5

    while True:
        print("\n  [1] Enroll courses for a student")
        print("  [2] View enrollment for a student")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            if not students:
                print("  X No students registered. Register a student first (Module 1).")
                continue
            name = input("  Enter student name: ").strip()
            found = any(s["name"].lower() == name.lower() for s in students)
            if not found:
                print("  X Student not found.")
                continue

            courses = enrollments.get(name, [])
            print(f"  Max courses: {MAX_COURSES}  |  Currently enrolled: {len(courses)}")

            while True:
                if len(courses) >= MAX_COURSES:
                    print("  X Maximum course limit reached!")
                    break

                course_name = input("  Enter course name (or 'done' to finish): ").strip()
                if course_name.lower() == "done":
                    break
                if not course_name:
                    print("  X Course name cannot be empty. Skipping...")
                    continue

                credits_raw = input("  Enter credit value: ").strip()
                if not credits_raw.isdigit():
                    print("  X Invalid credit value! Skipping entry...")
                    continue
                credits = int(credits_raw)
                if credits <= 0:
                    print("  X Credit must be positive! Skipping entry...")
                    continue

                courses.append((course_name, credits))
                print(f"  ✓ Course '{course_name}' with {credits} credits added.")

            enrollments[name] = courses

        elif choice == "2":
            name = input("  Enter student name: ").strip()
            courses = enrollments.get(name)
            if not courses:
                print(f"  (No enrollment found for '{name}'.)")
            else:
                print(f"\n  Enrollment Report for {name}")
                print("  " + "-" * 35)
                total_credits = 0
                for c, cr in courses:
                    print(f"  Course: {c:<25} Credits: {cr}")
                    total_credits += cr
                print(f"  Total Courses : {len(courses)}")
                print(f"  Total Credits : {total_credits}")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 3 – Student Record Management & Event Analysis  (Lab 3)
def module_records():
    separator("MODULE 3 · Student Record Management (Lists/Dicts/Sets)")

    while True:
        print("\n  [1] Add / update student grades")
        print("  [2] View all student records")
        print("  [3] Event participation analysis")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            name = input("  Enter student name: ").strip()
            # find or create record
            record = next((s for s in students if s["name"].lower() == name.lower()), None)
            if not record:
                print("  X Student not registered. Use Module 1 first.")
                continue
            raw = input("  Enter grades separated by spaces: ").strip()
            try:
                grades = [int(x) for x in raw.split()]
                record["grades"] = grades
                print(f"  ✓ Grades updated: {grades}")
            except ValueError:
                print("  X Invalid grades input.")

        elif choice == "2":
            if not students:
                print("  (No records available.)")
            else:
                print()
                for s in students:
                    print(f"  Name   : {s['name']}")
                    print(f"  Age    : {s.get('age', 'N/A')}")
                    print(f"  Grades : {s.get('grades', [])}")
                    avg = sum(s["grades"]) / len(s["grades"]) if s.get("grades") else "N/A"
                    print(f"  Avg    : {avg}")
                    print("  " + "-" * 30)

        elif choice == "3":
            print("\n  ── Event Participation Analysis ──")
            print("  Enter participants for two events (comma-separated names)")
            ev1_name = input("  Event A name: ").strip() or "Event A"
            ev1_members = set(x.strip() for x in input("  Participants: ").split(",") if x.strip())
            ev2_name = input("  Event B name: ").strip() or "Event B"
            ev2_members = set(x.strip() for x in input("  Participants: ").split(",") if x.strip())

            print(f"\n  Common ({ev1_name} ∩ {ev2_name})  : {ev1_members & ev2_members or '∅'}")
            print(f"  All    ({ev1_name} ∪ {ev2_name})  : {ev1_members | ev2_members}")
            print(f"  Only in {ev1_name}                : {ev1_members - ev2_members or '∅'}")
            print(f"  Only in {ev2_name}                : {ev2_members - ev1_members or '∅'}")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 4 – Sorting & Searching Student IDs  (Lab 4)
def _bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def _selection_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def _linear_search(arr, target):
    for i, v in enumerate(arr):
        if v == target:
            return i
    return -1


def _binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def module_sort_search():
    separator("MODULE 4 · Sorting & Searching Student IDs")

    while True:
        if not student_ids:
            print("  (No student IDs yet. Register students in Module 1.)")
        else:
            print(f"\n  Current IDs: {student_ids}")

        print("\n  [1] Add custom ID")
        print("  [2] Bubble Sort & display")
        print("  [3] Selection Sort & display")
        print("  [4] Search for an ID")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            try:
                sid = int(input("  Enter student ID: "))
                student_ids.append(sid)
                print(f"  ✓ ID {sid} added.")
            except ValueError:
                print("  X Invalid ID.")

        elif choice == "2":
            if not student_ids:
                print("  X No IDs to sort.")
                continue
            sorted_ids = _bubble_sort(student_ids)
            print(f"  Original       : {student_ids}")
            print(f"  Bubble Sorted  : {sorted_ids}")

        elif choice == "3":
            if not student_ids:
                print("  X No IDs to sort.")
                continue
            sorted_ids = _selection_sort(student_ids)
            print(f"  Original         : {student_ids}")
            print(f"  Selection Sorted : {sorted_ids}")

        elif choice == "4":
            if not student_ids:
                print("  X No IDs available.")
                continue
            try:
                target = int(input("  Enter ID to search: "))
            except ValueError:
                print("  X Invalid input.")
                continue

            sorted_ids = _bubble_sort(student_ids)

            li = _linear_search(sorted_ids, target)
            bi = _binary_search(sorted_ids, target)

            print(f"  Sorted list : {sorted_ids}")
            if li != -1:
                print(f"  Linear Search : ID {target} found at index {li}")
            else:
                print(f"  Linear Search : ID {target} not found")

            if bi != -1:
                print(f"  Binary Search : ID {target} found at index {bi}")
            else:
                print(f"  Binary Search : ID {target} not found")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 5 – Fee Calculation using Functions  (Lab 5)
def calculate_fee(tuition_fee, hostel_fee=0, transportation_fee=0):
    return tuition_fee + hostel_fee + transportation_fee


def module_fee():
    separator("MODULE 5 · Student Fee Calculation")

    while True:
        print("\n  [1] Calculate fee for a student")
        print("  [2] Show fee summary for all students")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            name = input("  Student name: ").strip()
            try:
                tuition   = float(input("  Tuition fee          : ₹"))
                hostel    = float(input("  Hostel fee   (0 = none): ₹") or 0)
                transport = float(input("  Transport fee (0 = none): ₹") or 0)
            except ValueError:
                print("  X Invalid amount.")
                continue

            total = calculate_fee(tuition, hostel, transport)

            print(f"\n  ── Fee Receipt for {name} ──")
            print(f"  Tuition       : ₹{tuition:,.0f}")
            print(f"  Hostel        : ₹{hostel:,.0f}")
            print(f"  Transportation: ₹{transport:,.0f}")
            print(f"  {'─'*30}")
            print(f"  TOTAL         : ₹{total:,.0f}")

            rec = next((s for s in students if s["name"].lower() == name.lower()), None)
            if rec:
                rec["fee"] = total

        elif choice == "2":
            fee_students = [s for s in students if "fee" in s]
            if not fee_students:
                print("  (No fee records yet.)")
            else:
                print(f"\n  {'Name':<22} Total Fee")
                print("  " + "-" * 35)
                for s in fee_students:
                    print(f"  {s['name']:<22} ₹{s['fee']:,.0f}")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 6 – File-based Academic Record Management  (Lab 6)
def module_file():
    separator("MODULE 6 · File-based Academic Records")

    while True:
        print("\n  [1] Write current student records to file")
        print("  [2] Read records from file")
        print("  [3] Generate report from file")
        print(f"  (File: {RECORDS_FILE})")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            if not students:
                print("  X No students to write.")
                continue
            with open(RECORDS_FILE, "w") as f:
                f.write("ID,Name,Score,Grade\n")
                for s in students:
                    f.write(f"{s['id']},{s['name']},{s['score']},{s['grade']}\n")
            print(f"  ✓ {len(students)} records written to '{RECORDS_FILE}'.")

        elif choice == "2":
            if not os.path.exists(RECORDS_FILE):
                print(f"  X File '{RECORDS_FILE}' not found. Write records first.")
                continue
            print(f"\n  Contents of '{RECORDS_FILE}':")
            print("  " + "-" * 40)
            with open(RECORDS_FILE, "r") as f:
                for line in f:
                    print("  " + line.strip())

        elif choice == "3":
            if not os.path.exists(RECORDS_FILE):
                print(f"  X File '{RECORDS_FILE}' not found. Write records first.")
                continue
            with open(RECORDS_FILE, "r") as f:
                lines = f.readlines()

            total, total_score, top_score, top_name = 0, 0, -1, ""
            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) < 3:
                    continue
                score = float(parts[2])
                total += 1
                total_score += score
                if score > top_score:
                    top_score = score
                    top_name  = parts[1]

            if total == 0:
                print("  (No data records found.)")
            else:
                print(f"\n  ── File Report ──────────────────")
                print(f"  Total Students : {total}")
                print(f"  Average Score  : {total_score / total:.2f}")
                print(f"  Top Student    : {top_name}  ({top_score})")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 7 – Directory Scanning & Exception Handling  (Lab 7)
class MissingFileOrFolderError(Exception):
    """Raised when a required file or folder is missing."""
    pass


def _scan_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Invalid directory path: {path}")

    print(f"\n  Scanning: {path}\n")
    empty_found = []

    for root, dirs, files in os.walk(path):
        level = root.replace(path, "").count(os.sep)
        indent = "    " * level
        print(f"  {indent}{os.path.basename(root)}/")
        sub_indent = "    " * (level + 1)
        for fname in files:
            print(f"  {sub_indent}{fname}")
        if not files and not dirs:
            empty_found.append(root)

    if empty_found:
        raise MissingFileOrFolderError(f"Empty folders detected: {', '.join(empty_found)}")


def module_directory():
    separator("MODULE 7 · Directory Scanning & Exception Handling")

    while True:
        print("\n  [1] Scan a directory")
        print("  [2] Create a sample project directory structure")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            path = input("  Enter directory path to scan: ").strip()
            try:
                _scan_directory(path)
            except FileNotFoundError as e:
                print(f"  X Error: {e}")
            except MissingFileOrFolderError as e:
                print(f"  ⚠  Custom Error: {e}")
            except Exception as e:
                print(f"  X Unexpected Error: {e}")

        elif choice == "2":
            base = "SampleProjects"
            os.makedirs(f"{base}/Student1", exist_ok=True)
            os.makedirs(f"{base}/Student2", exist_ok=True)
            os.makedirs(f"{base}/EmptyFolder", exist_ok=True)
            with open(f"{base}/Student1/report.docx", "w") as f:
                f.write("Sample report")
            with open(f"{base}/Student2/code.py", "w") as f:
                f.write("# Sample code")
            print(f"  ✓ Sample directory '{base}' created.")
            try:
                _scan_directory(base)
            except MissingFileOrFolderError as e:
                print(f"  ⚠  Custom Error: {e}")

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")


#  MODULE 8 – Performance Analytics (NumPy, Pandas, Matplotlib)  (Lab 8)
def _create_sample_csv():
    data = (
        "Name,Math,Science,English\n"
        "Arjun,85,78,90\n"
        "Meera,92,88,95\n"
        "Ravi,76,82,70\n"
        "Anita,89,91,85\n"
        "Kiran,60,74,68\n"
    )
    with open(PERF_CSV, "w") as f:
        f.write(data)
    print(f"  ✓ Sample CSV '{PERF_CSV}' created.")


def module_analytics():
    separator("MODULE 8 · Performance Analytics (NumPy / Pandas / Matplotlib)")

    if not ANALYTICS_AVAILABLE:
        print("\n  X NumPy, Pandas, or Matplotlib not installed.")
        print("    Run:  pip install numpy pandas matplotlib")
        pause()
        return

    while True:
        print("\n  [1] Create sample CSV file")
        print("  [2] Load & display raw data")
        print("  [3] Statistical summary (Pandas + NumPy)")
        print("  [4] Top performers per subject")
        print("  [5] Bar chart – average scores per subject")
        print("  [6] Bar chart – student-wise comparison")
        print(f"  (CSV: {PERF_CSV})")
        print("  [0] Back to main menu")
        choice = input("\n  Select: ").strip()

        if choice == "1":
            _create_sample_csv()

        elif choice in ("2", "3", "4", "5", "6"):
            if not os.path.exists(PERF_CSV):
                print(f"  X '{PERF_CSV}' not found. Create sample CSV first (option 1).")
                continue
            try:
                df = pd.read_csv(PERF_CSV)
            except Exception as e:
                print(f"  X Error reading CSV: {e}")
                continue

            if choice == "2":
                print("\n  Raw Data:")
                print(df.to_string(index=False))

            elif choice == "3":
                print("\n  Pandas Statistical Summary:")
                print(df.describe().to_string())
                scores = df[["Math", "Science", "English"]].to_numpy()
                print(f"\n  NumPy Mean   : {np.mean(scores, axis=0)}")
                print(f"  NumPy Median : {np.median(scores, axis=0)}")
                print(f"  NumPy StdDev : {np.std(scores, axis=0):.2f}" if scores.shape[1] == 1
                      else f"  NumPy StdDev : {np.std(scores, axis=0)}")

            elif choice == "4":
                for subj in ["Math", "Science", "English"]:
                    top = df.loc[df[subj].idxmax(), "Name"]
                    score = df[subj].max()
                    print(f"  Top in {subj:<10}: {top}  ({score})")

            elif choice == "5":
                subjects   = ["Math", "Science", "English"]
                means      = df[subjects].mean().values
                colors     = ["steelblue", "seagreen", "darkorange"]
                plt.figure(figsize=(7, 4))
                plt.bar(subjects, means, color=colors)
                plt.title("Average Scores per Subject")
                plt.xlabel("Subject")
                plt.ylabel("Average Score")
                plt.tight_layout()
                plt.show()

            elif choice == "6":
                subjects = ["Math", "Science", "English"]
                df.plot(x="Name", y=subjects, kind="bar", figsize=(8, 5))
                plt.title("Student Performance Comparison")
                plt.ylabel("Scores")
                plt.tight_layout()
                plt.show()

        elif choice == "0":
            break
        else:
            print("  X Invalid choice.")

#main program 
print("\n" + "╔" + "═" * 58 + "╗")
print("║   SMART CAMPUS INFORMATION SYSTEM                        ║")
print("║   Dayananda Sagar College of Engineering                 ║")
print("╚" + "═" * 58 + "╝")

while True:
    print("\n  ┌─ MAIN MENU ──────────────────────────────────────────┐")
    print("  │  [1]  Student Registration & Grade Evaluation        │")
    print("  │  [2]  Course Enrollment Management                   │")
    print("  │  [3]  Student Record Management (Data Structures)    │")
    print("  │  [4]  Sorting & Searching Student IDs                │")
    print("  │  [5]  Fee Calculation                                │")
    print("  │  [6]  File-based Academic Records                    │")
    print("  │  [7]  Directory Scanning & Exception Handling        │")
    print("  │  [8]  Performance Analytics (NumPy/Pandas/Matplotlib)│")
    print("  │  [0]  Exit                                           │")
    print("  └──────────────────────────────────────────────────────┘")

    option = input("\n  Enter option: ").strip()

    if   option == "1": module_registration()
    elif option == "2": module_enrollment()
    elif option == "3": module_records()
    elif option == "4": module_sort_search()
    elif option == "5": module_fee()
    elif option == "6": module_file()
    elif option == "7": module_directory()
    elif option == "8": module_analytics()
    elif option == "0":
        print("\n  Exiting......\n")
        sys.exit(0)
    else:
        print(" Invalid option. Please choose 0–8.")
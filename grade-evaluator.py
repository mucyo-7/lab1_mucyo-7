import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Check if the CSV is completely empty (no rows at all)
            rows = list(reader)
            if not rows:
                print("Error: The CSV file is empty. No grades to process.")
                sys.exit(1)

            for row in rows:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Core function that validates, calculates, and reports
    a student's academic standing from a list of assignment records.
    Each record is a dictionary with keys: assignment, group, score, weight.
    """
    print("\n--- Processing Grades ---")

    # -------------------------------------------------------
    # TODO a: GRADE VALIDATION
    # Before doing any calculations, we verify every score is
    # a valid percentage between 0 and 100 inclusive.
    # If any score is out of range, we stop immediately.
    # -------------------------------------------------------
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Error: '{item['assignment']}' has an invalid score of {item['score']}.")
            print("All scores must be between 0 and 100. Please fix the CSV and try again.")
            sys.exit(1)

    print("Validation passed: All scores are within the valid range (0-100).")

    # -------------------------------------------------------
    # TODO b: WEIGHT VALIDATION
    # The GPA formula only works if weights are correctly split:
    #   - All weights combined must equal exactly 100
    #   - Formative assignments must total exactly 60
    #   - Summative assignments must total exactly 40
    # We loop once and sort each weight into the right bucket.
    # -------------------------------------------------------
    total_weight = 0       # Accumulates weight of ALL assignments
    formative_weight = 0   # Accumulates weight of Formative assignments only
    summative_weight = 0   # Accumulates weight of Summative assignments only

    for item in data:
        total_weight += item['weight']

        if item['group'] == 'Formative':
            formative_weight += item['weight']
        elif item['group'] == 'Summative':
            summative_weight += item['weight']

    # Any mismatch means the data is incorrect — stop immediately
    if total_weight != 100:
        print(f"Error: Total weight is {total_weight}, but must equal 100.")
        sys.exit(1)
    if formative_weight != 60:
        print(f"Error: Formative weights sum to {formative_weight}, but must equal 60.")
        sys.exit(1)
    if summative_weight != 40:
        print(f"Error: Summative weights sum to {summative_weight}, but must equal 40.")
        sys.exit(1)

    print("Validation passed: All weights are correctly distributed (Total=100, Formative=60, Summative=40).")

    # -------------------------------------------------------
    # TODO c: GPA CALCULATION
    # Weighted grade = sum of (score x weight) for all assignments, divided by 100
    # GPA formula: (final_grade / 100) * 5.0
    # We also track formative and summative scores separately for TODO d.
    # -------------------------------------------------------
    total_weighted_score = 0       # Sum of (score x weight) for ALL assignments
    formative_weighted_score = 0   # Sum of (score x weight) for Formative only
    summative_weighted_score = 0   # Sum of (score x weight) for Summative only

    for item in data:
        weighted = item['score'] * item['weight']
        total_weighted_score += weighted

        if item['group'] == 'Formative':
            formative_weighted_score += weighted
        elif item['group'] == 'Summative':
            summative_weighted_score += weighted

    # Final grade is the total weighted score divided by 100
    final_grade = total_weighted_score / 100
    gpa = (final_grade / 100) * 5.0

    # -------------------------------------------------------
    # TODO d: PASS/FAIL DETERMINATION
    # A student passes ONLY if they score >= 50% in BOTH
    # formative AND summative categories independently.
    # Scoring 50% overall is NOT enough on its own.
    # -------------------------------------------------------

    # Divide each group's weighted score by that group's total weight
    # to get the actual percentage scored within that category
    formative_percentage = formative_weighted_score / formative_weight
    summative_percentage = summative_weighted_score / summative_weight

    # Both conditions must be true to pass
    passed = formative_percentage >= 50 and summative_percentage >= 50

    # -------------------------------------------------------
    # TODO e: RESUBMISSION LOGIC
    # Find all failed formative assignments (score < 50).
    # Among those, find the highest weight.
    # All failed formatives that share that highest weight
    # are eligible for resubmission.
    # -------------------------------------------------------

    # Filter: only formative assignments where score is below 50
    failed_formatives = [
        item for item in data
        if item['group'] == 'Formative' and item['score'] < 50
    ]

    resubmit_candidates = []

    if failed_formatives:
        # Find the highest weight among failed formatives
        max_weight = max(item['weight'] for item in failed_formatives)

        # All failed formatives that share this highest weight are eligible
        resubmit_candidates = [
            item for item in failed_formatives
            if item['weight'] == max_weight
        ]

    # -------------------------------------------------------
    # TODO f: PRINT FINAL DECISION AND RESUBMISSION OPTIONS
    # Display a clean summary of the student's results.
    # -------------------------------------------------------
    print("\n========== GRADE REPORT ==========")
    print(f"Formative Score:   {formative_percentage:.2f}%")
    print(f"Summative Score:   {summative_percentage:.2f}%")
    print(f"Final Grade:       {final_grade:.2f}%")
    print(f"GPA:               {gpa:.2f} / 5.0")
    print("==================================")

    # Print PASSED or FAILED
    if passed:
        print("\nFinal Status: PASSED")
    else:
        print("\nFinal Status: FAILED")

    # Print resubmission info
    print("\n--- Resubmission Eligibility ---")
    if not failed_formatives:
        print("No failed formative assignments. No resubmission needed.")
    elif resubmit_candidates:
        print("The following formative assignment(s) are eligible for resubmission:")
        for item in resubmit_candidates:
            print(f"  - {item['assignment']} (Score: {item['score']}%, Weight: {item['weight']})")
    print("==================================\n")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
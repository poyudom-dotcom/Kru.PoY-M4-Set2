import os
import subprocess

TEST_CASES = {
    "Examination_1": [
        {"input": "0\n", "expected": "32"},
        {"input": "100\n", "expected": "212"},
        {"input": "37\n", "expected": "98.6"}
    ],
    "Examination_2": [
        {"input": "18\n", "expected": "Eligible"},
        {"input": "15\n", "expected": "Not Eligible"}
    ],
    "Examination_3": [
        {"input": "5\n", "expected": "Positive"},
        {"input": "-3\n", "expected": "Negative"},
        {"input": "0\n", "expected": "Positive"}
    ],
    "Examination_4": [
        {"input": "2500\n", "expected": "2300"},
        {"input": "1500\n", "expected": "1400"},
        {"input": "500\n", "expected": "500"}
    ],
    "Examination_5": [
        {"input": "50\n", "expected": "Normal"},
        {"input": "80\n", "expected": "Fast"},
        {"input": "110\n", "expected": "Too Fast"}
    ]
}

def is_equal(actual, expected):
    clean_actual = actual.strip().lower()
    clean_expected = expected.strip().lower()
    
    if clean_actual == clean_expected:
        return True
        
    try:
        if float(clean_actual) == float(clean_expected):
            return True
    except ValueError:
        pass
        
    return False

def run_tests():
    all_passed = True
    
    for file_name, cases in TEST_CASES.items():
        py_file = f"{file_name}.py"
        if not os.path.exists(py_file):
            continue

        print(f"\n--- Testing {py_file} ---")
        for i, case in enumerate(cases, 1):
            try:
                process = subprocess.Popen(
                    ["python", py_file],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                stdout, stderr = process.communicate(input=case["input"])
                
                if is_equal(stdout, case["expected"]):
                    print(f"  Test Case {i}: PASSED ✅")
                else:
                    got_clean = stdout.strip()
                    print(f"  Test Case {i}: FAILED ❌ (Got: '{got_clean}', Expected: '{case['expected']}')")
                    all_passed = False
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"  Test Case {i}: FAILED ❌ (Timeout - โค้ดติด Infinite Loop)")
                all_passed = False
            except Exception as e:
                print(f"  Test Case {i}: ERROR ❌ ({str(e)})")
                all_passed = False

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    run_tests()

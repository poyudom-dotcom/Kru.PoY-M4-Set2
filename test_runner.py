import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อสำหรับ Kru.PoY-M4-Set2 (ข้อละ 4 เคส = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: แปลงอุณหภูมิ เซลเซียส เป็น ฟาเรนไฮต์ (F = C * 1.8 + 32)
    "Examination_1.py": [
        (["0"], "32.0"),
        (["100"], "212.0"),
        (["37"], "98.6"),
        (["-40"], "-40.0")
    ],
    # ข้อ 2: ตรวจสอบสิทธิ์เลือกตั้ง (>=18 Eligible, <18 Not Eligible)
    "Examination_2.py": [
        (["20"], "Eligible"),
        (["18"], "Eligible"),
        (["17"], "Not Eligible"),
        (["10"], "Not Eligible")
    ],
    # ข้อ 3: ตรวจสอบจำนวนบวก หรือ จำนวนลบ (>=0 Positive, <0 Negative)
    "Examination_3.py": [
        (["5"], "Positive"),
        (["0"], "Positive"),
        (["-1"], "Negative"),
        (["-10"], "Negative")
    ],
    # ข้อ 4: คำนวณราคาสินค้าหลังหักส่วนลด (>=2000 ลด 200, >=1000 ลด 100, <1000 ไม่ลด)
    "Examination_4.py": [
        (["2500"], "2300"),
        (["2000"], "1800"),
        (["1200"], "1100"),
        (["800"], "800")
    ],
    # ข้อ 5: ประเมินความเร็วรถยนต์ (<=60 Normal, 61-90 Fast, >90 Too Fast)
    "Examination_5.py": [
        (["50"], "Normal"),
        (["60"], "Normal"),
        (["75"], "Fast"),
        (["100"], "Too Fast")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(base_name):
        return base_name
    elif os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name.replace(".py", "")):
        return base_name.replace(".py", "")
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งข้อความและทศนิยม"""
    if actual is None:
        return False
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean.lower() == expected_clean.lower():
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # ยืดหยุ่นคะแนน: ผ่าน 1 เคส = 1 คะแนน
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม (Set 2)

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()

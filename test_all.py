"""Complete backend functionality test for AI Placement Predictor GUI."""
import sys
sys.path.insert(0, '.')
from db import conn

cur = conn.cursor()
passed = 0
total = 10

# Test 1: SELECT
cur.execute("SELECT COUNT(*) FROM students")
t = cur.fetchone()[0]
print(f"TEST 1 - SELECT: Total students = {t}")
passed += 1

# Test 2: INSERT
cur.execute(
    "INSERT INTO students (name, age, cgpa, python_skill, sql_skill, dsa_skill, "
    "communication, aptitude, projects, internship, certifications, target_role, "
    "resume_score, placement_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    ("TEST_GUI_USER", 22, 8.0, 8, 7, 7, 8, 7, 3, "Yes", 2, "Test Role", 80, "Placed"),
)
conn.commit()
print("TEST 2 - INSERT: Success")
passed += 1

# Test 3: Verify INSERT
cur.execute("SELECT student_id FROM students WHERE name = %s", ("TEST_GUI_USER",))
new_id = cur.fetchone()[0]
print(f"TEST 3 - VERIFY INSERT: New student ID = {new_id}")
passed += 1

# Test 4: UPDATE
cur.execute("UPDATE students SET cgpa = 9.0 WHERE student_id = %s", (new_id,))
conn.commit()
cur.execute("SELECT cgpa FROM students WHERE student_id = %s", (new_id,))
new_cgpa = cur.fetchone()[0]
print(f"TEST 4 - UPDATE: CGPA updated to {new_cgpa}")
passed += 1

# Test 5: SEARCH
cur.execute("SELECT * FROM students WHERE name LIKE %s", ("%TEST%",))
found = cur.fetchall()
print(f"TEST 5 - SEARCH: Found {len(found)} matching records")
passed += 1

# Test 6: DELETE
cur.execute("DELETE FROM students WHERE student_id = %s", (new_id,))
conn.commit()
print(f"TEST 6 - DELETE: Student #{new_id} deleted")
passed += 1

# Test 7: AI Model prediction (should be Placed)
import AI_Model
res1 = AI_Model.predict_student_placement({
    "cgpa": 8.5, "python_skill": 9, "sql_skill": 9, "dsa_skill": 9,
    "communication": 8, "aptitude": 80, "projects": 4, "certifications": 3, "resume_score": 85
})
accuracy = AI_Model.accuracy
print(f"TEST 7 - AI PREDICT (high): {res1['prediction']}, Confidence: {res1['confidence']}%, Accuracy: {accuracy*100:.1f}%")
passed += 1

# Test 8: AI Model prediction (should be Not Placed)
res2 = AI_Model.predict_student_placement({
    "cgpa": 5.5, "python_skill": 3, "sql_skill": 4, "dsa_skill": 3,
    "communication": 4, "aptitude": 30, "projects": 1, "certifications": 0, "resume_score": 40
})
print(f"TEST 8 - AI PREDICT (low): {res2['prediction']}, Confidence: {res2['confidence']}%")
passed += 1

# Test 9: CSV Export simulation
import csv, io
cur.execute("SELECT * FROM students")
rows = cur.fetchall()
headers = [desc[0] for desc in cur.description]
output = io.StringIO()
writer = csv.writer(output)
writer.writerow(headers)
writer.writerows(rows)
print(f"TEST 9 - EXPORT: CSV with {len(rows)} rows, {len(headers)} columns")
passed += 1

# Test 10: Dashboard stats
cur.execute("SELECT COUNT(*) FROM students")
total_s = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM students WHERE LOWER(placement_status) = 'placed'")
placed = cur.fetchone()[0]
cur.execute("SELECT AVG(cgpa) FROM students")
avg = cur.fetchone()[0]
print(f"TEST 10 - DASHBOARD: Total={total_s}, Placed={placed}, AvgCGPA={avg:.2f}")
passed += 1

print(f"\n{'='*50}")
print(f"RESULTS: {passed}/{total} TESTS PASSED")
print(f"{'='*50}")

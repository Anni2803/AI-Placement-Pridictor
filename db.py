import os
import csv
import pymysql as pym

conn = None

def init_db():
    global conn
    try:
        # First connect without database to ensure database exists
        base_conn = pym.connect(
            host="localhost",
            user="root",
            password="anjali123"
        )
        with base_conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS placement_system")
        base_conn.close()

        # Connect to placement_system
        conn = pym.connect(
            host="localhost",
            user="root",
            password="anjali123",
            database="placement_system"
        )

        print("Database Connected Successfully")

        # Ensure table exists
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                cgpa DECIMAL(3,2) NOT NULL,
                python_skill INT NOT NULL,
                sql_skill INT NOT NULL,
                dsa_skill INT NOT NULL,
                communication INT NOT NULL,
                aptitude INT NOT NULL,
                projects INT DEFAULT 0,
                internship VARCHAR(3) NOT NULL,
                certifications INT DEFAULT 0,
                target_role VARCHAR(50) NOT NULL,
                resume_score INT DEFAULT 0,
                placement_status VARCHAR(20) NOT NULL
            )
            """)
            conn.commit()

            # Seed data if table is empty
            cur.execute("SELECT COUNT(*) FROM students")
            count = cur.fetchone()[0]

            if count == 0:
                indian_csv = os.path.join(os.path.dirname(__file__), "dataset", "Indian_Student_Placement_Dataset_2025.csv")
                students_csv = os.path.join(os.path.dirname(__file__), "dataset", "students.csv")

                first_names = ["Aarav", "Anjali", "Rohan", "Priya", "Rahul", "Neha", "Vikram", "Sneha", "Aditya", "Kavya", "Siddharth", "Pooja", "Amit", "Riya", "Karan", "Ishita"]
                last_names = ["Sharma", "Verma", "Mehta", "Patel", "Singh", "Kumar", "Gupta", "Joshi", "Nair", "Reddy", "Rao", "Deshmukh", "Chopra", "Bhat"]

                if os.path.exists(indian_csv):
                    with open(indian_csv, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        insert_query = """
                        INSERT INTO students
                        (name, age, cgpa, python_skill, sql_skill, dsa_skill,
                        communication, aptitude, projects, internship,
                        certifications, target_role, resume_score, placement_status)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        for idx, row in enumerate(reader):
                            fn = first_names[idx % len(first_names)]
                            ln = last_names[(idx // len(first_names)) % len(last_names)]
                            name = f"{fn} {ln}"

                            age = int(row["age"])
                            cgpa = float(row["cgpa"])
                            coding = int(row["coding_skills"])
                            py_skill = coding
                            sql_skill = coding
                            dsa_skill = coding
                            comm_skill = int(row["communication_skills"])
                            apt_val = float(row["aptitude_score"])
                            aptitude = int(round(apt_val / 10.0)) if apt_val > 10 else int(apt_val)
                            projects = int(row["projects"])
                            internships_cnt = int(row["internships"])
                            internship = "Yes" if internships_cnt > 0 else "No"
                            certifications = int(row["certifications"])
                            branch = row.get("branch", "Computer Science")
                            target_role = f"{branch} Engineer" if "Engineer" not in branch else branch
                            resume_score = min(100, int(round(cgpa * 7.5 + coding * 2.0 + projects * 1.5)))
                            placement_status = "Placed" if int(row["placed"]) == 1 else "Not Placed"

                            cur.execute(insert_query, (
                                name, age, cgpa, py_skill, sql_skill, dsa_skill,
                                comm_skill, aptitude, projects, internship,
                                certifications, target_role, resume_score, placement_status
                            ))
                            if idx >= 999:  # Seed top 1,000 records for fast load & performance
                                break

                        conn.commit()
                        print("1,000 student records from Indian_Student_Placement_Dataset_2025.csv seeded into MySQL.")

                elif os.path.exists(students_csv):
                    with open(students_csv, "r", encoding="utf-8") as f:
                        reader = csv.DictReader(f)
                        insert_query = """
                        INSERT INTO students
                        (name, age, cgpa, python_skill, sql_skill, dsa_skill,
                        communication, aptitude, projects, internship,
                        certifications, target_role, resume_score, placement_status)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        for row in reader:
                            cur.execute(insert_query, (
                                row["name"], int(row["age"]), float(row["cgpa"]),
                                int(row["python_skill"]), int(row["sql_skill"]), int(row["dsa_skill"]),
                                int(row["communication"]), int(row["aptitude"]), int(row["projects"]),
                                row["internship"], int(row["certifications"]), row["target_role"],
                                int(row["resume_score"]), row["placement_status"]
                            ))
                        conn.commit()
                        print("Initial student dataset seeded successfully into MySQL.")

    except Exception as e:
        print("Connection Failed")
        print(e)

init_db()
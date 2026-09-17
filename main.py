from db import conn

cur = conn.cursor()

while True:

    print("\n" + "=" * 50)
    print(" AI Placement Predictor & Skill Improvement System ")
    print("=" * 50)

    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        print("Please enter only numbers.")
        continue

    # -------------------- ADD STUDENT --------------------

    if choice == 1:

        name = input("Enter Name : ")
        age = int(input("Enter Age : "))
        cgpa = float(input("Enter CGPA : "))
        python_skill = int(input("Enter Python Skill : "))
        sql_skill = int(input("Enter SQL Skill : "))
        dsa_skill = int(input("Enter DSA Skill : "))
        communication = int(input("Enter Communication Skill : "))
        aptitude = int(input("Enter Aptitude : "))
        projects = int(input("Enter Number of Projects : "))
        internship = input("Internship (Yes/No) : ")
        certifications = int(input("Enter Certifications : "))
        target_role = input("Enter Target Role : ")
        resume_score = int(input("Enter Resume Score : "))
        placement_status = input("Placement Status (Placed/Not Placed) : ")

        query = """
        INSERT INTO students
        (name, age, cgpa, python_skill, sql_skill, dsa_skill,
        communication, aptitude, projects, internship,
        certifications, target_role, resume_score, placement_status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            name,
            age,
            cgpa,
            python_skill,
            sql_skill,
            dsa_skill,
            communication,
            aptitude,
            projects,
            internship,
            certifications,
            target_role,
            resume_score,
            placement_status
        )

        cur.execute(query, values)
        conn.commit()

        print("\nStudent Added Successfully ✅")
        input("\nPress Enter to continue...")

    # -------------------- VIEW STUDENTS --------------------

    elif choice == 2:

        cur.execute("SELECT * FROM students")

        data = cur.fetchall()

        print("\nStudent Records")
        print("-" * 50)

        for i in data:

            print("ID :", i[0])
            print("Name :", i[1])
            print("Age :", i[2])
            print("CGPA :", i[3])
            print("Python Skill :", i[4])
            print("SQL Skill :", i[5])
            print("DSA Skill :", i[6])
            print("Communication :", i[7])
            print("Aptitude :", i[8])
            print("Projects :", i[9])
            print("Internship :", i[10])
            print("Certifications :", i[11])
            print("Target Role :", i[12])
            print("Resume Score :", i[13])
            print("Placement Status :", i[14])
            print("-" * 50)

        input("\nPress Enter to continue...")
        # -------------------- SEARCH STUDENT --------------------

    elif choice == 3:

        student_id = int(input("Enter Student ID : "))

        cur.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        data = cur.fetchone()

        if data:

            print("\nStudent Found")
            print("-" * 50)

            print("ID :", data[0])
            print("Name :", data[1])
            print("Age :", data[2])
            print("CGPA :", data[3])
            print("Python Skill :", data[4])
            print("SQL Skill :", data[5])
            print("DSA Skill :", data[6])
            print("Communication :", data[7])
            print("Aptitude :", data[8])
            print("Projects :", data[9])
            print("Internship :", data[10])
            print("Certifications :", data[11])
            print("Target Role :", data[12])
            print("Resume Score :", data[13])
            print("Placement Status :", data[14])

        else:
            print("Student Not Found")

        input("\nPress Enter to continue...")

    # -------------------- UPDATE STUDENT --------------------

    elif choice == 4:

        student_id = int(input("Enter Student ID to Update : "))

        cur.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        data = cur.fetchone()

        if data:

            print("\nEnter New Details")

            name = input("Enter Name : ")
            age = int(input("Enter Age : "))
            cgpa = float(input("Enter CGPA : "))
            python_skill = int(input("Enter Python Skill : "))
            sql_skill = int(input("Enter SQL Skill : "))
            dsa_skill = int(input("Enter DSA Skill : "))
            communication = int(input("Enter Communication Skill : "))
            aptitude = int(input("Enter Aptitude : "))
            projects = int(input("Enter Number of Projects : "))
            internship = input("Internship (Yes/No) : ")
            certifications = int(input("Enter Certifications : "))
            target_role = input("Enter Target Role : ")
            resume_score = int(input("Enter Resume Score : "))
            placement_status = input("Placement Status (Placed/Not Placed) : ")

            query = """
            UPDATE students
            SET
                name=%s,
                age=%s,
                cgpa=%s,
                python_skill=%s,
                sql_skill=%s,
                dsa_skill=%s,
                communication=%s,
                aptitude=%s,
                projects=%s,
                internship=%s,
                certifications=%s,
                target_role=%s,
                resume_score=%s,
                placement_status=%s
            WHERE student_id=%s
            """

            values = (
                name,
                age,
                cgpa,
                python_skill,
                sql_skill,
                dsa_skill,
                communication,
                aptitude,
                projects,
                internship,
                certifications,
                target_role,
                resume_score,
                placement_status,
                student_id
            )

            cur.execute(query, values)
            conn.commit()

            print("\nStudent Updated Successfully ")

        else:
            print("Student Not Found")

        input("\nPress Enter to continue...")
        # -------------------- DELETE STUDENT --------------------

    elif choice == 5:

        student_id = int(input("Enter Student ID to Delete : "))

        cur.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        data = cur.fetchone()

        if data:

            confirm = input("Are you sure? (yes/no) : ")

            if confirm.lower() == "yes":

                cur.execute(
                    "DELETE FROM students WHERE student_id = %s",
                    (student_id,)
                )

                conn.commit()

                print("\nStudent Deleted Successfully ✅")

            else:
                print("\nDelete Cancelled.")

        else:
            print("Student Not Found")

        input("\nPress Enter to continue...")

    # -------------------- EXIT --------------------

    elif choice == 6:

        print("\nThank You 😊")
        print("Exiting Program...")
        break

    # -------------------- INVALID CHOICE --------------------

    else:

        print("\nInvalid Choice!")
        input("\nPress Enter to continue...")
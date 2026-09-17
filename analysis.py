import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from db import conn

if __name__ == "__main__":
    query = "SELECT * FROM students"

    df = pd.read_sql(query, conn)

    print(df)

    print("\n" + "=" * 50)
    print("DATA ANALYSIS")
    print("=" * 50)

    print("Total Students :", len(df))

    print("Average CGPA :", round(df["cgpa"].mean(), 2))

    print("Highest CGPA :", df["cgpa"].max())

    print("Lowest CGPA :", df["cgpa"].min())

    print("Average Resume Score :", round(df["resume_score"].mean(), 2))

    print("Highest Resume Score :", df["resume_score"].max())

    print("Lowest Resume Score :", df["resume_score"].min())

    print("Placed Students :",
          len(df[df["placement_status"] == "Placed"]))

    print("Not Placed Students :",
          len(df[df["placement_status"] == "Not Placed"]))

    cgpa = np.array(df["cgpa"])

    print("\nNUMPY ANALYSIS")
    print("=" * 50)

    print("Mean CGPA :", np.mean(cgpa))
    print("Median CGPA :", np.median(cgpa))
    print("Standard Deviation :", round(np.std(cgpa), 2))

    #----------------bar graph(Different skills ka comparison karne ke liye)------------


    skills = ["Python", "SQL", "DSA", "Communication", "Aptitude"]

    avg = [
        df["python_skill"].mean(),
        df["sql_skill"].mean(),
        df["dsa_skill"].mean(),
        df["communication"].mean(),
        df["aptitude"].mean()
    ]

    plt.figure(figsize=(6,4))
    plt.bar(skills, avg)
    plt.title("Average Skill Scores")
    plt.xlabel("Skills")
    plt.ylabel("Average Score")
    plt.savefig("graphs/average_skills.png")
    plt.show()

    #-------------pii chart(Kisi category ka percentage dikhane ke liye)--------------------------

    placement = df["placement_status"].value_counts()

    plt.figure(figsize=(5,5))

    plt.pie(
        placement,
        labels=placement.index,
        autopct="%1.1f%%"
    )

    plt.title("Placement Status")
    plt.savefig("graphs/placement_status.png")
    plt.show()

    #----------histogram graph(Data kis range me kitna hai, ye dekhne ke liye)-----------------

    plt.figure(figsize=(6,4))

    plt.hist(df["cgpa"], bins=5)

    plt.title("CGPA Distribution")
    plt.xlabel("CGPA")
    plt.ylabel("Number of Students")
    plt.savefig("graphs/cgpa_distribution.png")
    plt.show()


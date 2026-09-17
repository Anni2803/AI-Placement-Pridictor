import pandas as pd

# -------------------- Load Dataset --------------------

df = pd.read_csv(
    "dataset/Indian_Student_Placement_Dataset_2025.csv"
)

print("Dataset Loaded Successfully")
print("Total Students :", len(df))

# -------------------- Dataset Information --------------------

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nPlacement Distribution:")
print(df["placed"].value_counts())

# -------------------- Feature Selection --------------------

features = [
    "age",
    "cgpa",
    "backlogs",
    "internships",
    "certifications",
    "coding_skills",
    "communication_skills",
    "aptitude_score",
    "projects"
]

X = df[features]
y = df["placed"]

print("\nFeatures Selected:")
print(features)

# -------------------- Train Test Split --------------------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing Samples :", len(X_test))

# -------------------- Machine Learning Pipeline --------------------

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ))
])

# -------------------- Train Model --------------------

model.fit(X_train, y_train)

print("\nAI Model Trained Successfully")

# -------------------- Test Prediction --------------------

prediction = model.predict(X_test)

# -------------------- Accuracy --------------------

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, prediction)

print("\nTest Accuracy :",
      round(accuracy * 100, 2), "%")

# -------------------- 5-Fold Cross Validation --------------------

from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

print("\n5-Fold Cross Validation Scores:")

for i, score in enumerate(cv_scores, start=1):
    print(
        f"Fold {i} Accuracy :",
        round(score * 100, 2),
        "%"
    )

print(
    "\nAverage Cross Validation Accuracy :",
    round(cv_scores.mean() * 100, 2),
    "%"
)
# -------------------- Detailed Model Evaluation --------------------

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

print("\nClassification Report:")
print(classification_report(y_test, prediction))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, prediction))

# -------------------- Helper Function for Programmatic Prediction --------------------

def predict_student_placement(data):
    """
    Accepts student data as a dict or DataFrame, formats features,
    and returns a dict containing prediction result, confidence, and recommendations.
    """
    if isinstance(data, dict):
        age = int(data.get("age", 21))
        cgpa = float(data.get("cgpa", 0.0))
        backlogs = int(data.get("backlogs", 0))

        # Handle internship representation
        internships_val = data.get("internships", data.get("internship", 0))
        if isinstance(internships_val, str):
            internships = 1 if internships_val.strip().lower() in ("yes", "1", "true") else 0
        else:
            internships = int(internships_val)

        certifications = int(data.get("certifications", 0))

        # Handle coding skills (if individual sub-skills are passed, calculate average)
        if "coding_skills" in data:
            coding_skills = float(data["coding_skills"])
        else:
            py = float(data.get("python_skill", 5))
            sql = float(data.get("sql_skill", 5))
            dsa = float(data.get("dsa_skill", 5))
            coding_skills = round((py + sql + dsa) / 3.0, 2)

        communication_skills = float(data.get("communication_skills", data.get("communication", 5)))

        aptitude_val = float(data.get("aptitude_score", data.get("aptitude", 50)))
        aptitude_score = aptitude_val * 10 if aptitude_val <= 10 else aptitude_val

        projects = int(data.get("projects", 0))

        sample_df = pd.DataFrame([{
            "age": age,
            "cgpa": cgpa,
            "backlogs": backlogs,
            "internships": internships,
            "certifications": certifications,
            "coding_skills": coding_skills,
            "communication_skills": communication_skills,
            "aptitude_score": aptitude_score,
            "projects": projects
        }])
    elif isinstance(data, pd.DataFrame):
        sample_df = data
    else:
        sample_df = pd.DataFrame(data, columns=features)

    # Prediction
    pred_val = model.predict(sample_df)[0]
    status_str = "Placed" if pred_val == 1 else "Not Placed"

    # Probability / Confidence
    try:
        prob = model.predict_proba(sample_df)[0]
        class_idx = list(model.classes_).index(pred_val)
        confidence_pct = round(prob[class_idx] * 100, 2)
    except Exception:
        confidence_pct = 85.0

    # Skill Suggestions
    suggestions = []
    c_skill = sample_df.iloc[0]["coding_skills"]
    comm_skill = sample_df.iloc[0]["communication_skills"]
    apt_score = sample_df.iloc[0]["aptitude_score"]
    cgpa_val = sample_df.iloc[0]["cgpa"]
    intern_val = sample_df.iloc[0]["internships"]
    cert_val = sample_df.iloc[0]["certifications"]
    proj_val = sample_df.iloc[0]["projects"]
    backlog_val = sample_df.iloc[0]["backlogs"]

    if c_skill < 7:
        suggestions.append("Improve coding/programming skills (Python, SQL, DSA)")
    if comm_skill < 7:
        suggestions.append("Enhance communication and interview presentation skills")
    if apt_score < 70:
        suggestions.append("Practice quantitative and logical aptitude questions")
    if cgpa_val < 7.5:
        suggestions.append("Aim to elevate academic CGPA score")
    if intern_val < 1:
        suggestions.append("Try to complete at least one practical internship")
    if cert_val < 2:
        suggestions.append("Earn relevant technical certifications")
    if proj_val < 2:
        suggestions.append("Build more practical portfolio projects")
    if backlog_val > 0:
        suggestions.append("Clear any pending academic backlogs")

    if not suggestions:
        suggestions.append("Great! Profile is well prepared for placements.")

    return {
        "prediction": status_str,
        "status_code": int(pred_val),
        "confidence": confidence_pct,
        "suggestions": suggestions
    }


# -------------------- Live CLI Placement Prediction --------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("LIVE PLACEMENT PREDICTION")
    print("=" * 50)

    try:
        age = int(input("Enter Age : "))
        cgpa = float(input("Enter CGPA : "))
        backlogs = int(input("Enter Backlogs : "))
        internships = int(input("Enter Number of Internships : "))
        certifications = int(input("Enter Number of Certifications : "))
        coding_skills = int(input("Enter Coding Skill (1-10) : "))
        communication_skills = int(input("Enter Communication Skill (1-10) : "))
        aptitude_score = int(input("Enter Aptitude Score (0-100) : "))
        projects = int(input("Enter Number of Projects : "))

        res = predict_student_placement({
            "age": age, "cgpa": cgpa, "backlogs": backlogs,
            "internships": internships, "certifications": certifications,
            "coding_skills": coding_skills, "communication_skills": communication_skills,
            "aptitude_score": aptitude_score, "projects": projects
        })

        print("\n" + "-" * 40)
        print("Prediction :", res["prediction"])
        print("Placement Probability :", res["confidence"], "%")
        print("-" * 40)

        print("\nSkill Improvement Suggestions:")
        for s in res["suggestions"]:
            print("-", s)

    except ValueError:
        print("\nInvalid input! Please enter numeric values correctly.")
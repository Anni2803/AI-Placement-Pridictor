import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

import AI_Model
from gui_views.styles import COLORS, FONTS


class PredictionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(10, 20))
        self.container.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 10))

        title = ctk.CTkLabel(
            self.header_frame,
            text="AI Placement Predictor",
            font=FONTS["title"],
            text_color=COLORS["text_primary"],
            anchor="w",
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            self.header_frame,
            text="Machine Learning Decision Tree Prediction Model",
            font=FONTS["subtitle"],
            text_color=COLORS["text_secondary"],
            anchor="w",
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        self.create_accuracy_banner()
        self.render_inputs_form()

        self.result_container = ctk.CTkFrame(self.container, fg_color="transparent")
        self.result_container.grid(row=3, column=0, sticky="ew", pady=(20, 10))
        self.result_container.grid_columnconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Accuracy banner — uses pack only (no .place with height)
    # ------------------------------------------------------------------
    def create_accuracy_banner(self):
        acc = getattr(AI_Model, "accuracy", None)

        banner = ctk.CTkFrame(
            self.container,
            fg_color=COLORS["bg_card"],
            corner_radius=10,
            border_color=COLORS["border"],
            border_width=1,
        )
        banner.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=2)

        banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
        banner_inner.pack(fill="x", padx=15, pady=12)

        dot = ctk.CTkFrame(
            banner_inner, width=10, height=10,
            fg_color=COLORS["success"], corner_radius=5,
        )
        dot.pack(side="left", padx=(0, 10))

        if acc is not None:
            acc_pct = acc * 100 if acc <= 1.0 else acc
            banner_text = f"AI model loaded successfully.  Training Test Accuracy: {acc_pct:.2f}%"
        else:
            banner_text = "AI model loaded. Accuracy could not be calculated (insufficient data)."

        lbl = ctk.CTkLabel(
            banner_inner,
            text=banner_text,
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"],
        )
        lbl.pack(side="left")

    # ------------------------------------------------------------------
    # Input form — 9 features matching the existing Decision Tree model
    # ------------------------------------------------------------------
    def render_inputs_form(self):
        self.form_card = ctk.CTkFrame(
            self.container,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_color=COLORS["border"],
            border_width=1,
        )
        self.form_card.grid(row=1, column=0, sticky="ew", pady=10, padx=2)
        self.form_card.grid_columnconfigure(0, weight=1)
        self.form_card.grid_columnconfigure(1, weight=1)

        col_left = ctk.CTkFrame(self.form_card, fg_color="transparent")
        col_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        col_left.grid_columnconfigure(1, weight=1)

        col_right = ctk.CTkFrame(self.form_card, fg_color="transparent")
        col_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        col_right.grid_columnconfigure(1, weight=1)

        self.inputs = {}

        def add_entry(parent, label_text, key, placeholder="", r=0):
            lbl = ctk.CTkLabel(parent, text=label_text, font=FONTS["body_bold"],
                               text_color=COLORS["text_secondary"])
            lbl.grid(row=r, column=0, sticky="w", pady=10, padx=(0, 10))
            entry = ctk.CTkEntry(parent, placeholder_text=placeholder, height=36)
            entry.grid(row=r, column=1, sticky="ew", pady=10)
            self.inputs[key] = entry

        def add_dropdown(parent, label_text, key, values, r=0):
            lbl = ctk.CTkLabel(parent, text=label_text, font=FONTS["body_bold"],
                               text_color=COLORS["text_secondary"])
            lbl.grid(row=r, column=0, sticky="w", pady=10, padx=(0, 10))
            menu = ctk.CTkOptionMenu(
                parent, values=values, height=36,
                fg_color=COLORS["bg_main"],
                text_color=COLORS["text_primary"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"],
            )
            menu.grid(row=r, column=1, sticky="ew", pady=10)
            self.inputs[key] = menu

        skills_range = [str(x) for x in range(1, 11)]

        # Left column
        add_entry(col_left, "CGPA:", "cgpa", "e.g. 8.5", 0)
        add_dropdown(col_left, "Python Skill:", "python_skill", skills_range, 1)
        add_dropdown(col_left, "SQL Skill:", "sql_skill", skills_range, 2)
        add_dropdown(col_left, "DSA Skill:", "dsa_skill", skills_range, 3)
        add_entry(col_left, "Resume Score:", "resume_score", "0 to 100", 4)

        # Right column
        add_dropdown(col_right, "Communication:", "communication", skills_range, 0)
        add_dropdown(col_right, "Aptitude:", "aptitude", skills_range, 1)
        add_entry(col_right, "Number of Projects:", "projects", "e.g. 3", 2)
        add_entry(col_right, "Certifications:", "certifications", "e.g. 2", 3)

        btn_predict = ctk.CTkButton(
            self.container,
            text="Predict Student Placement Status",
            font=FONTS["section"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            height=45,
            command=self.run_prediction,
        )
        btn_predict.grid(row=2, column=0, pady=(15, 5), padx=2, sticky="ew")

    # ------------------------------------------------------------------
    # Prediction engine — calls the EXISTING AI_Model.model
    # ------------------------------------------------------------------
    def run_prediction(self):
        # ---- Validate all inputs ----
        raw_cgpa = self.inputs["cgpa"].get().strip()
        raw_resume = self.inputs["resume_score"].get().strip()
        raw_projects = self.inputs["projects"].get().strip()
        raw_certs = self.inputs["certifications"].get().strip()

        if not raw_cgpa:
            messagebox.showerror("Validation Error", "Please enter CGPA.")
            return
        if not raw_resume:
            messagebox.showerror("Validation Error", "Please enter Resume Score.")
            return
        if not raw_projects:
            messagebox.showerror("Validation Error", "Please enter Number of Projects.")
            return
        if not raw_certs:
            messagebox.showerror("Validation Error", "Please enter Certifications.")
            return

        try:
            cgpa = float(raw_cgpa)
            if cgpa < 0.0 or cgpa > 10.0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "CGPA must be a decimal value between 0.0 and 10.0.")
            return

        try:
            resume = int(raw_resume)
            if resume < 0 or resume > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Resume Score must be an integer between 0 and 100.")
            return

        try:
            projects = int(raw_projects)
            if projects < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Projects must be a positive integer.")
            return

        try:
            certs = int(raw_certs)
            if certs < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Certifications must be a positive integer.")
            return

        python_skill = int(self.inputs["python_skill"].get())
        sql_skill = int(self.inputs["sql_skill"].get())
        dsa_skill = int(self.inputs["dsa_skill"].get())
        communication = int(self.inputs["communication"].get())
        aptitude = int(self.inputs["aptitude"].get())

        # Clear previous results
        for widget in self.result_container.winfo_children():
            widget.destroy()

        try:
            res = AI_Model.predict_student_placement({
                "cgpa": cgpa,
                "python_skill": python_skill,
                "sql_skill": sql_skill,
                "dsa_skill": dsa_skill,
                "communication": communication,
                "aptitude": aptitude,
                "projects": projects,
                "certifications": certs,
                "resume_score": resume
            })

            predicted_status = res["prediction"]
            confidence_text = f"{res['confidence']:.1f}%"

            self.display_prediction_result(
                predicted_status, confidence_text, res["suggestions"]
            )

        except Exception as e:
            messagebox.showerror("Model Error", f"Failed to run prediction:\n{str(e)}")

    # ------------------------------------------------------------------
    # Result display — uses ONLY pack (no .place) to avoid CTk crash
    # ------------------------------------------------------------------
    def display_prediction_result(self, status, confidence, suggestions):
        result_card = ctk.CTkFrame(
            self.result_container,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_color=COLORS["border"],
            border_width=1,
        )
        result_card.pack(fill="x", padx=2, pady=10)

        lbl_header = ctk.CTkLabel(
            result_card, text="PLACEMENT INFERENCE REPORT",
            font=FONTS["body_bold"], text_color=COLORS["text_secondary"],
        )
        lbl_header.pack(anchor="w", padx=20, pady=(20, 10))

        status_clean = status.strip().lower()
        is_placed = "not" not in status_clean

        status_text = "PLACED" if is_placed else "NOT PLACED"
        status_color = COLORS["success"] if is_placed else COLORS["danger"]

        status_box = ctk.CTkFrame(
            result_card,
            fg_color=("#E6F4EA", "#137333") if is_placed else ("#FCE8E6", "#C5221F"),
            corner_radius=8,
        )
        status_box.pack(fill="x", padx=20, pady=10)

        # Row inside status_box using pack — no .place()
        status_inner = ctk.CTkFrame(status_box, fg_color="transparent")
        status_inner.pack(fill="x", padx=20, pady=15)

        lbl_status_title = ctk.CTkLabel(
            status_inner, text="PREDICTION:",
            font=FONTS["body_bold"], text_color=status_color,
        )
        lbl_status_title.pack(side="left")

        lbl_status_val = ctk.CTkLabel(
            status_inner, text=f"  {status_text}",
            font=("Helvetica Neue", 22, "bold"), text_color=status_color,
        )
        lbl_status_val.pack(side="left", padx=(5, 0))

        lbl_conf = ctk.CTkLabel(
            status_inner, text=f"CONFIDENCE: {confidence}",
            font=FONTS["body_bold"],
            text_color=COLORS["text_primary"] if is_placed else "#FFFFFF",
        )
        lbl_conf.pack(side="right")

        # ---- Skill Improvement Suggestions ----
        if not is_placed or suggestions:
            rec_frame = ctk.CTkFrame(
                result_card, fg_color=COLORS["bg_card_inner"], corner_radius=8,
            )
            rec_frame.pack(fill="x", padx=20, pady=(10, 20))

            lbl_rec_title = ctk.CTkLabel(
                rec_frame, text="SKILL IMPROVEMENT RECOMMENDATIONS",
                font=FONTS["body_bold"],
                text_color=COLORS["success"] if is_placed else COLORS["warning"],
            )
            lbl_rec_title.pack(anchor="w", padx=15, pady=(15, 10))

            for sug in suggestions:
                lbl_sug = ctk.CTkLabel(
                    rec_frame, text=f"  •  {sug}",
                    font=FONTS["body"], text_color=COLORS["text_primary"],
                    justify="left", anchor="w",
                )
                lbl_sug.pack(anchor="w", padx=25, pady=4)

            ctk.CTkFrame(rec_frame, height=10, fg_color="transparent").pack()

        else:
            congrats_frame = ctk.CTkFrame(
                result_card, fg_color=COLORS["bg_card_inner"], corner_radius=8,
            )
            congrats_frame.pack(fill="x", padx=20, pady=(10, 20))

            ctk.CTkLabel(
                congrats_frame,
                text="Congratulations! High Placement Chances.",
                font=FONTS["body_bold"], text_color=COLORS["success"],
            ).pack(anchor="w", padx=20, pady=20)

    # ------------------------------------------------------------------
    def refresh_data(self):
        if hasattr(self, "inputs"):
            for k, widget in self.inputs.items():
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, ctk.CTkOptionMenu):
                    widget.set("5")

        if hasattr(self, "result_container"):
            for widget in self.result_container.winfo_children():
                widget.destroy()

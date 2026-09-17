import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from db import conn
from gui_views.styles import COLORS, FONTS


class StudentFormFrame(ctk.CTkFrame):
    """
    Multi-mode student form:
      Add          — blank form → INSERT
      Update       — pre-filled form for a known student_id → UPDATE
      SelectUpdate — enter ID first, then edit → UPDATE
      SelectDelete — enter ID first, then confirm → DELETE
    """

    def __init__(self, parent, controller, mode="Add", student_id=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.mode = mode
        self.student_id = student_id

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Scrollable container
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(10, 20))
        self.container.grid_columnconfigure(0, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 10))
        self.header_title = ctk.CTkLabel(
            self.header_frame, text="",
            font=FONTS["title"], text_color=COLORS["text_primary"], anchor="w",
        )
        self.header_title.pack(anchor="w")

        self.setup_ui()

    # ------------------------------------------------------------------
    def setup_ui(self):
        if self.mode == "Add":
            self.header_title.configure(text="Add New Student Record")
            self.render_form()
        elif self.mode == "Update" and self.student_id:
            self.header_title.configure(text=f"Update Student #{self.student_id}")
            self.render_form()
            self.load_student_data(self.student_id)
        elif self.mode == "SelectUpdate":
            self.header_title.configure(text="Update Student Record")
            self.render_selector("Enter Student ID to Edit:", "Fetch and Edit",
                                 self.fetch_for_update)
        elif self.mode == "SelectDelete":
            self.header_title.configure(text="Delete Student Record")
            self.render_selector("Enter Student ID to Delete:", "Fetch Details",
                                 self.fetch_for_delete)

    # ------------------------------------------------------------------
    def render_selector(self, label_text, button_text, command):
        self.selector_card = ctk.CTkFrame(
            self.container, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        self.selector_card.grid(row=0, column=0, sticky="ew", pady=10, padx=2)
        self.selector_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.selector_card, text=label_text,
            font=FONTS["body_bold"], text_color=COLORS["text_primary"],
        ).grid(row=0, column=0, padx=20, pady=25, sticky="w")

        self.id_entry = ctk.CTkEntry(
            self.selector_card, placeholder_text="e.g. 5", width=180, height=36,
        )
        self.id_entry.grid(row=0, column=1, padx=10, pady=25, sticky="w")

        ctk.CTkButton(
            self.selector_card, text=button_text, font=FONTS["body_bold"],
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            height=36, command=command,
        ).grid(row=0, column=2, padx=20, pady=25, sticky="e")

        self.detail_area = ctk.CTkFrame(self.container, fg_color="transparent")
        self.detail_area.grid(row=1, column=0, sticky="nsew", pady=20)
        self.detail_area.grid_columnconfigure(0, weight=1)

    # ------------------------------------------------------------------
    def render_form(self, parent=None):
        if parent is None:
            parent = self.container

        self.form_card = ctk.CTkFrame(
            parent, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        self.form_card.grid(row=0, column=0, sticky="ew", pady=10, padx=2)
        self.form_card.grid_columnconfigure(0, weight=1)
        self.form_card.grid_columnconfigure(1, weight=1)

        col_left = ctk.CTkFrame(self.form_card, fg_color="transparent")
        col_left.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        col_left.grid_columnconfigure(1, weight=1)

        col_right = ctk.CTkFrame(self.form_card, fg_color="transparent")
        col_right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        col_right.grid_columnconfigure(1, weight=1)

        self.inputs = {}

        def add_entry(p, label, key, ph="", r=0):
            ctk.CTkLabel(p, text=label, font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=r, column=0, sticky="w", pady=10, padx=(0, 10))
            e = ctk.CTkEntry(p, placeholder_text=ph, height=36)
            e.grid(row=r, column=1, sticky="ew", pady=10)
            self.inputs[key] = e

        def add_dropdown(p, label, key, vals, r=0):
            ctk.CTkLabel(p, text=label, font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=r, column=0, sticky="w", pady=10, padx=(0, 10))
            m = ctk.CTkOptionMenu(
                p, values=vals, height=36,
                fg_color=COLORS["bg_main"], text_color=COLORS["text_primary"],
                button_color=COLORS["primary"],
                button_hover_color=COLORS["primary_hover"],
            )
            m.grid(row=r, column=1, sticky="ew", pady=10)
            self.inputs[key] = m

        skills_range = [str(x) for x in range(1, 11)]

        # Left column
        add_entry(col_left, "Name:", "name", "Full Name", 0)
        add_entry(col_left, "Age:", "age", "e.g. 21", 1)
        add_entry(col_left, "CGPA:", "cgpa", "e.g. 8.5", 2)
        add_entry(col_left, "Resume Score:", "resume_score", "0 to 100", 3)
        add_entry(col_left, "Target Role:", "target_role", "e.g. Data Scientist", 4)
        add_dropdown(col_left, "Internship:", "internship", ["No", "Yes"], 5)
        add_dropdown(col_left, "Placement Status:", "placement_status",
                     ["Placed", "Not Placed"], 6)

        # Right column
        add_dropdown(col_right, "Python Skill:", "python_skill", skills_range, 0)
        add_dropdown(col_right, "SQL Skill:", "sql_skill", skills_range, 1)
        add_dropdown(col_right, "DSA Skill:", "dsa_skill", skills_range, 2)
        add_dropdown(col_right, "Communication:", "communication", skills_range, 3)
        add_dropdown(col_right, "Aptitude:", "aptitude", skills_range, 4)
        add_entry(col_right, "Projects:", "projects", "Number of projects", 5)
        add_entry(col_right, "Certifications:", "certifications", "Number of certificates", 6)

        btn_text = ("Save Student Record"
                    if self.mode in ("Add", "SelectUpdate")
                    else "Update Student Record")

        self.btn_save = ctk.CTkButton(
            parent, text=btn_text, font=FONTS["section"],
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            height=44, command=self.save_record,
        )
        self.btn_save.grid(row=1, column=0, columnspan=2,
                           pady=(10, 25), padx=20, sticky="ew")

    # ------------------------------------------------------------------
    def fetch_for_update(self):
        raw_id = self.id_entry.get().strip()
        if not raw_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Student ID.")
            return

        student_id = int(raw_id)
        for widget in self.detail_area.winfo_children():
            widget.destroy()

        self.student_id = student_id
        self.render_form(self.detail_area)
        if not self.load_student_data(student_id):
            for widget in self.detail_area.winfo_children():
                widget.destroy()

    # ------------------------------------------------------------------
    def fetch_for_delete(self):
        raw_id = self.id_entry.get().strip()
        if not raw_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Student ID.")
            return

        student_id = int(raw_id)
        for widget in self.detail_area.winfo_children():
            widget.destroy()

        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            row = cur.fetchone()

            if not row:
                messagebox.showerror("Not Found",
                                     f"Student with ID {student_id} not found.")
                return

            delete_card = ctk.CTkFrame(
                self.detail_area, fg_color=COLORS["bg_card"], corner_radius=12,
                border_color=COLORS["border"], border_width=1,
            )
            delete_card.pack(fill="x", padx=2, pady=10)

            ctk.CTkLabel(
                delete_card, text="Are you sure you want to delete this student?",
                font=FONTS["section"], text_color=COLORS["danger"],
            ).pack(anchor="w", padx=20, pady=(20, 10))

            details_text = (
                f"Student ID: {row[0]}\n"
                f"Name: {row[1]}\n"
                f"Age: {row[2]}\n"
                f"CGPA: {row[3]:.2f}\n"
                f"Target Role: {row[12]}\n"
                f"Skills: Python ({row[4]}), SQL ({row[5]}), DSA ({row[6]}), "
                f"Comm ({row[7]}), Apt ({row[8]})\n"
                f"Projects: {row[9]} | Certifications: {row[11]}\n"
                f"Resume Score: {row[13]} | Internship: {row[10]}\n"
                f"Placement Status: {row[14]}"
            )

            ctk.CTkLabel(
                delete_card, text=details_text, font=FONTS["body"],
                text_color=COLORS["text_secondary"], justify="left", anchor="w",
            ).pack(anchor="w", padx=20, pady=(0, 20))

            ctk.CTkButton(
                delete_card, text="Permanently Delete Student Record",
                font=FONTS["body_bold"],
                fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
                height=40, command=lambda: self.execute_delete(student_id),
            ).pack(fill="x", padx=20, pady=(0, 20))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve student data:\n{str(e)}")

    # ------------------------------------------------------------------
    def execute_delete(self, student_id):
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you absolutely sure you want to delete Student #{student_id}?",
        )
        if not confirm:
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Student #{student_id} deleted successfully.")

            for widget in self.detail_area.winfo_children():
                widget.destroy()
            if hasattr(self, "id_entry"):
                self.id_entry.delete(0, tk.END)

            # Invalidate cached frames so they reload fresh data
            self._invalidate_caches()
            self.controller.show_page("Dashboard")

        except Exception as e:
            messagebox.showerror("Error", f"Database delete failed:\n{str(e)}")

    # ------------------------------------------------------------------
    def load_student_data(self, student_id):
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
            row = cur.fetchone()

            if not row:
                messagebox.showerror("Not Found",
                                     f"Student with ID {student_id} not found.")
                return False

            self.inputs["name"].insert(0, str(row[1]))
            self.inputs["age"].insert(0, str(row[2]))
            self.inputs["cgpa"].insert(0, f"{row[3]:.2f}")
            self.inputs["python_skill"].set(str(row[4]))
            self.inputs["sql_skill"].set(str(row[5]))
            self.inputs["dsa_skill"].set(str(row[6]))
            self.inputs["communication"].set(str(row[7]))
            self.inputs["aptitude"].set(str(row[8]))
            self.inputs["projects"].insert(0, str(row[9]))
            self.inputs["internship"].set(str(row[10]))
            self.inputs["certifications"].insert(0, str(row[11]))
            self.inputs["target_role"].insert(0, str(row[12]))
            self.inputs["resume_score"].insert(0, str(row[13]))
            self.inputs["placement_status"].set(str(row[14]))
            return True

        except Exception as e:
            messagebox.showerror("Error",
                                 f"Failed to load student record:\n{str(e)}")
            return False

    # ------------------------------------------------------------------
    def validate_inputs(self):
        data = {k: v.get().strip() for k, v in self.inputs.items()}

        if not data["name"]:
            return "Name cannot be empty."
        if not data["target_role"]:
            return "Target Role cannot be empty."

        if not data["age"].isdigit():
            return "Age must be a positive whole number."
        age = int(data["age"])
        if age < 15 or age > 100:
            return "Age must be between 15 and 100."

        try:
            cgpa = float(data["cgpa"])
            if cgpa < 0.0 or cgpa > 10.0:
                raise ValueError
        except ValueError:
            return "CGPA must be a decimal between 0.0 and 10.0."

        if not data["resume_score"].isdigit():
            return "Resume Score must be an integer."
        resume = int(data["resume_score"])
        if resume < 0 or resume > 100:
            return "Resume Score must be between 0 and 100."

        if not data["projects"].isdigit():
            return "Projects count must be an integer."

        if not data["certifications"].isdigit():
            return "Certifications count must be an integer."

        return None

    # ------------------------------------------------------------------
    def save_record(self):
        err = self.validate_inputs()
        if err:
            messagebox.showerror("Validation Error", err)
            return

        name = self.inputs["name"].get().strip()
        age = int(self.inputs["age"].get().strip())
        cgpa = float(self.inputs["cgpa"].get().strip())
        resume_score = int(self.inputs["resume_score"].get().strip())
        target_role = self.inputs["target_role"].get().strip()
        internship = self.inputs["internship"].get()
        placement_status = self.inputs["placement_status"].get()

        python_skill = int(self.inputs["python_skill"].get())
        sql_skill = int(self.inputs["sql_skill"].get())
        dsa_skill = int(self.inputs["dsa_skill"].get())
        communication = int(self.inputs["communication"].get())
        aptitude = int(self.inputs["aptitude"].get())
        projects = int(self.inputs["projects"].get().strip())
        certifications = int(self.inputs["certifications"].get().strip())

        try:
            cur = conn.cursor()

            if self.mode == "Add":
                query = """
                INSERT INTO students
                (name, age, cgpa, python_skill, sql_skill, dsa_skill,
                communication, aptitude, projects, internship,
                certifications, target_role, resume_score, placement_status)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                values = (
                    name, age, cgpa, python_skill, sql_skill, dsa_skill,
                    communication, aptitude, projects, internship,
                    certifications, target_role, resume_score, placement_status,
                )
                cur.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success", "Student record added successfully!")

                # Clear the form
                self._clear_form()

                # Invalidate caches and go to Dashboard
                self._invalidate_caches()
                self.controller.show_page("Dashboard")

            elif self.mode in ("Update", "SelectUpdate") and self.student_id:
                query = """
                UPDATE students
                SET name=%s, age=%s, cgpa=%s, python_skill=%s, sql_skill=%s,
                    dsa_skill=%s, communication=%s, aptitude=%s, projects=%s,
                    internship=%s, certifications=%s, target_role=%s,
                    resume_score=%s, placement_status=%s
                WHERE student_id=%s
                """
                values = (
                    name, age, cgpa, python_skill, sql_skill, dsa_skill,
                    communication, aptitude, projects, internship,
                    certifications, target_role, resume_score, placement_status,
                    self.student_id,
                )
                cur.execute(query, values)
                conn.commit()
                messagebox.showinfo("Success",
                                    f"Student #{self.student_id} updated successfully!")

                # Invalidate caches
                self._invalidate_caches()

                if self.mode == "SelectUpdate":
                    for widget in self.detail_area.winfo_children():
                        widget.destroy()
                    self.id_entry.delete(0, tk.END)
                else:
                    self.controller.show_page("View Students")

        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"Failed to save student record:\n{str(e)}")

    # ------------------------------------------------------------------
    def _invalidate_caches(self):
        """Remove cached frames so they get recreated with fresh DB data."""
        for key in list(self.controller.frames.keys()):
            if key in ("Dashboard", "View Students", "Search Student",
                       "Data Analysis"):
                try:
                    self.controller.frames[key].grid_forget()
                except Exception:
                    pass
                del self.controller.frames[key]

    def _clear_form(self):
        """Reset all form inputs to blank/default."""
        if not hasattr(self, "inputs"):
            return
        for k, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ctk.CTkOptionMenu):
                if k in ("internship", "placement_status"):
                    widget.set(widget.cget("values")[0])
                else:
                    widget.set("5")

    # ------------------------------------------------------------------
    def refresh_data(self):
        if self.mode in ("SelectUpdate", "SelectDelete"):
            if hasattr(self, "id_entry"):
                self.id_entry.delete(0, tk.END)
            if hasattr(self, "detail_area"):
                for widget in self.detail_area.winfo_children():
                    widget.destroy()
        elif self.mode == "Add":
            self._clear_form()

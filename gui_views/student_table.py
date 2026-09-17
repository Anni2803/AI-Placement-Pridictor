import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from db import conn
from gui_views.styles import COLORS, FONTS


class StudentTableFrame(ctk.CTkFrame):
    """
    Full student table with ALL 15 database columns displayed in a
    native ttk.Treeview.  Supports two modes:
      • "View"   — quick name search + refresh
      • "Search" — advanced multi-filter search
    """

    COLUMNS = [
        ("student_id", "ID", 50),
        ("name", "Name", 120),
        ("age", "Age", 45),
        ("cgpa", "CGPA", 60),
        ("python_skill", "Python", 55),
        ("sql_skill", "SQL", 45),
        ("dsa_skill", "DSA", 45),
        ("communication", "Comm", 50),
        ("aptitude", "Aptitude", 60),
        ("projects", "Projects", 60),
        ("internship", "Internship", 70),
        ("certifications", "Certs", 50),
        ("target_role", "Target Role", 130),
        ("resume_score", "Resume", 60),
        ("placement_status", "Status", 90),
    ]

    def __init__(self, parent, controller, mode="View"):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.mode = mode

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_header()
        self.create_filter_bar()
        self.create_treeview()
        self.create_action_bar()

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 5))
        header.grid_columnconfigure(0, weight=1)

        title_text = ("Student Management System"
                      if self.mode == "View" else "Advanced Student Lookup")
        ctk.CTkLabel(
            header, text=title_text, font=FONTS["title"],
            text_color=COLORS["text_primary"], anchor="w",
        ).grid(row=0, column=0, sticky="w")

        sub_text = ("View and manage student database records"
                    if self.mode == "View"
                    else "Search students using multiple filters")
        ctk.CTkLabel(
            header, text=sub_text, font=FONTS["subtitle"],
            text_color=COLORS["text_secondary"], anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

    # ------------------------------------------------------------------
    # Filter bar
    # ------------------------------------------------------------------
    def create_filter_bar(self):
        self.filter_card = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        self.filter_card.grid(row=1, column=0, sticky="ew", padx=25, pady=(10, 10))

        if self.mode == "View":
            self.filter_card.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                self.filter_card, text="Quick Search Name:",
                font=FONTS["body_bold"], text_color=COLORS["text_secondary"],
            ).grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")

            self.quick_search_entry = ctk.CTkEntry(
                self.filter_card, placeholder_text="Enter student name...", width=250,
            )
            self.quick_search_entry.grid(row=0, column=1, padx=10, pady=15, sticky="w")
            self.quick_search_entry.bind("<KeyRelease>", lambda e: self.refresh_data())

            ctk.CTkButton(
                self.filter_card, text="Clear", width=80,
                fg_color=COLORS["bg_main"], text_color=COLORS["text_primary"],
                hover_color=COLORS["border"], command=self.clear_quick_search,
            ).grid(row=0, column=2, padx=10, pady=15, sticky="w")

            ctk.CTkButton(
                self.filter_card, text="Refresh Table", width=120,
                fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                command=self.refresh_data,
            ).grid(row=0, column=3, padx=20, pady=15, sticky="e")
        else:
            for i in range(4):
                self.filter_card.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(self.filter_card, text="Student ID:", font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=0, column=0, padx=20, pady=(15, 2), sticky="w")
            self.search_id = ctk.CTkEntry(self.filter_card, placeholder_text="e.g. 5")
            self.search_id.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

            ctk.CTkLabel(self.filter_card, text="Student Name:", font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=0, column=1, padx=20, pady=(15, 2), sticky="w")
            self.search_name = ctk.CTkEntry(self.filter_card, placeholder_text="Name pattern...")
            self.search_name.grid(row=1, column=1, padx=20, pady=(0, 15), sticky="ew")

            ctk.CTkLabel(self.filter_card, text="Target Role:", font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=0, column=2, padx=20, pady=(15, 2), sticky="w")
            self.search_role = ctk.CTkEntry(self.filter_card, placeholder_text="e.g. Developer")
            self.search_role.grid(row=1, column=2, padx=20, pady=(0, 15), sticky="ew")

            ctk.CTkLabel(self.filter_card, text="Placement Status:", font=FONTS["body_bold"],
                         text_color=COLORS["text_secondary"]).grid(
                row=0, column=3, padx=20, pady=(15, 2), sticky="w")
            self.search_status = ctk.CTkOptionMenu(
                self.filter_card, values=["All", "Placed", "Not Placed"],
                fg_color=COLORS["bg_main"], text_color=COLORS["text_primary"],
                button_color=COLORS["primary"], button_hover_color=COLORS["primary_hover"],
            )
            self.search_status.grid(row=1, column=3, padx=20, pady=(0, 15), sticky="ew")

            btn_frame = ctk.CTkFrame(self.filter_card, fg_color="transparent")
            btn_frame.grid(row=2, column=0, columnspan=4, sticky="e", padx=20, pady=(0, 15))

            ctk.CTkButton(
                btn_frame, text="Clear Filters", width=110,
                fg_color=COLORS["bg_main"], text_color=COLORS["text_primary"],
                hover_color=COLORS["border"], command=self.clear_search_filters,
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                btn_frame, text="Search Records", width=130,
                fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
                command=self.refresh_data,
            ).pack(side="left")

    # ------------------------------------------------------------------
    # Treeview — shows ALL 15 columns with scrollbars
    # ------------------------------------------------------------------
    def create_treeview(self):
        tree_frame = ctk.CTkFrame(
            self, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=(10, 10))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Style the Treeview to match theme
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background="#1F2937", foreground="#F9FAFB",
                        fieldbackground="#1F2937", rowheight=28,
                        font=("Helvetica Neue", 12))
        style.configure("Custom.Treeview.Heading",
                        background="#374151", foreground="#F9FAFB",
                        font=("Helvetica Neue", 12, "bold"))
        style.map("Custom.Treeview",
                   background=[("selected", "#4F46E5")],
                   foreground=[("selected", "#FFFFFF")])

        col_ids = [c[0] for c in self.COLUMNS]
        self.tree = ttk.Treeview(
            tree_frame, columns=col_ids, show="headings",
            style="Custom.Treeview", selectmode="browse",
        )

        for col_key, col_title, col_width in self.COLUMNS:
            self.tree.heading(col_key, text=col_title, anchor="w")
            self.tree.column(col_key, width=col_width, minwidth=40, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        vsb.grid(row=0, column=1, sticky="ns", pady=10)
        hsb.grid(row=1, column=0, sticky="ew", padx=10)

        # Status label at bottom
        self.lbl_count = ctk.CTkLabel(
            tree_frame, text="", font=FONTS["small"],
            text_color=COLORS["text_muted"],
        )
        self.lbl_count.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 8))

    # ------------------------------------------------------------------
    # Action bar
    # ------------------------------------------------------------------
    def create_action_bar(self):
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.grid(row=3, column=0, sticky="ew", padx=25, pady=(10, 20))

        ctk.CTkButton(
            action_bar, text="Delete Selected", font=FONTS["body_bold"],
            fg_color=COLORS["danger"], hover_color=COLORS["danger_hover"],
            width=140, command=self.delete_selected,
        ).pack(side="right", padx=10)

        ctk.CTkButton(
            action_bar, text="Edit Selected", font=FONTS["body_bold"],
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            width=130, command=self.edit_selected,
        ).pack(side="right", padx=10)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def clear_quick_search(self):
        self.quick_search_entry.delete(0, tk.END)
        self.refresh_data()

    def clear_search_filters(self):
        self.search_id.delete(0, tk.END)
        self.search_name.delete(0, tk.END)
        self.search_role.delete(0, tk.END)
        self.search_status.set("All")
        self.refresh_data()

    # ------------------------------------------------------------------
    # refresh_data — real MySQL queries, populates Treeview
    # ------------------------------------------------------------------
    def refresh_data(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cur = conn.cursor()

            if self.mode == "View":
                filter_val = self.quick_search_entry.get().strip()
                if filter_val:
                    query = "SELECT * FROM students WHERE name LIKE %s ORDER BY student_id DESC"
                    params = (f"%{filter_val}%",)
                else:
                    query = "SELECT * FROM students ORDER BY student_id DESC"
                    params = ()
            else:
                query = "SELECT * FROM students WHERE 1=1"
                params = []

                raw_id = self.search_id.get().strip()
                name_val = self.search_name.get().strip()
                role_val = self.search_role.get().strip()
                status_val = self.search_status.get()

                if raw_id:
                    if raw_id.isdigit():
                        query += " AND student_id = %s"
                        params.append(int(raw_id))
                    else:
                        messagebox.showwarning("Filter Warning", "Student ID must be a number.")

                if name_val:
                    query += " AND name LIKE %s"
                    params.append(f"%{name_val}%")

                if role_val:
                    query += " AND target_role LIKE %s"
                    params.append(f"%{role_val}%")

                if status_val != "All":
                    query += " AND placement_status = %s"
                    params.append(status_val)

                query += " ORDER BY student_id DESC"
                params = tuple(params)

            cur.execute(query, params)
            rows = cur.fetchall()

            if not rows:
                self.lbl_count.configure(text="No student records found.")
                return

            for row in rows:
                # row = (id, name, age, cgpa, py, sql, dsa, comm, apt, proj, intern, cert, role, resume, status)
                values = []
                for i, val in enumerate(row):
                    if i == 3 and isinstance(val, float):
                        values.append(f"{val:.2f}")
                    else:
                        values.append(str(val))
                self.tree.insert("", "end", values=values)

            self.lbl_count.configure(text=f"Showing {len(rows)} record(s)")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve student records:\n{str(e)}")

    # ------------------------------------------------------------------
    def _get_selected_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required",
                                   "Please select a student record from the table.")
            return None
        values = self.tree.item(selected[0], "values")
        return int(values[0])  # student_id is first column

    def edit_selected(self):
        sid = self._get_selected_id()
        if sid is not None:
            self.controller.open_update_student(sid)

    def delete_selected(self):
        sid = self._get_selected_id()
        if sid is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to permanently delete Student #{sid}?",
        )
        if not confirm:
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE student_id = %s", (sid,))
            conn.commit()
            messagebox.showinfo("Success", f"Student #{sid} deleted successfully.")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student record:\n{str(e)}")

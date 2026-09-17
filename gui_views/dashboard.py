import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from db import conn
from gui_views.styles import COLORS, FONTS


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ---- Header with Refresh button ----
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 10))
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame, text="Placement Dashboard",
            font=FONTS["title"], text_color=COLORS["text_primary"], anchor="w",
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ctk.CTkLabel(
            header_frame, text="Placement Prediction & Skill Improvement System",
            font=FONTS["subtitle"], text_color=COLORS["text_secondary"], anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        btn_refresh = ctk.CTkButton(
            header_frame, text="Refresh Stats", width=130,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"],
            font=FONTS["body_bold"], command=self.refresh_data,
        )
        btn_refresh.grid(row=0, column=1, rowspan=2, sticky="e", padx=(10, 0))

        # ---- Scrollable content ----
        self.content_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(10, 20))
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(1, weight=1)
        self.content_container.grid_columnconfigure(2, weight=1)

        self.kpi_widgets = {}
        self.create_kpi_cards()
        self.create_bottom_sections()

    # ------------------------------------------------------------------
    def create_kpi_cards(self):
        card_configs = [
            ("Total Students", "total_students", 0, 0, COLORS["primary"]),
            ("Placed Students", "placed_students", 0, 1, COLORS["success"]),
            ("Not Placed Students", "not_placed_students", 0, 2, COLORS["danger"]),
            ("Average CGPA", "avg_cgpa", 1, 0, COLORS["primary"]),
            ("Average Resume Score", "avg_resume", 1, 1, COLORS["primary"]),
            ("Placement Rate", "placement_rate", 1, 2, COLORS["success"]),
        ]

        for title, key, r, c, theme_color in card_configs:
            card = ctk.CTkFrame(
                self.content_container,
                fg_color=COLORS["bg_card"], corner_radius=12,
                border_color=COLORS["border"], border_width=1,
                height=110,
            )
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)
            card.grid_columnconfigure(0, weight=1)
            card.grid_rowconfigure(0, weight=1)
            card.grid_rowconfigure(1, weight=1)

            lbl_title = ctk.CTkLabel(
                card, text=title.upper(),
                font=FONTS["card_title"], text_color=COLORS["text_secondary"], anchor="w",
            )
            lbl_title.grid(row=0, column=0, padx=(18, 15), pady=(15, 0), sticky="w")

            lbl_val = ctk.CTkLabel(
                card, text="--",
                font=FONTS["card_val"], text_color=COLORS["text_primary"], anchor="w",
            )
            lbl_val.grid(row=1, column=0, padx=(18, 15), pady=(0, 15), sticky="sw")

            self.kpi_widgets[key] = lbl_val

    # ------------------------------------------------------------------
    def create_bottom_sections(self):
        bottom_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, columnspan=3, pady=(20, 10), sticky="nsew")
        bottom_frame.grid_columnconfigure(0, weight=3)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # Recent records card
        recent_card = ctk.CTkFrame(
            bottom_frame, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        recent_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        recent_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            recent_card, text="Recent Student Records",
            font=FONTS["section"], text_color=COLORS["text_primary"], anchor="w",
        ).pack(anchor="w", padx=20, pady=(20, 15))

        self.recent_table = ctk.CTkFrame(recent_card, fg_color="transparent")
        self.recent_table.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Quick actions card
        actions_card = ctk.CTkFrame(
            bottom_frame, fg_color=COLORS["bg_card"], corner_radius=12,
            border_color=COLORS["border"], border_width=1,
        )
        actions_card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        ctk.CTkLabel(
            actions_card, text="Quick Actions",
            font=FONTS["section"], text_color=COLORS["text_primary"], anchor="w",
        ).pack(anchor="w", padx=20, pady=(20, 15))

        for text, color, hover, page in [
            ("Add New Student", COLORS["primary"], COLORS["primary_hover"], "Add Student"),
            ("Predict Placement", COLORS["success"], COLORS["success_hover"], "AI Prediction"),
            ("View Data Analysis", COLORS["primary"], COLORS["primary_hover"], "Data Analysis"),
        ]:
            ctk.CTkButton(
                actions_card, text=text, font=FONTS["body_bold"],
                fg_color=color, hover_color=hover, height=38,
                command=lambda p=page: self.controller.show_page(p),
            ).pack(fill="x", padx=20, pady=8)

    # ------------------------------------------------------------------
    # refresh_data — queries MySQL for REAL statistics
    # ------------------------------------------------------------------
    def refresh_data(self):
        try:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM students")
            total = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM students WHERE LOWER(placement_status) = 'placed'")
            placed = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM students WHERE LOWER(placement_status) LIKE '%not%'")
            not_placed = cur.fetchone()[0]

            cur.execute("SELECT AVG(cgpa) FROM students")
            avg_cgpa = cur.fetchone()[0] or 0.0

            cur.execute("SELECT AVG(resume_score) FROM students")
            avg_resume = cur.fetchone()[0] or 0.0

            self.kpi_widgets["total_students"].configure(text=str(total))
            self.kpi_widgets["placed_students"].configure(text=str(placed))
            self.kpi_widgets["not_placed_students"].configure(text=str(not_placed))
            self.kpi_widgets["avg_cgpa"].configure(text=f"{avg_cgpa:.2f}")
            self.kpi_widgets["avg_resume"].configure(text=f"{avg_resume:.1f}")

            rate = (placed / total * 100) if total > 0 else 0.0
            self.kpi_widgets["placement_rate"].configure(text=f"{rate:.1f}%")

            self.load_recent_table(cur)

        except Exception as e:
            messagebox.showerror("Dashboard Error", f"Failed to load dashboard data:\n{str(e)}")

    # ------------------------------------------------------------------
    def load_recent_table(self, cur):
        for widget in self.recent_table.winfo_children():
            widget.destroy()

        cur.execute("""
            SELECT student_id, name, cgpa, target_role, placement_status
            FROM students
            ORDER BY student_id DESC
            LIMIT 5
        """)
        rows = cur.fetchall()

        if not rows:
            ctk.CTkLabel(
                self.recent_table, text="No records found in database.",
                font=FONTS["body"], text_color=COLORS["text_secondary"],
            ).pack(pady=20)
            return

        headers = ["ID", "Name", "CGPA", "Target Role", "Status"]
        col_widths = [50, 130, 70, 160, 100]

        for col_idx, (header, width) in enumerate(zip(headers, col_widths)):
            ctk.CTkLabel(
                self.recent_table, text=header,
                font=FONTS["body_bold"], text_color=COLORS["text_secondary"],
                anchor="w", width=width,
            ).grid(row=0, column=col_idx, padx=5, pady=(5, 10), sticky="w")

        ctk.CTkFrame(
            self.recent_table, height=1, fg_color=COLORS["border"],
        ).grid(row=1, column=0, columnspan=5, sticky="ew", pady=(0, 5))

        for row_idx, row in enumerate(rows):
            grid_row = row_idx + 2
            for col_idx, (val, width) in enumerate(zip(row, col_widths)):
                text_str = str(val)
                if col_idx == 2 and isinstance(val, float):
                    text_str = f"{val:.2f}"

                text_color = COLORS["text_primary"]
                if col_idx == 4:
                    text_color = (
                        COLORS["success"] if val.lower() == "placed"
                        else COLORS["danger"]
                    )

                ctk.CTkLabel(
                    self.recent_table, text=text_str,
                    font=FONTS["body"], text_color=text_color,
                    anchor="w", width=width,
                ).grid(row=grid_row, column=col_idx, padx=5, pady=6, sticky="w")

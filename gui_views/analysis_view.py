import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from db import conn
from gui_views.styles import COLORS, FONTS

class AnalysisViewFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(10, 20))
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=(25, 10))
        
        title = ctk.CTkLabel(
            self.header_frame,
            text="Placement Data Analysis",
            font=FONTS["title"],
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            self.header_frame,
            text="Statistical Analysis and Visualizations of Student Records",
            font=FONTS["subtitle"],
            text_color=COLORS["text_secondary"],
            anchor="w"
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        self.metrics_card = ctk.CTkFrame(
            self.container,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_color=COLORS["border"],
            border_width=1
        )
        self.metrics_card.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 15), padx=2)
        
        self.metrics_card.grid_columnconfigure(0, weight=1)
        self.metrics_card.grid_columnconfigure(1, weight=1)
        self.metrics_card.grid_columnconfigure(2, weight=1)
        self.metrics_card.grid_columnconfigure(3, weight=1)
        
        self.graphs_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.graphs_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        self.graphs_frame.grid_columnconfigure(0, weight=1)
        self.graphs_frame.grid_columnconfigure(1, weight=1)

    def refresh_data(self):
        try:
            df = pd.read_sql("SELECT * FROM students", conn)
            
            if df.empty:
                self.show_empty_state()
                return

            self.calculate_metrics(df)
            self.render_charts(df)

        except Exception as e:
            messagebox.showerror("Analysis Error", f"Failed to compute statistical analysis:\n{str(e)}")

    def show_empty_state(self):
        for widget in self.metrics_card.winfo_children():
            widget.destroy()
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
            
        lbl = ctk.CTkLabel(
            self.metrics_card,
            text="No student records available for analysis.",
            font=FONTS["body_bold"],
            text_color=COLORS["text_muted"]
        )
        lbl.pack(pady=30)

    def calculate_metrics(self, df):
        for widget in self.metrics_card.winfo_children():
            widget.destroy()

        total = len(df)
        avg_cgpa = df["cgpa"].mean()
        high_cgpa = df["cgpa"].max()
        low_cgpa = df["cgpa"].min()
        avg_resume = df["resume_score"].mean()
        
        placed_count = len(df[df["placement_status"].str.lower() == "placed"])
        not_placed_count = len(df[df["placement_status"].str.lower().str.contains("not")])
        rate = (placed_count / total * 100) if total > 0 else 0.0
        
        cgpa_arr = np.array(df["cgpa"])
        median_cgpa = np.median(cgpa_arr)
        std_cgpa = np.std(cgpa_arr)

        lbl_title = ctk.CTkLabel(self.metrics_card, text="PANDAS & NUMPY METRICS SUMMARY", font=FONTS["card_title"], text_color=COLORS["text_secondary"])
        lbl_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=20, pady=(15, 10))
        
        metrics_list = [
            ("Total Students", str(total), 0, 0),
            ("Average CGPA", f"{avg_cgpa:.2f}", 0, 1),
            ("Median CGPA", f"{median_cgpa:.2f}", 0, 2),
            ("CGPA Std Dev", f"{std_cgpa:.2f}", 0, 3),
            
            ("Highest CGPA", f"{high_cgpa:.2f}", 1, 0),
            ("Lowest CGPA", f"{low_cgpa:.2f}", 1, 1),
            ("Avg Resume Score", f"{avg_resume:.1f}", 1, 2),
            ("Placement Rate", f"{rate:.1f}%", 1, 3)
        ]

        for label_text, val_text, r, c in metrics_list:
            grid_row = r + 1
            
            inner = ctk.CTkFrame(self.metrics_card, fg_color=COLORS["bg_card_inner"], corner_radius=8, height=75)
            inner.grid(row=grid_row, column=c, padx=10, pady=8, sticky="ew")
            inner.grid_propagate(False)
            inner.grid_columnconfigure(0, weight=1)
            
            lbl_inner_lbl = ctk.CTkLabel(inner, text=label_text, font=FONTS["small"], text_color=COLORS["text_secondary"], anchor="w")
            lbl_inner_lbl.pack(anchor="w", padx=12, pady=(10, 2))
            
            lbl_inner_val = ctk.CTkLabel(inner, text=val_text, font=FONTS["body_bold"], text_color=COLORS["text_primary"], anchor="w")
            lbl_inner_val.pack(anchor="w", padx=12, pady=(0, 10))

    def render_charts(self, df):
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()

        is_dark = (ctk.get_appearance_mode() == "Dark")
        bg_hex = "#1F2937" if is_dark else "#FFFFFF"
        text_hex = "#F9FAFB" if is_dark else "#1F2937"
        grid_hex = "#4B5563" if is_dark else "#D1D5DB"
        
        primary_color = "#6366F1" if is_dark else "#4F46E5"
        secondary_colors = ["#10B981", "#EF4444"] if is_dark else ["#059669", "#DC2626"]

        # Card 1: Skill scores comparison
        card_skills = ctk.CTkFrame(self.graphs_frame, fg_color=COLORS["bg_card"], corner_radius=12, border_color=COLORS["border"], border_width=1)
        card_skills.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        
        lbl_s = ctk.CTkLabel(card_skills, text="Average Skill Scores Comparison", font=FONTS["body_bold"], text_color=COLORS["text_primary"])
        lbl_s.pack(anchor="w", padx=20, pady=(15, 5))

        fig_skills = Figure(figsize=(5, 3.8), dpi=100, facecolor=bg_hex)
        ax_skills = fig_skills.add_subplot(111)
        ax_skills.set_facecolor(bg_hex)
        
        skills = ["Python", "SQL", "DSA", "Comm", "Aptitude"]
        avg_scores = [
            df["python_skill"].mean(),
            df["sql_skill"].mean(),
            df["dsa_skill"].mean(),
            df["communication"].mean(),
            df["aptitude"].mean()
        ]
        
        ax_skills.bar(skills, avg_scores, color=primary_color, width=0.5, edgecolor=grid_hex)
        ax_skills.set_ylim(0, 10)
        ax_skills.set_ylabel("Average Score", color=text_hex)
        
        self.apply_fig_styles(fig_skills, ax_skills, text_hex, grid_hex)
        
        canvas_s = FigureCanvasTkAgg(fig_skills, card_skills)
        canvas_s.draw()
        canvas_s.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Card 2: Placement breakdown pie
        card_pie = ctk.CTkFrame(self.graphs_frame, fg_color=COLORS["bg_card"], corner_radius=12, border_color=COLORS["border"], border_width=1)
        card_pie.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        lbl_p = ctk.CTkLabel(card_pie, text="Placement Distribution Status", font=FONTS["body_bold"], text_color=COLORS["text_primary"])
        lbl_p.pack(anchor="w", padx=20, pady=(15, 5))

        fig_pie = Figure(figsize=(5, 3.8), dpi=100, facecolor=bg_hex)
        ax_pie = fig_pie.add_subplot(111)
        ax_pie.set_facecolor(bg_hex)
        
        placement = df["placement_status"].value_counts()
        
        pie_colors = []
        for cat in placement.index:
            if "not" in cat.lower():
                pie_colors.append(secondary_colors[1])
            else:
                pie_colors.append(secondary_colors[0])
                
        ax_pie.pie(
            placement,
            labels=placement.index,
            autopct="%1.1f%%",
            textprops={"color": text_hex},
            colors=pie_colors,
            startangle=90
        )
        
        fig_pie.patch.set_facecolor(bg_hex)
        ax_pie.title.set_color(text_hex)
        
        canvas_p = FigureCanvasTkAgg(fig_pie, card_pie)
        canvas_p.draw()
        canvas_p.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Card 3: CGPA Distribution Histogram
        card_hist = ctk.CTkFrame(self.graphs_frame, fg_color=COLORS["bg_card"], corner_radius=12, border_color=COLORS["border"], border_width=1)
        card_hist.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")
        
        lbl_h = ctk.CTkLabel(card_hist, text="Student CGPA Frequency Distribution", font=FONTS["body_bold"], text_color=COLORS["text_primary"])
        lbl_h.pack(anchor="w", padx=20, pady=(15, 5))

        fig_hist = Figure(figsize=(10, 3.8), dpi=100, facecolor=bg_hex)
        ax_hist = fig_hist.add_subplot(111)
        ax_hist.set_facecolor(bg_hex)
        
        ax_hist.hist(df["cgpa"], bins=10, color=primary_color, edgecolor=grid_hex, alpha=0.85)
        ax_hist.set_xlabel("CGPA Bracket", color=text_hex)
        ax_hist.set_ylabel("Number of Students", color=text_hex)
        
        self.apply_fig_styles(fig_hist, ax_hist, text_hex, grid_hex)
        
        canvas_h = FigureCanvasTkAgg(fig_hist, card_hist)
        canvas_h.draw()
        canvas_h.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def apply_fig_styles(self, fig, ax, text_hex, grid_hex):
        ax.tick_params(colors=text_hex, labelsize=9)
        ax.xaxis.label.set_color(text_hex)
        ax.yaxis.label.set_color(text_hex)
        ax.grid(True, linestyle="--", alpha=0.3, color=grid_hex)
        
        for spine in ax.spines.values():
            spine.set_color(grid_hex)
            spine.set_alpha(0.5)
            
        fig.patch.set_facecolor(ax.get_facecolor())

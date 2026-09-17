import os
import csv
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from db import conn

# Import styles and views from gui_views
from gui_views.styles import COLORS, FONTS
from gui_views.dashboard import DashboardFrame
from gui_views.student_form import StudentFormFrame
from gui_views.student_table import StudentTableFrame
from gui_views.prediction import PredictionFrame
from gui_views.analysis_view import AnalysisViewFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("AI Placement Predictor & Skill Improvement System")
        self.geometry("1280x800")
        self.minsize(1050, 700)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set default appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.current_frame = None
        self.active_button = None
        self.frames = {}
        
        self.create_sidebar()
        
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.show_page("Dashboard")

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color=COLORS["bg_sidebar"],
            border_color=COLORS["border"],
            border_width=1
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title_label = ctk.CTkLabel(
            self.sidebar,
            text="AI Predictor",
            font=FONTS["title"],
            text_color=COLORS["primary"]
        )
        title_label.pack(pady=(30, 2), padx=20, anchor="w")

        subtitle_label = ctk.CTkLabel(
            self.sidebar,
            text="Placement Analytics & ML",
            font=FONTS["small"],
            text_color=COLORS["text_secondary"]
        )
        subtitle_label.pack(pady=(0, 25), padx=20, anchor="w")

        sep = ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"])
        sep.pack(fill="x", padx=15, pady=(0, 15))

        nav_items = [
            ("Dashboard", "Dashboard"),
            ("Add Student", "Add Student"),
            ("View Students", "View Students"),
            ("Search Student", "Search Student"),
            ("Update Student", "Update Student"),
            ("Delete Student", "Delete Student"),
            ("Data Analysis", "Data Analysis"),
            ("AI Prediction", "AI Prediction"),
            ("Export Dataset", "Export"),
            ("Settings", "Settings"),
        ]

        self.nav_buttons = {}
        for text, key in nav_items:
            if key == "Export":
                cmd = self.export_dataset
            elif key == "Exit":
                cmd = self.confirm_exit
            else:
                cmd = lambda k=key: self.show_page(k)

            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color=COLORS["text_primary"],
                hover_color=COLORS["border"],
                font=FONTS["body_bold"],
                anchor="w",
                command=cmd
            )
            btn.pack(fill="x", padx=15, pady=3)
            self.nav_buttons[key] = btn

        exit_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        exit_frame.pack(side="bottom", fill="x", padx=15, pady=20)
        
        btn_exit = ctk.CTkButton(
            exit_frame,
            text="Exit Application",
            height=40,
            corner_radius=8,
            fg_color="transparent",
            text_color=COLORS["danger"],
            hover_color=("#FEE2E2", "#7F1D1D"),
            font=FONTS["body_bold"],
            anchor="w",
            command=self.confirm_exit
        )
        btn_exit.pack(fill="x")

    def show_page(self, page_key):
        if self.current_frame and self.current_frame == self.frames.get(page_key):
            if hasattr(self.current_frame, "refresh_data"):
                self.current_frame.refresh_data()
            return

        if self.current_frame:
            self.current_frame.grid_forget()

        if self.active_button:
            self.active_button.configure(
                fg_color="transparent",
                text_color=COLORS["text_primary"]
            )

        if page_key in self.nav_buttons:
            self.active_button = self.nav_buttons[page_key]
            self.active_button.configure(
                fg_color=COLORS["primary"],
                text_color="#FFFFFF"
            )

        if page_key not in self.frames:
            if page_key == "Dashboard":
                self.frames[page_key] = DashboardFrame(self.main_container, self)
            elif page_key == "Add Student":
                self.frames[page_key] = StudentFormFrame(self.main_container, self, mode="Add")
            elif page_key == "View Students":
                self.frames[page_key] = StudentTableFrame(self.main_container, self, mode="View")
            elif page_key == "Search Student":
                self.frames[page_key] = StudentTableFrame(self.main_container, self, mode="Search")
            elif page_key == "Update Student":
                self.frames[page_key] = StudentFormFrame(self.main_container, self, mode="SelectUpdate")
            elif page_key == "Delete Student":
                self.frames[page_key] = StudentFormFrame(self.main_container, self, mode="SelectDelete")
            elif page_key == "AI Prediction":
                self.frames[page_key] = PredictionFrame(self.main_container, self)
            elif page_key == "Data Analysis":
                self.frames[page_key] = AnalysisViewFrame(self.main_container, self)
            elif page_key == "Settings":
                self.frames[page_key] = SettingsFrame(self.main_container, self)

        self.current_frame = self.frames[page_key]
        
        if hasattr(self.current_frame, "refresh_data"):
            self.current_frame.refresh_data()

        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def open_update_student(self, student_id):
        if "Update Student" in self.frames:
            self.frames["Update Student"].grid_forget()
            del self.frames["Update Student"]
            
        self.frames["Update Student"] = StudentFormFrame(self.main_container, self, mode="Update", student_id=student_id)
        self.show_page("Update Student")

    def export_dataset(self):
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            
            if not rows:
                messagebox.showinfo("Export", "No student data to export.")
                return
                
            headers = [desc[0] for desc in cur.description]
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Export Dataset",
                initialfile="students_dataset.csv"
            )
            
            if not file_path:
                return
                
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
                
            messagebox.showinfo("Export Successful", f"Dataset successfully exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export dataset:\n{str(e)}")

    def confirm_exit(self):
        confirm = messagebox.askyesno("Exit Application", "Are you sure you want to exit the application?")
        if confirm:
            self.destroy()

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            container,
            text="Settings",
            font=FONTS["title"],
            text_color=COLORS["text_primary"],
            anchor="w"
        )
        title.grid(row=0, column=0, sticky="w", pady=(0, 20))
        
        appearance_card = ctk.CTkFrame(
            container,
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=12
        )
        appearance_card.grid(row=1, column=0, sticky="ew", pady=(0, 20), padx=2)
        appearance_card.grid_columnconfigure(1, weight=1)
        
        ac_title = ctk.CTkLabel(
            appearance_card,
            text="Appearance Mode",
            font=FONTS["section"],
            text_color=COLORS["text_primary"]
        )
        ac_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))
        
        lbl_theme = ctk.CTkLabel(
            appearance_card,
            text="App Theme:",
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"]
        )
        lbl_theme.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 20))
        
        self.theme_menu = ctk.CTkOptionMenu(
            appearance_card,
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode,
            fg_color=COLORS["primary"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )
        self.theme_menu.grid(row=1, column=1, sticky="w", padx=20, pady=(0, 20))
        self.theme_menu.set(ctk.get_appearance_mode())
        
        lbl_color = ctk.CTkLabel(
            appearance_card,
            text="Accent Color:",
            font=FONTS["body_bold"],
            text_color=COLORS["text_secondary"]
        )
        lbl_color.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))
        
        self.color_menu = ctk.CTkOptionMenu(
            appearance_card,
            values=["blue", "green", "dark-blue"],
            command=self.change_color_theme,
            fg_color=COLORS["primary"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"]
        )
        self.color_menu.grid(row=2, column=1, sticky="w", padx=20, pady=(0, 20))
        
        about_card = ctk.CTkFrame(
            container,
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=12
        )
        about_card.grid(row=2, column=0, sticky="ew", pady=10, padx=2)
        about_card.grid_columnconfigure(0, weight=1)
        
        about_title = ctk.CTkLabel(
            about_card,
            text="About Project",
            font=FONTS["section"],
            text_color=COLORS["text_primary"]
        )
        about_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))
        
        about_text = (
            "AI Placement Predictor & Skill Improvement System\n\n"
            "This application uses a Machine Learning Decision Tree Classifier trained on student "
            "academic records, technical skill scores, and project/resume metrics to predict placement outcomes.\n\n"
            "Features:\n"
            "• MySQL Integration for Real-time Student Management\n"
            "• Advanced Pandas & NumPy Data Analysis\n"
            "• Embedded Matplotlib Skill & Status Visualizations\n"
            "• AI-powered Predictive Inference and Probability/Confidence values\n"
            "• Dynamic Skill Improvement Advisor based on weak subject metrics\n\n"
            "Version: 1.0.0\n"
            "Author: Anjali"
        )
        
        lbl_about = ctk.CTkLabel(
            about_card,
            text=about_text,
            font=FONTS["body"],
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w"
        )
        lbl_about.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 25))

    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    def change_color_theme(self, new_theme):
        ctk.set_default_color_theme(new_theme)
        messagebox.showinfo("Theme Update", "Color theme updated. Please restart the application to apply the new color theme completely.")

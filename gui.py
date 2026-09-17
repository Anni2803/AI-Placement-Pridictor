# Entry point for the AI Placement Predictor & Skill Improvement System GUI
# Run this file to start the desktop application

from gui_views.app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()
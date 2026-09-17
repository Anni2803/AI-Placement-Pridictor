# Styling and Theme Configuration for the AI Placement Predictor GUI

# Colors are defined as (light_color, dark_color) for CustomTkinter compatibility

COLORS = {
    "bg_main": ("#F3F4F6", "#111827"),        # Light gray vs Dark gray-blue
    "bg_sidebar": ("#FFFFFF", "#1F2937"),     # Pure white vs Slate gray
    "bg_card": ("#FFFFFF", "#1F2937"),        # Card backgrounds
    "bg_card_inner": ("#F9FAFB", "#374151"),  # Inner elements/subcards
    
    "primary": ("#6366F1", "#4F46E5"),        # Indigo accent
    "primary_hover": ("#4F46E5", "#4338CA"),
    
    "success": ("#10B981", "#059669"),        # Emerald green
    "success_hover": ("#059669", "#047857"),
    
    "danger": ("#EF4444", "#DC2626"),         # Red
    "danger_hover": ("#DC2626", "#B91C1C"),
    
    "warning": ("#F59E0B", "#D97706"),        # Amber
    
    "text_primary": ("#1F2937", "#F9FAFB"),   # Dark gray vs Off-white
    "text_secondary": ("#4B5563", "#9CA3AF"), # Medium gray
    "text_muted": ("#9CA3AF", "#6B7280"),     # Light gray muting
    
    "border": ("#E5E7EB", "#374151"),         # Thin dividers
}

FONTS = {
    "title": ("Helvetica Neue", 28, "bold"),
    "subtitle": ("Helvetica Neue", 14, "normal"),
    "section": ("Helvetica Neue", 20, "bold"),
    "card_title": ("Helvetica Neue", 12, "bold"),
    "card_val": ("Helvetica Neue", 24, "bold"),
    "body_bold": ("Helvetica Neue", 13, "bold"),
    "body": ("Helvetica Neue", 13, "normal"),
    "small": ("Helvetica Neue", 11, "normal"),
}

# Theme presets
THEMES = ["blue", "green", "dark-blue"]
APPEARANCE_MODES = ["System", "Dark", "Light"]

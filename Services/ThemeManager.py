class ThemeManager:
    current_theme = None # Default theme name
    THEMES = {
        "Default Light": {
            "background": "#ffffff",
            "text": "#000000",
            "accent": "#007bff",
            "widget_bg": "#FFFFFF",
            "button": "#4a90e2",
            "button_text": "#FFFFFF",
            "border": "#CCCCCC"
        },
        "Dark Mode": {
            "background": "#2E2E2E",
            "text": "#FFFFFF",
            "accent": "#00aaff",
            "widget_bg": "#3E3E3E",
            "button": "#505050",
            "button_text": "#FFFFFF",
            "border": "#505050"
        },
        "Nature": {
            "background": "#f0f7f0",
            "text": "#2c4a2c",
            "accent": "#4caf50",
            "widget_bg": "#ffffff",
            "button": "#4caf50",
            "button_text": "#FFFFFF",
            "border": "#a5d6a7"
        },
        "Ocean": {
            "background": "#1a374d",
            "text": "#b6e1e7",
            "accent": "#51c4d3",
            "widget_bg": "#406882",
            "button": "#51c4d3",
            "button_text": "#FFFFFF",
            "border": "#6998AB"
        },
      
        "Sunset": {
            "background": "#2b1b17",
            "text": "#f4c9b7",
            "accent": "#e86d5c",
            "widget_bg": "#462521",
            "button": "#d64933",
            "button_text": "#FFFFFF",
            "border": "#8e4a40"
        },
        "Nord": {
            "background": "#2e3440",
            "text": "#eceff4",
            "accent": "#88c0d0",
            "widget_bg": "#3b4252",
            "button": "#5e81ac",
            "button_text": "#eceff4",
            "border": "#4c566a"
        },
        "Dracula": {
            "background": "#282a36",
            "text": "#f8f8f2",
            "accent": "#bd93f9",
            "widget_bg": "#44475a",
            "button": "#6272a4",
            "button_text": "#f8f8f2",
            "border": "#6272a4"
        },
        "Solarized": {
            "background": "#002b36",
            "text": "#839496",
            "accent": "#268bd2",
            "widget_bg": "#073642",
            "button": "#2aa198",
            "button_text": "#fdf6e3",
            "border": "#586e75"
        },
    
        "Arctic Aurora": {
            "background": "#2c3e50",
            "text": "#ecf0f1",
            "accent": "#1abc9c",
            "widget_bg": "#34495e",
            "button": "#16a085",
            "button_text": "#ffffff",
            "border": "#2ecc71"
        },
        "Cyber Neon": {
            "background": "#000000",
            "text": "#00ff9f",
            "accent": "#ff00ff",
            "widget_bg": "#0a0a0a",
            "button": "#00ffff",
            "button_text": "#000000",
            "border": "#ff00ff"
        },
        "Candy": {
            "background": "#ffebee",
            "text": "#880e4f",
            "accent": "#f48fb1",
            "widget_bg": "#ffc1e3",
            "button": "#f06292",
            "button_text": "#ffffff",
            "border": "#ad1457"
        },
        "Lava": {
            "background": "#4a0000",
            "text": "#ffcccb",
            "accent": "#ff5722",
            "widget_bg": "#5d001e",
            "button": "#d84315",
            "button_text": "#ffffff",
            "border": "#bf360c"
        },
        "Skyline": {
            "background": "#e3f2fd",
            "text": "#0d47a1",
            "accent": "#64b5f6",
            "widget_bg": "#bbdefb",
            "button": "#2196f3",
            "button_text": "#ffffff",
            "border": "#1976d2"
        },
      
        "Blush Pink": {
            "background": "#ffe4e1",
            "text": "#5a2a27",
            "accent": "#ff7f7f",
            "widget_bg": "#fff5f5",
            "button": "#ff6f61",
            "button_text": "#ffffff",
            "border": "#ff9999"
        },
        "Emerald Dream": {
            "background": "#004d40",
            "text": "#a7ffeb",
            "accent": "#1de9b6",
            "widget_bg": "#00695c",
            "button": "#00bfa5",
            "button_text": "#ffffff",
            "border": "#004d40"
        },
        "Amber Glow": {
            "background": "#ffcc80",
            "text": "#4e342e",
            "accent": "#ffab40",
            "widget_bg": "#ffe0b2",
            "button": "#ff8a65",
            "button_text": "#ffffff",
            "border": "#ff7043"
        },
        "Mystic Lavender": {
            "background": "#e6e6fa",
            "text": "#4b0082",
            "accent": "#9370db",
            "widget_bg": "#f8f8ff",
            "button": "#8a2be2",
            "button_text": "#ffffff",
            "border": "#7b68ee"
        },
            "Galaxy": {
                "background": "#0b0c10",
                "text": "#66fcf1",
                "accent": "#45a29e",
                "widget_bg": "#1f2833",
                "button": "#c5c6c7",
                "button_text": "#0b0c10",
                "border": "#66fcf1"
            },
            "Starlight": {
                "background": "#1a1a40",
                "text": "#e0e0eb",
                "accent": "#ffcc00",
                "widget_bg": "#2e2e5e",
                "button": "#ffcc00",
                "button_text": "#1a1a40",
                "border": "#e0e0eb"
            },
            "Cosmic Purple": {
                "background": "#2d004d",
                "text": "#e6e6fa",
                "accent": "#9933ff",
                "widget_bg": "#400080",
                "button": "#8000ff",
                "button_text": "#ffffff",
                "border": "#9933ff"
            },
            "Nebula": {
                "background": "#1b0033",
                "text": "#d1c4e9",
                "accent": "#7e57c2",
                "widget_bg": "#311b92",
                "button": "#9575cd",
                "button_text": "#ffffff",
                "border": "#7e57c2"
            },
            "Aurora Borealis": {
                "background": "#001a33",
                "text": "#a7ffeb",
                "accent": "#00e676",
                "widget_bg": "#00334d",
                "button": "#00bfa5",
                "button_text": "#ffffff",
                "border": "#00e676"
            },
  
            "Solar Flare": {
                "background": "#331a00",
                "text": "#ffcc80",
                "accent": "#ff6f00",
                "widget_bg": "#4d2600",
                "button": "#ff8a00",
                "button_text": "#ffffff",
                "border": "#ff6f00"
            },
            "Meteor Shower": {
                "background": "#000033",
                "text": "#99ccff",
                "accent": "#3366ff",
                "widget_bg": "#001a66",
                "button": "#0033cc",
                "button_text": "#ffffff",
                "border": "#3366ff"
            },

            "Transparent": {
                "background": "transparent",
                "text": "#f7f2f2",
                "accent": "#007bff",
                "widget_bg": "rgba(255, 255, 255, 0.5)",
                "button": "rgba(0, 123, 255, 0.7)",
                "button_text": "#FFFFFF",
                "border": "rgba(204, 204, 204, 0.5)"
            },
  
    }

    @staticmethod
    def get_theme(theme_name):
        """Get the theme dictionary for the given theme name."""
        if theme_name not in ThemeManager.THEMES:
            return ThemeManager.THEMES["Dark Mode"]
        return ThemeManager.THEMES[theme_name]

    @staticmethod
    def set_current_theme(theme_name=None):
        """Set the current theme by name."""
        if theme_name in ThemeManager.THEMES:
            ThemeManager.current_theme = theme_name
        else:
            from config.config_manager import Config_Manager
            ThemeManager.current_theme =  Config_Manager().get_default_theme()

    @staticmethod
    def get_current_theme():
        """Get the current theme dictionary."""
        if ThemeManager.current_theme:
            return ThemeManager.get_theme(ThemeManager.current_theme)
        else:
            from config.config_manager import Config_Manager
            ThemeManager.current_theme =  Config_Manager().get_default_theme()
            return ThemeManager.get_theme(ThemeManager.current_theme)


    @staticmethod
    def get_theme_names():
        """Return a list of all available theme names."""
        return list(ThemeManager.THEMES.keys())

    @staticmethod
    def get_button_style():
        """Return button style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QPushButton {{
                background-color: {theme['button']};
                color: {theme['button_text']};
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {theme['accent']};
            }}
        """

    @staticmethod
    def get_line_edit_style():
        """Return line edit style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QLineEdit {{
                background-color: {theme['widget_bg']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 2px solid {theme['accent']};
            }}
        """

    @staticmethod
    def get_checkbox_style():
        """Return checkbox style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QCheckBox {{
                color: {theme['text']};
                spacing: 5px;
            }}
        """

    @staticmethod
    def get_container_style():
        """Return container style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                border-radius: 15px;
            }}
            QPushButton {{
                background-color: {theme['button']};
                color: {theme['button_text']};
                border: none;
                padding: 5px 15px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme['accent']};
            }}
            QComboBox {{
                background-color: {theme['widget_bg']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 4px;
                padding: 5px;
            }}
        """

    @staticmethod
    def get_label_style():
        """Return label style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QLabel {{
                color: {theme['text']};
            }}
        """
    @staticmethod
    def get_list_widget_style():
        """Return QListWidget style based on the current theme."""
        theme = ThemeManager.get_current_theme()
        return f"""
            QListWidget {{
                background-color: {theme['widget_bg']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 5px;
                font-size: 12px;
                padding: 1px;
            }}
            QListWidget::item {{
                padding: 1px;
                border-bottom: 1px solid lightgray;
            }}
            QListWidget::item:selected {{
                background-color: {theme['accent']};
                color: {theme['button_text']};
            }}
            QListWidget::item:hover {{
                background-color: #E5E5E5;
                color: black;
            }}
        """
    
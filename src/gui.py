import platform
import tkinter as tk
from tkinter import Checkbutton, IntVar, Listbox, Text, filedialog, messagebox, Toplevel, Label, Entry, Button
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
import threading
import time
import psutil
import requests

# Assuming your .env setup and API key retrieval are already correctly implemented
api_key = os.getenv('VIRUSTOTAL_API_KEY')

class AntivirusGUI:
    def __init__(self, master):
        self.master = master
        master.title('Omega Antivirus')
        master.geometry('1024x768')

         # Define colors and load images
        self.dark_bg = '#0a0000'
        self.light_bg = '#fafafa'
        self.accent_color = '#61cf4a'
        self.light_text = "#FFFFFF"
        self.quick_scan_img = ImageTk.PhotoImage(Image.open('img/quick_scan.png'))
        self.full_scan_img = ImageTk.PhotoImage(Image.open('img/full.png'))
        self.real_img = ImageTk.PhotoImage(Image.open('img/pro.png'))
        self.hash_img =ImageTk.PhotoImage(Image.open('img/hash.png'))
        self.quarantine_img = ImageTk.PhotoImage(Image.open('img/quar.png'))
        self.logo_img = ImageTk.PhotoImage(Image.open('img/logo.png'))
        self.privacy_icon_img = ImageTk.PhotoImage(Image.open('img/logo.png'))
        self.about_logo_img = ImageTk.PhotoImage(Image.open('img/about.png'))
        self.help_icon_img = ImageTk.PhotoImage(Image.open('img/help.png'))


        self.setup_sidebar()
        self.setup_content_area()

    def setup_sidebar(self):
        self.sidebar = tk.Frame(root, bg=self.dark_bg, width=200, height=768)
        self.sidebar.pack(side='left', fill='y', padx=20, pady=60)

        buttons_info = {
            "Dashboard": self.show_dashboard,
            "Protection": self.show_protection_options,
            "Privacy": self.show_privacy_dashboard,
            "About": self.show_about_page,
            "Preferences": self.show_preferences_page,
            "Help": self.show_help
        }

        for text, command in buttons_info.items():
            button = tk.Button(self.sidebar, text=text, fg=self.light_text, bg=self.dark_bg, bd=0, padx=20, pady=10, command=command)
            button.pack(fill="x")

    def setup_content_area(self):
        self.content = tk.Frame(root, bg=self.light_bg)
        self.content.pack(expand=True, fill='both')

    def show_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        dashboard_frame = tk.Frame(self.content, bg=self.light_bg)
        dashboard_frame.pack(expand=True, fill='both')

        # Logo and Welcome Message
        logo_label = tk.Label(dashboard_frame, image=self.logo_img, bg=self.light_bg)
        logo_label.image = self.logo_img
        logo_label.pack(pady=20)

        welcome_label = tk.Label(dashboard_frame, text="Welcome to Omega Antivirus", bg=self.light_bg, font=("Helvetica", 20, "bold"), fg=self.accent_color)
        welcome_label.pack()

        # System Information
        system_info_label = tk.Label(dashboard_frame, text="System Information", bg=self.light_bg, font=("Helvetica", 16, "underline"), fg=self.accent_color)
        system_info_label.pack(pady=10)

        current_status_message = "Your PC is running smoothly. All systems are go!"
        status_message_label = tk.Label(dashboard_frame, text=current_status_message, bg=self.light_bg, font=("Helvetica", 16), fg=self.accent_color)
        status_message_label.pack()

        system_info = {
            "Operating System": platform.system(),
            "Processor": platform.processor(),
            "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            "Storage": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
        }
        for key, value in system_info.items():
            info_label = tk.Label(dashboard_frame, text=f"{key}: {value}", bg=self.light_bg, font=("Helvetica", 12))
            info_label.pack()

        
        # Dynamic Status Indicator
        status_label = tk.Label(dashboard_frame, text="Current PC Status", bg=self.light_bg, font=("Helvetica", 16, "underline"), fg=self.accent_color)
        status_label.pack(pady=10)

        status_indicator = tk.Label(dashboard_frame, text="Stable", bg=self.light_bg, fg=self.accent_color, font=("Helvetica", 14, "bold"))
        status_indicator.pack()
    

    def update_content(self, text):
        for widget in self.content.winfo_children():
            widget.destroy()
        tk.Label(self.content, text=text, bg=self.light_bg, font=("Helvetica", 16)).pack(expand=True)

    def show_protection_options(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        options_frame = tk.Frame(self.content, bg=self.light_bg)
        options_frame.pack(expand=True, fill='both')

        scan_options = [
            ("Quick Scan", self.quick_scan_img, "Scans critical areas where malware usually resides.", self.quick_scan),
            ("Advance Scan", self.full_scan_img, "Scans all your files and directories.", self.advance_scan),
            ("Real-time Protection", self.real_img, "Turn ON Real Time Protection", self.real_time_protection),
            ("Hash ID", self.hash_img, "Analysis The malware ID", self.hash_id),
            ("Quarantine", self.quarantine_img, "Show malware quarantine", self.show_quarantine)
        ]

        for option, img, desc, command in scan_options:
            self.create_scan_option(options_frame, option, img, desc, command)
    
    def show_privacy_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        privacy_frame = tk.Frame(self.content, bg=self.light_bg)
        privacy_frame.pack(expand=True, fill='both')

        # Privacy Icon and Message
        privacy_icon_label = tk.Label(privacy_frame, image=self.privacy_icon_img, bg=self.light_bg)
        privacy_icon_label.image = self.privacy_icon_img
        privacy_icon_label.pack(pady=20)

        privacy_message = "Your privacy is our top priority. Customize your settings below:"
        privacy_message_label = tk.Label(privacy_frame, text=privacy_message, bg=self.light_bg, font=("Helvetica", 16), fg=self.accent_color)
        privacy_message_label.pack()

        # Privacy Settings
        privacy_settings = [
            ("Activity Log", "View your activity log", self.show_activity_log),
            ("Location Services", "Manage apps accessing your location", self.manage_location_services),
            ("App Permissions", "Review and adjust app permissions", self.review_app_permissions),
            ("Browser Privacy", "Enhance your browser privacy", self.enhance_browser_privacy),
            ("Clear History", "Clear your browsing and search history", self.clear_history)
        ]

        for option, desc, command in privacy_settings:
            self.create_privacy_option(privacy_frame, option, desc, command)

    def create_privacy_option(self, parent, text, description, command):
        option_frame = tk.Frame(parent, bg="white", padx=10, pady=10)
        option_frame.pack(side="left", expand=True, fill="both", padx=10)

        btn = tk.Button(option_frame, text=text, compound="top", bg=self.accent_color, fg="white", command=command)
        btn.pack(pady=5)

        desc_label = tk.Label(option_frame, text=description, wraplength=150, justify="center", bg="white", fg="black")
        desc_label.pack()

    def show_activity_log(self):
    # Mock data for the activity log
        activity_log = [
        "2024-02-20 10:00:00 - Full scan completed. No threats found.",
        "2024-02-20 14:30:00 - Real-time protection blocked a threat.",
        "2024-02-20 09:15:00 - Update"
    ]
        activity_log_window = Toplevel(self.master)
        activity_log_window.title("Activity Log")
        activity_log_window.geometry("600x400")
    
        log_text = Text(activity_log_window, wrap="word")
        log_text.pack(padx=20, pady=20, fill="both", expand=True)
    
        for entry in activity_log:
            log_text.insert("end", entry + "\n")
        log_text.config(state="disabled") 

    def manage_location_services(self):
        location_settings_window = Toplevel(self.master)
        location_settings_window.title("Location Services")

        location_status_label = Label(location_settings_window, text="Location Services are currently enabled.", font=("Helvetica", 14))
        location_status_label.pack(padx=20, pady=20)

        toggle_location_button = Button(location_settings_window, text="Location Services", command=lambda: self.toggle_location(location_status_label))
        toggle_location_button.pack(pady=10)

    def toggle_location(self, status_label):
        current_status = status_label.cget("text")
        new_status = "Location Services are currently " + ("disabled." if "enabled" in current_status else "enabled.")
        status_label.config(text=new_status)

    def review_app_permissions(self):
        # Simulated data structure to hold app permissions and their states
        self.app_permissions = {
            "App1": {"Camera": True, "Microphone": False, "Location": True},
            "App2": {"Contacts": True, "Storage": False},
            "App3": {"Notifications": True, "Background Refresh": False}
        }

        permissions_window = Toplevel(self.master)
        permissions_window.title("App Permissions")
        permissions_window.geometry("500x400")

        for app, permissions in self.app_permissions.items():
            app_frame = tk.LabelFrame(permissions_window, text=app, padx=10, pady=10)
            app_frame.pack(padx=10, pady=5, fill="x")

            for permission, enabled in permissions.items():
                self._create_permission_toggle(app_frame, app, permission, enabled)
    

    def _create_permission_toggle(self, parent, app_name, permission, enabled):
        var = IntVar(value=enabled)
        chk = Checkbutton(parent, text=permission, variable=var, onvalue=1, offvalue=0,
                          command=lambda: self._toggle_permission(app_name, permission, var))
        chk.pack(anchor="w")
    
    def _toggle_permission(self, app_name, permission, var):
        # Update the app_permissions data structure based on the checkbox state
        self.app_permissions[app_name][permission] = bool(var.get())
        # Placeholder for actual permission toggle logic
        print(f"Permission {permission} for {app_name} set to {'enabled' if var.get() else 'disabled'}")
        messagebox.showinfo("Permission Toggled", f"{permission} for {app_name} {'enabled' if var.get() else 'disabled'}.")

    def enhance_browser_privacy(self):
        browser_privacy_window = Toplevel(self.master)
        browser_privacy_window.title("Enhance Browser Privacy")

        enhance_browser_label = Label(browser_privacy_window, text="Choose options to enhance your browser privacy:", font=("Helvetica", 14))
        enhance_browser_label.pack(padx=20, pady=20)

        clear_cookies_button = Button(browser_privacy_window, text="Clear Cookies", command=self.clear_cookies)
        clear_cookies_button.pack(pady=10)

        enable_tracking_protection_button = Button(browser_privacy_window, text="Enable Tracking Protection", command=self.enable_tracking_protection)
        enable_tracking_protection_button.pack(pady=10)

    def clear_cookies(self):
        messagebox.showinfo("Clear Cookies", "Cookies cleared successfully.")

    def enable_tracking_protection(self):
        messagebox.showinfo("Enable Tracking Protection", "Tracking protection enabled successfully.")

    def clear_history(self):
        messagebox.showinfo("Clear History", "Browsing history cleared successfully.")

    def show_about_page(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        about_frame = tk.Frame(self.content, bg=self.light_bg)
        about_frame.pack(expand=True, fill='both')

    # Cool logo or image for your application
        about_logo_img = ImageTk.PhotoImage(Image.open('img/about.png'))
        about_logo_label = tk.Label(about_frame, image=about_logo_img, bg=self.light_bg)
        about_logo_label.image = about_logo_img
        about_logo_label.pack(pady=20)

    # Application Name and Version
        app_name_label = tk.Label(about_frame, text="Cool Antivirus", font=("Helvetica", 24, "bold"), fg=self.accent_color, bg=self.light_bg)
        app_version_label = tk.Label(about_frame, text="Version 1.0", font=("Helvetica", 16), fg="gray", bg=self.light_bg)
        app_name_label.pack()
        app_version_label.pack(pady=10)

    # Description
        about_description = (
            "Cool Antivirus is a state-of-the-art application designed to protect your PC from all kinds of cyber threats. "
            "With advanced scanning options, real-time protection, and enhanced privacy controls, your digital world is in safe hands."
        )
        description_label = tk.Label(about_frame, text=about_description, font=("Helvetica", 14), wraplength=600, justify="center", bg=self.light_bg, fg="black")
        description_label.pack(pady=20)

    # Credits and Acknowledgments
        credits_label = tk.Label(about_frame, text="Credits & Acknowledgments", font=("Helvetica", 18, "bold"), fg=self.accent_color, bg=self.light_bg)
        credits_label.pack(pady=10)

        about_credits = (
            "Special thanks to our amazing development team for bringing this application to life. "
            "We also extend our gratitude to the open-source community and everyone who contributed to the success of Cool Antivirus."
        )
        credits_description_label = tk.Label(about_frame, text=about_credits, font=("Helvetica", 14), wraplength=600, justify="center", bg=self.light_bg, fg="black")
        credits_description_label.pack(pady=20)

    # Close button
        close_button = tk.Button(about_frame, text="Close", bg=self.accent_color, fg="white", command=lambda: self.update_content("Your PC is Great"))
        close_button.pack(pady=20)

    def show_preferences_page(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        preferences_frame = tk.Frame(self.content, bg=self.light_bg)
        preferences_frame.pack(expand=True, fill='both')

    # Preferences Icon and Message
        preferences_icon_img = ImageTk.PhotoImage(Image.open('img/pref.png'))
        preferences_icon_label = tk.Label(preferences_frame, image=preferences_icon_img, bg=self.light_bg)
        preferences_icon_label.image = preferences_icon_img
        preferences_icon_label.pack(pady=20)

        preferences_message = "Customize your Cool Antivirus experience with the following preferences:"
        preferences_message_label = tk.Label(preferences_frame, text=preferences_message, bg=self.light_bg, font=("Helvetica", 16), fg=self.accent_color)
        preferences_message_label.pack()

    # Preferences Options
        preferences_options = [
            ("Theme", "Choose your favorite color theme", self.choose_theme),
            ("Language", "Select your preferred language", self.select_language),
            ("Backup & Restore", "Backup and restore application settings", self.backup_restore_settings),
            ("Update Preferences", "Keep your preferences up to date", self.update_preferences)
        ]

        for option, desc, command in preferences_options:
            self.create_preferences_option(preferences_frame, option, desc, command)

    def create_preferences_option(self, parent, text, description, command):
        option_frame = tk.Frame(parent, bg="white", padx=10, pady=10)
        option_frame.pack(side="left", expand=True, fill="both", padx=10)

        btn = tk.Button(option_frame, text=text, compound="top", bg=self.accent_color, fg="white", command=command)
        btn.pack(pady=5)

        desc_label = tk.Label(option_frame, text=description, wraplength=150, justify="center", bg="white", fg="black")
        desc_label.pack()

    def choose_theme(self):
        theme_window = Toplevel(self.master)
        theme_window.title("Choose Theme")

        theme_options = [
            ("Dark Theme", "#333333", "#FFFFFF"),
            ("Light Theme", "#F9FEFF", "#333333"),
            ("Green Theme", "#4E9F3D", "#FFFFFF"),
            ("Blue Theme", "#1976D2", "#FFFFFF"),
        ]

        for theme_name, bg_color, text_color in theme_options:
            theme_button = Button(theme_window, text=theme_name, bg=bg_color, fg=text_color, width=20, height=2, command=lambda t=theme_name: self.apply_theme(t))
            theme_button.pack(pady=10)

    def apply_theme(self, selected_theme):
    # Dictionary mapping theme names to corresponding colors
        theme_colors = {
            "Dark Theme": {"bg": "#333333", "fg": "#FFFFFF"},
            "Light Theme": {"bg": "#F9FEFF", "fg": "#333333"},
            "Green Theme": {"bg": "#4E9F3D", "fg": "#FFFFFF"},
            "Blue Theme": {"bg": "#1976D2", "fg": "#FFFFFF"},
        # Add more themes as needed
        }

    # Get the selected theme colors
        selected_theme_colors = theme_colors.get(selected_theme, {"bg": "", "fg": ""})

    # Apply the selected theme to the main window
        self.master.configure(bg=selected_theme_colors["bg"])

    # Apply the selected theme to specific widgets (example: sidebar, content area)
        self.sidebar.configure(bg=selected_theme_colors["bg"])
        self.content.configure(bg=selected_theme_colors["bg"])

    # Apply the selected theme to text and foreground colors
        self.light_text = selected_theme_colors["fg"]

    # Inform the user that the theme has been applied
        messagebox.showinfo("Theme Applied", f"{selected_theme} applied successfully.")

    def choose_theme(self):
        theme_window = Toplevel(self.master)
        theme_window.title("Choose Theme")

        theme_options = [
        ("Dark Theme", "#333333", "#FFFFFF"),
        ("Light Theme", "#F9FEFF", "#333333"),
        ("Green Theme", "#4E9F3D", "#FFFFFF"),
        ("Blue Theme", "#1976D2", "#FFFFFF"),
    ]

        for theme_name, bg_color, text_color in theme_options:
            theme_button = Button(theme_window, text=theme_name, bg=bg_color, fg=text_color, width=20, height=2, command=lambda t=theme_name: self.apply_theme(t))
            theme_button.pack(pady=10)
    def select_language(self):
        language_window = Toplevel(self.master)
        language_window.title("Select Language")

        language_options = [
            ("English", "en_US"),
            ("Spanish", "es_ES"),
            ("French", "fr_FR"),
            ("German", "de_DE"),
        ]

        for language_name, language_code in language_options:
            language_button = Button(language_window, text=language_name, bg=self.accent_color, fg="white", width=20, height=2, command=lambda l=language_name: self.apply_language(l))
            language_button.pack(pady=10)

    def apply_language(self, selected_language):
    # Dictionary mapping language names to corresponding translations
        language_translations = {
        "English": {
            "Dashboard": "Dashboard",
            "Protection": "Protection",
            "Privacy": "Privacy",
            "Notifications": "Notifications",
            "My Account": "My Account",
            "Preferences": "Preferences",
            "Help": "Help",
            "Your PC is Great": "Your PC is Great",
            "Privacy Settings": "Privacy Settings",
            "No new notifications": "No new notifications",
            "Account Information": "Account Information",
            "Set your preferences": "Set your preferences",
            "Get Help and Support": "Get Help and Support",
            "Quick Scan": "Quick Scan",
            "Advance Scan": "Advance Scan",
            "Real-time Protection": "Real-time Protection",
            "Hash ID": "Hash ID",
            "Quarantine": "Quarantine",
            "Activity Log": "Activity Log",
            "View your activity log": "View your activity log",
            "Location Services": "Location Services",
            "Manage apps accessing your location": "Manage apps accessing your location",
            "App Permissions": "App Permissions",
            "Review and adjust app permissions": "Review and adjust app permissions",
            "Browser Privacy": "Browser Privacy",
            "Enhance your browser privacy": "Enhance your browser privacy",
            "Clear History": "Clear History",
            "Choose options to enhance your browser privacy:": "Choose options to enhance your browser privacy:",
            "Clear Cookies": "Clear Cookies",
            "Enable Tracking Protection": "Enable Tracking Protection",
            "File Submitted": "File Submitted",
            "Failed to submit the file for scanning. Error code:": "Failed to submit the file for scanning. Error code:",
            "Scanned": "Scanned",
            "suspicious files detected in": "suspicious files detected in",
            "Scan cancelled, no directory selected.": "Scan cancelled, no directory selected.",
            "Failed to get the scan report.": "Failed to get the scan report.",
            "Failed to submit the file for scanning.": "Failed to submit the file for scanning.",
            "No file selected.": "No file selected.",
            "Scan Complete": "Scan Complete",
            "Detailed Scan Report": "Detailed Scan Report",
            "Suspicious Files": "Suspicious Files",
            "malicious_file_1.exe": "malicious_file_1.exe",
            "malicious_file_2.exe": "malicious_file_2.exe",
            "Detailed Report": "Detailed Report",
            "Suspicious File Details": "Suspicious File Details",
            "Hash Id Result": "Hash Id Result",
            "Choose a file to scan": "Choose a file to scan",
            "Toggle Location Services": "Toggle Location Services",
            "Location Services are currently enabled.": "Location Services are currently enabled.",
            "Location Services are currently disabled.": "Location Services are currently disabled.",
            "Review and adjust app permissions": "Review and adjust app permissions",
            "Tracking protection enabled successfully.": "Tracking protection enabled successfully.",
            "Browsing history cleared successfully.": "Browsing history cleared successfully.",
            "Cookies cleared successfully.": "Cookies cleared successfully.",
            "Clear Cookies": "Clear Cookies",
            "Enable Tracking Protection": "Enable Tracking Protection",
            "Clear History": "Clear History"
        },
        "Spanish": {
                "Dashboard": "Tablero",
                "Protection": "Protección",
                "Privacy": "Privacidad",
                "Notifications": "Notificaciones",
                "My Account": "Mi Cuenta",
                "Preferences": "Preferencias",
                "Help": "Ayuda",
                "Your PC is Great": "Tu PC es Genial",
                "Privacy Settings": "Configuración de Privacidad",
                "No new notifications": "Sin nuevas notificaciones",
                "Account Information": "Información de la Cuenta",
                "Set your preferences": "Configura tus preferencias",
                "Get Help and Support": "Obtener Ayuda y Soporte",
                	    "Quick Scan": "Análisis rápido",
                        "Advance Scan":  "Escaneo avanzado",
            "Real-time Protection": "Protección en tiempo real",
            "Hash ID": "ID de hash",
            "Quarantine": "Cuarentena",
            "Activity Log": "Registro de actividades",
            "View your activity log": "Ver tu registro de actividad",
            "Location Services": "Servicios de localización",
            "Manage apps accessing your location":"Administrar aplicaciones que acceden a su ubicación",
            "App Permissions": "Permisos de aplicaciones",
            "Review and adjust app permissions":"Revisar y ajustar los permisos de la aplicación",
            "Browser Privacy":  "Privacidad del navegador",
            "Enhance your browser privacy": "Mejore la privacidad de su navegador",
            "Clear History": "Borrar historial",
            "Choose options to enhance your browser privacy":"Elija opciones para mejorar la privacidad de su navegador",
            "Clear Cookies": "Eliminar cookies",
            "Enable Tracking Protection": "Habilitar protección de seguimiento",
            "File Submitted": "Archivo enviado",
            "Failed to submit the file for scanning. Error code":"Error al enviar el archivo para escanear. Código de error",
            "Scanned": "Escaneado",
            "suspicious files detected in": "archivos sospechosos detectados en",
            "Scan cancelled, no directory selected.": "Escaneo cancelado, no se seleccionó ningún directorio.",
            "Failed to get the scan report.": "Error al obtener el informe del escaneo.",
            "Failed to submit the file for scanning.": "Error al enviar el archivo para escanear.",
            "No file selected.":"Ningún archivo seleccionado.",
            "Scan Complete": "Escaneo completado",
            "Detailed Scan Report": "Informe de análisis detallado",
            "Suspicious Files":"Archivos sospechosos",
            "malicious_file_1.exe": "malicious_file_1.exe",
            "malicious_file_2.exe":  "malicious_file_2.exe",
            "Detailed Report":  "Reporte detallado",
            "Suspicious File Details": "Detalles del archivo sospechoso",
            "Hash Id Result": "Resultado del ID de hash",
            "Choose a file to scan": "Elija un archivo para escanear",
            "Toggle Location Services": "Alternar servicios de ubicación",
            "Location Services are currently enabled.": "Los servicios de ubicación están actualmente habilitados.",
            "Location Services are currently disabled.": "Los servicios de ubicación están actualmente deshabilitados.",
            "Review and adjust app permissions": "Revisar y ajustar los permisos de la aplicación",
            "Tracking protection enabled successfully.": "La protección de seguimiento se habilitó correctamente.",
            "Browsing history cleared successfully.":"El historial de navegación se borró correctamente.",
            "Cookies cleared successfully.": "Las cookies se borraron correctamente.",
            "Enable Tracking Protection": "Habilitar protección de seguimiento",
            "Clear History": "Borrar historial"
                
            },
        "German": {
    "Dashboard": "Instrumententafel",
    "Protection": "Schutz",
    "Privacy": "Datenschutz",
    "Notifications": "Benachrichtigungen",
    "My Account": "Mein Konto",
    "Preferences": "Einstellungen",
    "Help": "Hilfe",
    "Your PC is Great": "Ihr PC ist großartig",
    "Privacy Settings": "Datenschutzeinstellungen",
    "No new notifications": "Keine neuen Benachrichtigungen",
    "Account Information": "Kontoinformationen",
    "Set your preferences": "Legen Sie Ihre Einstellungen fest",
    "Get Help and Support": "Hilfe und Unterstützung erhalten",
    "Activity Log": "Aktivitätsprotokoll",
    "Location Services": "Standortdienste",
    "Toggle Location Services": "Standortdienste umschalten",
    "Review App Permissions": "App-Berechtigungen überprüfen",
    "Enhance Browser Privacy": "Browser-Datenschutz verbessern",
    "Clear Cookies": "Cookies löschen",
    "Enable Tracking Protection": "Tracking-Schutz aktivieren",
    "Clear History": "Verlauf löschen"
},
"Chinese": {
    "File Submitted": "文件已提交",
    "Failed to submit the file for scanning. Error code": "无法提交文件进行扫描。错误代码",
    "Scan Complete": "扫描完成",
    "Suspicious file detected": "检测到可疑文件",
    "Detailed Scan Report": "详细扫描报告",
    "Hash Id Result": "哈希ID结果",
    "Quick Scan": "快速扫描",
    "Advance Scan": "高级扫描",
    "Real-time Protection": "实时保护",
    "Hash ID": "哈希ID",
    "Quarantine": "隔离区",
    "Select directory for scanning:": "选择扫描目录：",
    "File types to scan (e.g., .exe, .pdf):": "要扫描的文件类型（例如，.exe，.pdf）：",
    "Start Scan": "开始扫描",
    "Scanned": "已扫描",
    "suspicious files detected in": "检测到可疑文件",
    "Real-time protection disabled.": "实时保护已禁用。",
    "Real-time protection enabled.": "实时保护已启用。",
    "Your privacy is our top priority. Customize your settings below:": "您的隐私是我们的首要任务。在下面自定义您的设置：",
    "Activity Log": "活动日志",
    "View your activity log": "查看您的活动日志",
    "Location Services": "位置服务",
    "Manage apps accessing your location": "管理访问您位置的应用",
    "App Permissions": "应用权限",
    "Review and adjust app permissions": "审查并调整应用权限",
    "Browser Privacy": "浏览器隐私",
    "Enhance your browser privacy": "增强您的浏览器隐私",
    "Clear History": "清除历史记录",
    "Clear your browsing and search history": "清除您的浏览和搜索历史",
    "Choose options to enhance your browser privacy:": "选择选项以增强您的浏览器隐私：",
    "Clear Cookies": "清除Cookies",
    "Cookies cleared successfully.": "Cookies已成功清除。",
    "Enable Tracking Protection": "启用跟踪保护",
    "Tracking protection enabled successfully.": "跟踪保护已成功启用。",
    "Clear History": "清除历史记录",
    "Browsing history cleared successfully.": "浏览历史记录已成功清除。",
    "Your PC is Great": "您的电脑很棒",
    "Privacy Settings": "隐私设置",
    "No new notifications": "没有新通知",
    "Account Information": "帐户信息",
    "Set your preferences": "设置您的偏好",
    "Get Help and Support": "获取帮助和支持"
    
},
    }
        

         # Update text content based on the selected language
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, Button):
                widget.config(text=language_translations[selected_language].get(widget.cget("text"), widget.cget("text")))

        for widget in self.content.winfo_children():
            if isinstance(widget, Label):
                widget.config(text=language_translations[selected_language].get(widget.cget("text"), widget.cget("text")))

    # Inform the user that the language has been applied
        messagebox.showinfo("Language Applied", f"{selected_language} language applied successfully.")


    def backup_restore_settings(self):
    # Placeholder logic for backup and restore settings
        backup_location = filedialog.askdirectory()
        if backup_location:
            messagebox.showinfo("Backup & Restore", f"Settings backed up to {backup_location}")
        else:
            messagebox.showwarning("Backup & Restore", "Backup cancelled.")

    def update_preferences(self):
    # Placeholder logic to update preferences
        new_preference_value = simpledialog.askstring("Update Preferences", "Enter new preference value:")
        if new_preference_value:
            messagebox.showinfo("Update Preferences", f"Preferences updated successfully. New value: {new_preference_value}")
        else:
            messagebox.showwarning("Update Preferences", "Update preferences cancelled.")


    def show_help(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        help_frame = tk.Frame(self.content, bg=self.light_bg)
        help_frame.pack(expand=True, fill='both')

    # Help Icon and Message
        help_icon_label = tk.Label(help_frame, image=self.help_icon_img, bg=self.light_bg)
        help_icon_label.image = self.help_icon_img
        help_icon_label.pack(pady=20)

        help_message = "Need assistance? Check out our help resources or contact support:"
        help_message_label = tk.Label(help_frame, text=help_message, bg=self.light_bg, font=("Helvetica", 16), fg=self.accent_color)
        help_message_label.pack()

    # Help Options
        help_options = [
            ("Knowledge Base", "Explore our knowledge base for guides and tutorials", self.explore_knowledge_base),
            ("Contact Support", "Get in touch with our support team", self.contact_support),
            ("FAQs", "Find answers to frequently asked questions", self.show_faqs)
        ]

        for option, desc, command in help_options:
            self.create_help_option(help_frame, option, desc, command)

    def create_help_option(self, parent, text, description, command):
        option_frame = tk.Frame(parent, bg="white", padx=10, pady=10)
        option_frame.pack(side="left", expand=True, fill="both", padx=10)

        btn = tk.Button(option_frame, text=text, compound="top", bg=self.accent_color, fg="white", command=command)
        btn.pack(pady=5)

        desc_label = tk.Label(option_frame, text=description, wraplength=150, justify="center", bg="white", fg="black")
        desc_label.pack()

    def explore_knowledge_base(self):
        knowledge_base_window = Toplevel(self.master)
        knowledge_base_window.title("Knowledge Base")
        Label(knowledge_base_window, text="Explore our knowledge base for helpful guides and tutorials.", font=("Helvetica", 14)).pack(padx=20, pady=20)

    def contact_support(self):
        support_window = Toplevel(self.master)
        support_window.title("Contact Support")
        Label(support_window, text="For assistance, please contact our support team at support@example.com.", font=("Helvetica", 14)).pack(padx=20, pady=20)

    def show_faqs(self):
        faqs_window = Toplevel(self.master)
        faqs_window.title("Frequently Asked Questions")
        Label(faqs_window, text="Find answers to common questions in our FAQs section.", font=("Helvetica", 14)).pack(padx=20, pady=20)

    def create_scan_option(self, parent, text, image, description, command):
        option_frame = tk.Frame(parent, bg="white", padx=10, pady=10, highlightbackground=self.accent_color, highlightthickness=2)
        option_frame.pack(side="left", expand=True, fill="both", padx=10)

        btn = tk.Button(option_frame, image=image, text=text, compound="top", bg=self.accent_color, fg="white", command=command)
        btn.image = image
        btn.pack(pady=5)

        desc_label = tk.Label(option_frame, text=description, wraplength=150, justify="center", bg="white", fg="black")
        desc_label.pack()

    def scan(self, directory_path):
        self.master.update_idletasks()
        suspicious_extensions = ['.exe', '.js', '.bat', '.cmd', '.sh']  # Sample extensions
        found_suspicious_files = []

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in suspicious_extensions):
                    found_suspicious_files.append(os.path.join(root, file))
                    self.progress["value"] += 10
                    self.master.update_idletasks()
                    time.sleep(10)  # Simulated scan delay for demonstration

        
        if found_suspicious_files:
            report_message = f"Scan Complete. Found {len(found_suspicious_files)} suspicious files."
            if messagebox.askyesno("Scan Complete", f"{report_message}\nWould you like to see a detailed report?"):
                detailed_report = "\n".join(found_suspicious_files)
                self.show_detailed_report(detailed_report)
        else:
            messagebox.showinfo("Scan Complete", "No suspicious files found!")
    

    def quick_scan(self):
        directory_path = filedialog.askdirectory()
        if not directory_path:
            messagebox.showinfo("Quick Scan", "Scan cancelled, no directory selected.")
            return
        threading.Thread(target=lambda: self.scan(directory_path)).start()

    
    def show_detailed_report(self, report):
        report_window = Toplevel(self.master)
        report_window.title("Detailed Scan Report")
        text_area = Text(report_window, wrap="word")
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, report)
        text_area.configure(state="disabled")  # Make text area read-only

    def hash_id(self):
        # Prompt the user to select a file
        file_path = filedialog.askopenfilename()
        if not file_path:
            # User cancelled the selection
            messagebox.showinfo("Hash ID", "No file selected.")
            return
        
        # Read the file content
        with open(file_path, 'rb') as file_to_scan:
            files = {'file': (file_path, file_to_scan)}

            headers = {"x-apikey": api_key}
            response = requests.post('https://www.virustotal.com/api/v3/files', headers=headers, files=files)

            if response.status_code == 200:
                # The file was submitted successfully
                data = response.json()
                analysis_id = data['data']['id']

                # Retrieve the analysis results
                report_url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
                report_response = requests.get(report_url, headers=headers)

                if report_response.status_code == 200:
                    report = report_response.json()
                    # Show the result to the user
                    messagebox.showinfo("Hash Id Result", str(report))
                else:
                    messagebox.showerror("Hash ID", "Failed to get the scan report.")
            else:
                messagebox.showerror("Hash ID", "Failed to submit the file for scanning.")
    

    def show_quarantine(self):
        quarantine_window = Toplevel(self.master)
        quarantine_window.title("Quarantined Items")

        listbox = Listbox(quarantine_window)
        listbox.pack(fill="both", expand=True)

        # Just as an example, add some dummy items to the listbox
        listbox.insert("end", "malicious_file_1.exe")
        listbox.insert("end", "malicious_file_2.exe")

    def advance_scan(self):
        advance_scan_window = Toplevel(self.master)
        advance_scan_window.title("Advance Scan Options")
    
        # Directory selection
        Label(advance_scan_window, text="Select directory for scanning:").pack()
        directory_entry = Entry(advance_scan_window, width=50)
        directory_entry.pack()
        Button(advance_scan_window, text="Browse...", command=lambda: self.select_directory(directory_entry)).pack()

        # File types to scan
        Label(advance_scan_window, text="File types to scan (e.g., .exe, .pdf):").pack()
        file_types_entry = Entry(advance_scan_window, width=50)
        file_types_entry.pack()

        # Scan button
        Button(advance_scan_window, text="Start Scan", command=lambda: self.start_advance_scan(directory_entry.get(), file_types_entry.get())).pack()

    def select_directory(self, entry_widget):
        directory = filedialog.askdirectory()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

    def is_file_suspicious(self, file_name):
        # Simulated database of suspicious file criteria
        suspicious_extensions = ['.exe', '.dll', '.bat', '.scr']
        suspicious_keywords = ['keygen', 'crack', 'patch']

        # Check if the file matches any suspicious patterns
        if any(file_name.endswith(ext) for ext in suspicious_extensions):
            return True
        if any(keyword in file_name.lower() for keyword in suspicious_keywords):
            return True
        return False
    
    def start_advance_scan(self, directory, file_types):
        # Adjusted to use self.is_file_suspicious
        if not directory or not file_types:
            messagebox.showerror("Error", "Please select a directory and specify file types to scan.")
            return
        file_types_list = [file_type.strip() for file_type in file_types.split(',')]
        scanned_files_count = 0
        suspicious_files_count = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(file_type) for file_type in file_types_list):
                    scanned_files_count += 1
                    if self.is_file_suspicious(file):
                        suspicious_files_count += 1
                        print(f"Suspicious file detected: {os.path.join(root, file)}")
        messagebox.showinfo("Scan Complete", f"Scanned {scanned_files_count} files; {suspicious_files_count} suspicious files detected in {directory}.")
    
    def real_time_protection(self):
        if hasattr(self, 'real_time_protection_status') and self.real_time_protection_status:
            self.real_time_protection_status = False
            messagebox.showinfo("Real-time Protection", "Real-time protection disabled.")
        else:
            self.real_time_protection_status = True
            messagebox.showinfo("Real-time Protection", "Real-time protection enabled.")


# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = AntivirusGUI(root)
    root.mainloop()


    

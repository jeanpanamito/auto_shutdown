import customtkinter as ctk
import os
import time
import threading
from datetime import datetime, timedelta
from tkinter import messagebox

# Configuration for "Hacker" Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")  # Uses green accents by default

class AutoShutdownApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("SYSTEM CONTROL // AUTO_SHUTDOWN")
        self.geometry("600x500")
        self.resizable(False, False)

        # Custom Hacker Colors
        self.bg_color = "#000000"
        self.term_green = "#00FF41"
        self.term_font = ("Courier New", 14, "bold")
        self.header_font = ("Courier New", 24, "bold")
        
        self.configure(fg_color=self.bg_color)

        # State Variables
        self.shutdown_job = None
        self.target_time = None
        self.is_running = False
        self.warning_shown = False

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.header = ctk.CTkLabel(
            self, 
            text="> INITIATE_SHUTDOWN_PROTOCOL", 
            font=self.header_font, 
            text_color=self.term_green
        )
        self.header.pack(pady=20)

        # Tab Control
        self.tab_view = ctk.CTkTabview(
            self, 
            width=500, 
            height=250, 
            fg_color="#111111", 
            segmented_button_fg_color="#000000",
            segmented_button_selected_color="#222222",
            segmented_button_selected_hover_color="#333333",
            segmented_button_unselected_hover_color="#111111",
            text_color=self.term_green
        )
        self.tab_view.pack(pady=10)

        self.tab_timer = self.tab_view.add(">> COUNTDOWN_TIMER")
        self.tab_exact = self.tab_view.add(">> EXACT_TIME")

        # --- Timer Tab ---
        self.setup_timer_tab()

        # --- Exact Time Tab ---
        self.setup_exact_tab()

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_start = ctk.CTkButton(
            self.btn_frame, 
            text="[ EXECUTE ]", 
            command=self.start_sequence,
            fg_color="#004400", 
            hover_color="#006600",
            border_color=self.term_green,
            border_width=2,
            text_color=self.term_green,
            font=self.term_font,
            width=200
        )
        self.btn_start.pack(side="left", padx=10)

        self.btn_cancel = ctk.CTkButton(
            self.btn_frame, 
            text="[ ABORT ]", 
            command=self.cancel_sequence,
            fg_color="#440000", 
            hover_color="#660000",
            border_color="#FF0000",
            border_width=2,
            text_color="#FF0000",
            font=self.term_font,
            width=200,
            state="disabled"
        )
        self.btn_cancel.pack(side="left", padx=10)

        # Status Display
        self.status_label = ctk.CTkLabel(
            self, 
            text="STATUS: IDLE // WAITING FOR INPUT...", 
            font=self.term_font, 
            text_color=self.term_green
        )
        self.status_label.pack(pady=10)

        self.time_display = ctk.CTkLabel(
            self, 
            text="T-MINUS: 00:00:00", 
            font=("Courier New", 30, "bold"), 
            text_color=self.term_green
        )
        self.time_display.pack(pady=5)

    def setup_timer_tab(self):
        # Entry for Hours
        self.lbl_hrs = ctk.CTkLabel(self.tab_timer, text="HOURS:", font=self.term_font, text_color=self.term_green)
        self.lbl_hrs.grid(row=0, column=0, padx=20, pady=20)
        
        self.entry_hrs = ctk.CTkEntry(self.tab_timer, width=80, font=self.term_font, fg_color="#111111", border_color=self.term_green, text_color=self.term_green)
        self.entry_hrs.grid(row=0, column=1, padx=20, pady=20)
        self.entry_hrs.insert(0, "0")

        # Entry for Minutes
        self.lbl_mins = ctk.CTkLabel(self.tab_timer, text="MINUTES:", font=self.term_font, text_color=self.term_green)
        self.lbl_mins.grid(row=1, column=0, padx=20, pady=20)
        
        self.entry_mins = ctk.CTkEntry(self.tab_timer, width=80, font=self.term_font, fg_color="#111111", border_color=self.term_green, text_color=self.term_green)
        self.entry_mins.grid(row=1, column=1, padx=20, pady=20)
        self.entry_mins.insert(0, "0")

    def setup_exact_tab(self):
        # Entry for Time (HH:MM)
        self.lbl_time = ctk.CTkLabel(self.tab_exact, text="TARGET TIME (HH:MM):", font=self.term_font, text_color=self.term_green)
        self.lbl_time.pack(pady=20)

        self.entry_time = ctk.CTkEntry(self.tab_exact, width=150, font=self.term_font, placeholder_text="23:30", fg_color="#111111", border_color=self.term_green, text_color=self.term_green)
        self.entry_time.pack(pady=10)
        
        self.lbl_hint = ctk.CTkLabel(self.tab_exact, text="(24-HOUR FORMAT)", font=("Courier New", 10), text_color="#666666")
        self.lbl_hint.pack()

    def start_sequence(self):
        if self.is_running:
            return

        mode = self.tab_view.get()
        seconds_remaining = 0

        try:
            if mode == ">> COUNTDOWN_TIMER":
                try:
                    h = int(self.entry_hrs.get())
                except ValueError:
                    h = 0
                try:
                    m = int(self.entry_mins.get())
                except ValueError:
                    m = 0
                
                if h == 0 and m == 0:
                     raise ValueError("Time must be > 0")

                seconds_remaining = (h * 3600) + (m * 60)
                self.target_time = datetime.now() + timedelta(seconds=seconds_remaining)

            elif mode == ">> EXACT_TIME":
                time_str = self.entry_time.get()
                if not time_str:
                     raise ValueError("Enter a time")
                
                try:
                    now = datetime.now()
                    # Parse assuming HH:MM
                    target_dt = datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
                except ValueError:
                     raise ValueError("Invalid Format (HH:MM)")
                
                # If target is earlier today, assume tomorrow
                if target_dt < now:
                    target_dt += timedelta(days=1)
                
                self.target_time = target_dt
                seconds_remaining = (target_dt - now).total_seconds()
            
            # Start Process
            self.is_running = True
            self.warning_shown = False
            self.lock_ui(True)
            self.status_label.configure(text="STATUS: TIMER ACTIVE // RUNNING...", text_color=self.term_green)
            
            # Start countdown thread
            self.shutdown_thread = threading.Thread(target=self.countdown_loop, daemon=True)
            self.shutdown_thread.start()

        except ValueError as ve:
            self.status_label.configure(text=f"ERROR // {str(ve)}", text_color="#FF0000")
        except Exception as e:
            self.status_label.configure(text=f"ERROR // SYSTEM FAILURE", text_color="#FF0000")
            print(e)

    def cancel_sequence(self):
        self.is_running = False
        self.lock_ui(False)
        self.status_label.configure(text="STATUS: SEQUENCE ABORTED", text_color="#FF0000")
        self.time_display.configure(text="T-MINUS: 00:00:00")
        # Ensure system command is cancelled
        os.system("shutdown /a")

    def lock_ui(self, locked):
        state = "disabled" if locked else "normal"
        start_state = "disabled" if locked else "normal"
        cancel_state = "normal" if locked else "disabled"
        
        try:
            self.entry_hrs.configure(state=state)
            self.entry_mins.configure(state=state)
            self.entry_time.configure(state=state)
            self.btn_start.configure(state=start_state)
            self.btn_cancel.configure(state=cancel_state)
        except:
            pass
        
        if locked:
            self.status_label.configure(text="STATUS: SEQUENCE ACTIVE // DO NOT CLOSE", text_color=self.term_green)

    def show_warning(self):
         # Run on main thread to be safe
         def _show():
            try:
                top = ctk.CTkToplevel(self)
                top.title("WARNING")
                top.geometry("400x250")
                top.attributes("-topmost", True)
                top.configure(fg_color="#000000")
                
                # Center the window
                x = self.winfo_x() + 50
                y = self.winfo_y() + 50
                top.geometry(f"+{x}+{y}")
                
                lbl = ctk.CTkLabel(top, text="WARNING: SYSTEM SHUTDOWN IMMINENT\n\n1 MINUTE REMAINING", 
                                   font=("Courier New", 16, "bold"), text_color="#FF0000")
                lbl.pack(pady=40)
                
                btn = ctk.CTkButton(top, text="[ ABORT SHUTDOWN ]", command=lambda: [self.cancel_sequence(), top.destroy()],
                                    fg_color="#440000", hover_color="#660000", text_color="#FF0000", border_color="#FF0000", border_width=2)
                btn.pack()
            except:
                pass
         self.after(0, _show)

    def countdown_loop(self):
        while self.is_running:
            now = datetime.now()
            remaining = self.target_time - now
            total_seconds = int(remaining.total_seconds())

            if total_seconds <= 0:
                self.is_running = False
                # Schedule shutdown execution on main thread/loop to avoid issues, 
                # although os.system is thread-safe usually.
                self.after(0, self.execute_shutdown)
                break

            # Update Display
            # Formatting as HH:MM:SS
            m, s = divmod(total_seconds, 60)
            h, m = divmod(m, 60)
            time_str = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
            
            # Use .after to update UI safely from thread
            self.after(0, lambda t=time_str: self.time_display.configure(text=f"T-MINUS: {t}"))

            # Warning Logic (1 minute mark)
            if 0 < total_seconds <= 60 and not self.warning_shown:
                self.warning_shown = True
                self.after(0, self.show_warning)

            time.sleep(0.5)

    def execute_shutdown(self):
        self.status_label.configure(text="STATUS: EXECUTING SHUTDOWN...", text_color="#FF0000")
        os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    app = AutoShutdownApp()
    app.mainloop()

import tkinter as tk
from tkinter import filedialog, scrolledtext
from drm_analysis import DRMAnalysis
import os
import sys
import io


class PrintLogger(io.StringIO):
    def __init__(self, log_area):
        super().__init__()
        self.log_area = log_area

    def write(self, text):
        self.log_area.insert(tk.END, text)
        self.log_area.yview(tk.END)


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        game_name = os.path.basename(folder_path)
        path_label.config(text=game_name)
    else:
        path_label.config(text="No folder selected")


def decrypt():
    game_name = path_label.cget("text")
    if game_name == "No folder selected":
        log_area.insert(tk.END, "Please select a folder first.\n")
        return

    drm_analysis = DRMAnalysis(game_name)
    availability_section, denuvo_detected = drm_analysis.get_pcgamingwiki_info()

    if denuvo_detected:
        log_area.insert(tk.END, "Denuvo Anti-Tamper detected.\n")
    elif availability_section:
        analysis_result = drm_analysis.analyze_steam_availability(
            availability_section)
        log_area.insert(tk.END, analysis_result)
    else:
        log_area.insert(
            tk.END, "Availability section not found or failed to retrieve data.\n")

    log_area.yview(tk.END)


app = tk.Tk()
app.title('Game Folder Selector')

log_area = scrolledtext.ScrolledText(app, width=40, height=10, state='normal')
log_area.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

path_label = tk.Label(app, text="No folder selected")
path_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

button_frame = tk.Frame(app)
button_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

browse_button = tk.Button(button_frame, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=0, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt)
decrypt_button.grid(row=0, column=1, padx=5)

log_stream = PrintLogger(log_area)
sys.stdout = log_stream

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()
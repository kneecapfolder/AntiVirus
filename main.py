import os
import threading
from time import sleep
import tkinter
import tkinter.messagebox
import customtkinter as tk
import colorama
import scan
import detect_creation

# Get all files from the folder and subfolders
def search_all_subfolders(path):
    subfolders = []
    if os.path.isdir(path):
        for fileName in os.listdir(path):
            if os.path.isdir(path + "/" + fileName):
                subfolders += search_all_subfolders(path + "/" + fileName)
            else:
                subfolders.append(path + "/" + fileName)
    else:
        subfolders.append(path)

    return subfolders

# Write all the files that will be searched
def update_file_status(paths, colors, do_log):
    if do_log:
        files.configure(state=tk.NORMAL)
        files.delete(0.0, "end")

    malicious_count = 0
    malicious_paths = "\n"
    incomplete_flag = True
    for i in range(len(paths)):
        if do_log:
            files.insert("end", paths[i].split("/")[-1] + "\n\n", colors[i])
        
        if (colors[i] == "white"):
            incomplete_flag = False
        if (incomplete_flag and colors[i] == "malicious"):
            malicious_count += 1
            malicious_paths += f"{paths[i]}\n"

    files.configure(state=tk.DISABLED)

    # Check if the scan was completed
    if incomplete_flag and colors[0] != "locked":
        # A lazy replacement for thread locking because i wanna finish this already :)
        colors[0] = "locked"
        log.configure(state=tk.DISABLED)

        print(f"\n\n{malicious_paths}")
        if do_log:
            tkinter.messagebox.showinfo(title="scan completed", message=f"{malicious_count} possibly malicious files found{malicious_paths}")
        elif malicious_count > 0:
            tkinter.messagebox.showwarning(title="malicious files found!", message=f"{malicious_count} possibly malicious files found!{malicious_paths}")



# Scan all files in the paths list
def scan_files(paths, do_log=False):
    threads = []
    colors = ["white"] * len(paths)

    def log_text(text, tag):
        if do_log:
            log.insert("end", text, tag)
            log.see("end")
        else:
            print(text)
        
    update_file_status(paths, colors, do_log)
    for i in range(len(paths)):
        def update_at_index(i, color):
            colors[i] = color
            update_file_status(paths, colors, do_log)

        t = threading.Thread(target=scan.scan_file, args=(paths[i], update_at_index, i, log_text))
        threads.append(t)
        t.start()

def scan_btn():
    path_str = path_input.get()
    log.configure(state=tk.NORMAL)
    log.delete(0.0, "end")

    if not path_str:
        tkinter.messagebox.showerror(title="input error", message="enter a file path")
        return

    scan_files(search_all_subfolders(path_str), True)

# Start background scanning
def check_new_files(choice):
    choice_to_min = {
        "15min": 15,
        "30min": 30,
        "45min": 45,
        "1hr": 60 
    }

    detect_creation.start_thread(choice_to_min[choice] * 60, scan_files)

    
    





    
    

def browse_folders_btn():
    # app.withdraw()
    filename = tk.filedialog.askdirectory(
        title="Select a file",
        initialdir="C:/Users/ilan7/Downloads/"
    )
    path_input.delete(0, tk.END)
    path_input.insert(tk.END, filename)
    # app.deiconify()
    
def browse_files_btn():
    filename = tk.filedialog.askopenfilename(
        title="Select a file",
        initialdir="C:/Users/ilan7/Downloads/",
        filetypes=(("All files","*.*"), ("tiff files","*.tiff"))
    )
    path_input.delete(0, tk.END)
    path_input.insert(tk.END, filename)





# Theme
tk.set_default_color_theme("green")
tk.set_appearance_mode("Dark")
font = lambda size: ("Ariel", size, "bold")

# App frame
app = tk.CTk()
app.geometry("720x505")
app.title("AntiVirus")
app.iconbitmap("images/icon.ico")
app.resizable(False, False)

# UI elements
title = tk.CTkLabel(app, text="ANTIVIRUS", font=font(20))
title.pack(pady=20)

main_frame = tk.CTkFrame(app)
main_frame.pack()


# Path input
# path_var = tkinter.StringVar()
path_input = tk.CTkEntry(main_frame, placeholder_text="Enter a file path", width=290, height=40) # , textvariable=path_var)
path_input.pack(padx=(10, 0), pady=10, side=tk.LEFT)

# Browse files btn
browse_files = tk.CTkButton(main_frame, text="files", command=browse_files_btn, fg_color="gray", hover_color="darkgray", width=60, height=40, font=("Ariel", 15, "bold"))
browse_files.pack(padx=10, side=tk.RIGHT)

# Browse folders btn
browse_folders = tk.CTkButton(main_frame, text="directories", command=browse_folders_btn, fg_color="gray", hover_color="darkgray", width=100, height=40, font=("Ariel", 15, "bold"))
browse_folders.pack(padx=(10, 0), side=tk.RIGHT)


# Scan button
btn = tk.CTkButton(app, text="SCAN", command=scan_btn, font=font(35), width=490, height=60)
btn.pack()

log_frame = tk.CTkFrame(app)
log_frame.pack(pady=(30, 0))

# Log files in path
files = tk.CTkTextbox(log_frame, width=225, state=tk.DISABLED)
files.pack(padx=(10, 10), pady=10, side=tk.LEFT)
files.tag_config("white", foreground="white")
files.tag_config("clean", foreground="lime") 
files.tag_config("malicious", foreground="red")
files.tag_config("unfound", foreground="darkgray", overstrike=1)

# Log scaning
log = tk.CTkTextbox(log_frame, width=225, wrap="word", state=tk.DISABLED)
log.pack(padx=10, side=tk.RIGHT)
log.tag_config("white", foreground="white")
log.tag_config("yellow", foreground="yellow")
log.tag_config("green", foreground="lime") 
log.tag_config("red", foreground="red")
# log.tag_config("clean", background="white", foreground="green")
# log.tag_config("danger", background="white", foreground="red")

# Make the frame invisible
# auto_frame = tk.CTkFrame(app, fg_color="#242424")
auto_frame = tk.CTkFrame(app)
auto_frame.pack(padx=(0, 220), pady=(10, 0))

# Run background scan on new files (Keep app running)
auto_scan_text = tk.CTkLabel(auto_frame, text="Auto scan every:", font=font(20), text_color="gray50")
auto_scan_text.pack(padx=10, pady=10, side=tk.LEFT)

timing_options = ["15min", "30min", "45min", "1hr"]
selected_timing = tk.StringVar(value=timing_options[0])
auto_scan_timing = tk.CTkOptionMenu(auto_frame, values=timing_options, variable=selected_timing, command=check_new_files, width=80)
auto_scan_timing.pack(padx=(0, 10), side=tk.RIGHT)

check_new_files("15min")



#run app
detect_creation.start()
app.mainloop()

detect_creation.exit_event.set()

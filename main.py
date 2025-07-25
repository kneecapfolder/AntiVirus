import os
from threading import Thread
import tkinter
import tkinter.messagebox
import customtkinter as tk
import colorama
import scan

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
def list_files(paths, colors):
    files.configure(state=tk.NORMAL)
    files.delete(0.0, "end")
    malicious_count = 0
    completed = True
    for i in range(len(paths)):
        files.insert("end", paths[i].split("/")[-1] + "\n\n", colors[i])
        if (colors[i] == "white"):
            completed = False
        if (completed and colors[i] == "malicious"):
            malicious_count += 1

    files.configure(state=tk.DISABLED)

    if (completed):
        tkinter.messagebox.showinfo(title="scan completed", message=f"{malicious_count} possibly malicious files found")


# Scan files
def scan_btn():
    path_str = path_input.get()
    log.configure(state=tk.NORMAL)
    log.delete(0.0, "end")

    if not path_str:
        tkinter.messagebox.showerror(title="input error", message="enter a file path")
        return
    
    def log_text(text, tag):
        log.insert("end", text, tag)
        log.see("end")

    threads = []
    paths = search_all_subfolders(path_str)
    colors = ["white"] * len(paths)
    list_files(paths, colors)
    for i in range(len(paths)):
        t = Thread(target=scan.scan_file, args=(
            paths[i], lambda: list_files(paths, colors),
            colors, i, log_text
        ))
        threads.append(t)
        t.start()

    
    # for t in threads:
    #     t.join()
    # list_files(paths, colors)
    
    

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
font = lambda size: ("Ariel", size, "bold")

# App frame
app = tk.CTk()
app.geometry("720x480")
app.title("AntiVirus")
app.iconbitmap("icon.ico")

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
log_frame.pack(pady=(40, 0))

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







#run app
app.mainloop()



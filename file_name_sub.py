import os
import glob
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def remove_SI_block(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    new_lines = []
    skip = False
    for line in lines:
        if line.strip().startswith("SI"):
            skip = True
        elif len(line.strip()) == 2 and not line.strip().startswith('  '):
            skip = False
        if not skip:
            new_lines.append(line)

    with open(filepath, 'w') as file:
        file.writelines(new_lines)

def process_idstv_file(idstv_file, text_to_remove):
    with open(idstv_file, 'r') as file:
        content = file.read()

    # Escape special characters in user input
    text_to_remove = re.escape(text_to_remove)

    # Remove user input text from between <Name> tags
    content = re.sub(f'(<Name>.*?){text_to_remove}(.*?</Name>)', r'\1\2', content)

    # Replace content between <RemnantLocation> tags with 'v'
    content = re.sub(r'<RemnantLocation>.*?</RemnantLocation>', '<RemnantLocation>v</RemnantLocation>', content)

    with open(idstv_file, 'w') as file:
        file.write(content)

def browse_dir():
    dir_path = filedialog.askdirectory()
    directory.set(dir_path)

def process_files():
    # Check if directory exists
    if not os.path.isdir(directory.get()):
        messagebox.showerror("Error", "The directory does not exist")
        return

    # Check if text to remove is empty
    if not text_to_remove.get():
        messagebox.showerror("Error", "Text to remove cannot be empty")
        return

    # Get all nc1 and idstv files
    nc1_files = glob.glob(os.path.join(directory.get(), '*.nc1'))
    idstv_files = glob.glob(os.path.join(directory.get(), '*.idstv'))

    # Check if there are nc1 or idstv files in the directory
    if not nc1_files and not idstv_files:
        messagebox.showinfo("Info", "No .nc1 or .idstv files found in the directory")
        return

    # Process each nc1 file
    for file in nc1_files:
        remove_SI_block(file)

    # Process each idstv file
    for file in idstv_files:
        process_idstv_file(file, text_to_remove.get())

    messagebox.showinfo("Success", "Files processed successfully")

root = tk.Tk()

directory = tk.StringVar()
text_to_remove = tk.StringVar()

tk.Label(root, text="Directory Path").grid(row=0)
tk.Entry(root, textvariable=directory).grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_dir).grid(row=0, column=2)

tk.Label(root, text="Text to Remove").grid(row=1)
tk.Entry(root, textvariable=text_to_remove).grid(row=1, column=1)

tk.Button(root, text="Process Files", command=process_files).grid(row=2, column=1)

root.mainloop()

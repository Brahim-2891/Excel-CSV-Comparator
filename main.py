import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Initialize GUI
root = tk.Tk()
root.title("Excel/CSV File Comparator")
root.geometry("400x300")

# Global variables to hold file paths
file_paths = []

# Function to upload files
def upload_file():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    if filepath:
        file_paths.append(filepath)
        lbl_file.config(text="\n".join(file_paths))

# Function to process and compare files
def process_files():
    if len(file_paths) != 3:
        messagebox.showerror("Error", "Please upload exactly three files.")
        return
    
    identifier_column = entry_column.get()
    if not identifier_column:
        messagebox.showerror("Error", "Please specify an identifier column.")
        return

    # Load files and compare
    try:
        dfs = [pd.read_excel(fp) if fp.endswith('.xlsx') else pd.read_csv(fp) for fp in file_paths]
        unique_entries = pd.concat(dfs).drop_duplicates(subset=[identifier_column], keep=False)
        unique_entries.to_excel("unique_entries.xlsx", index=False)
        messagebox.showinfo("Success", "Unique entries saved to unique_entries.xlsx")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Components
btn_upload = tk.Button(root, text="Upload File", command=upload_file)
btn_upload.pack(pady=10)

lbl_file = tk.Label(root, text="No files uploaded", wraplength=300)
lbl_file.pack()

lbl_column = tk.Label(root, text="Unique Identifier Column (e.g., ID or Name):")
lbl_column.pack(pady=5)

entry_column = tk.Entry(root)
entry_column.pack()

btn_process = tk.Button(root, text="Process Files", command=process_files)
btn_process.pack(pady=10)

root.mainloop()

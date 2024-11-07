import customtkinter as ctkt  # Import CustomTkinter
from customtkinter import filedialog, messagebox
import pandas as pd

# Initialize GUI
root = ctkt.CTk()
root.geometry("400x300")
root.title("Excel/CSV File Comparator")

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

    try:
        dfs = [pd.read_excel(fp) if fp.endswith('.xlsx') else pd.read_csv(fp) for fp in file_paths]
        unique_entries = pd.concat(dfs).drop_duplicates(subset=[identifier_column], keep=False)
        unique_entries.to_excel("unique_entries.xlsx", index=False)
        messagebox.showinfo("Success", "Unique entries saved to unique_entries.xlsx")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create frames for better organization
upload_frame = ctkt.CTkFrame(master=root)
upload_frame.pack(pady=10)

process_frame = ctkt.CTkFrame(master=root)
process_frame.pack(pady=10)


# GUI Components - Upload Frame
btn_upload = ctkt.CTkButton(master=upload_frame, text="Upload File", command=upload_file)
btn_upload.pack(pady=10)

lbl_file = ctkt.CTkLabel(master=upload_frame, text="No files uploaded", wraplength=300)
lbl_file.pack()


# GUI Components - Process frame
lbl_column = ctkt.CTkLabel(master=process_frame, text="Unique Identifier Column (e.g., ID or Name):")
lbl_column.pack(pady=5)

entry_column = ctkt.CTkEntry(master=process_frame, width=200)
entry_column.pack()

btn_process = ctkt.CTkButton(master=process_frame, text="Process Files", command=process_files)
btn_process.pack(pady=10)


root.mainloop()
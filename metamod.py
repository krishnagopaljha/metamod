import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import json


class MetadataEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meta Mod")
        self.file_path = None

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        # File selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        tk.Button(file_frame, text="Open File", command=self.open_file).pack(side=tk.LEFT, padx=5)
        self.file_label = tk.Label(file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)

        # Metadata display
        metadata_frame = tk.LabelFrame(self.root, text="Metadata", padx=10, pady=10)
        metadata_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(metadata_frame, columns=("Key", "Value"), show="headings")
        self.tree.heading("Key", text="Key")
        self.tree.heading("Value", text="Value")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_item)  # Bind item selection to populate fields

        # Editing controls
        edit_frame = tk.Frame(self.root)
        edit_frame.pack(pady=10)

        tk.Label(edit_frame, text="Key").grid(row=0, column=0, padx=5, pady=5)
        self.key_entry = tk.Entry(edit_frame)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_frame, text="Value/New Key").grid(row=0, column=2, padx=5, pady=5)
        self.value_entry = tk.Entry(edit_frame)
        self.value_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(edit_frame, text="Add/Update", command=self.add_update_metadata).grid(row=0, column=4, padx=5, pady=5)
        tk.Button(edit_frame, text="Rename Key", command=self.rename_metadata_key).grid(row=0, column=5, padx=5, pady=5)
        tk.Button(edit_frame, text="Delete Tag", command=self.delete_metadata_tag).grid(row=0, column=6, padx=5, pady=5)
        tk.Button(edit_frame, text="Save File", command=self.save_file).grid(row=0, column=7, padx=5, pady=5)

        # Remove All Metadata button
        tk.Button(
            self.root,
            text="Remove All Metadata",
            command=self.remove_all_metadata,
            bg="red",
            fg="white"
        ).pack(pady=10, padx=10, fill="x")

    def open_file(self):
        """Open a file and display its metadata."""
        self.file_path = filedialog.askopenfilename()
        if not self.file_path:
            return

        self.file_label.config(text=self.file_path)
        self.display_metadata()

    def display_metadata(self):
        """Display metadata of the selected file."""
        self.tree.delete(*self.tree.get_children())  # Clear previous data

        try:
            # Use exiftool to extract metadata
            command = ["exiftool", "-json", self.file_path]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            metadata = json.loads(result.stdout)[0]

            for key, value in metadata.items():
                self.tree.insert("", "end", values=(key, value))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load metadata: {e}")

    def select_item(self, event):
        """Populate entry fields when a tree item is selected."""
        selected_item = self.tree.focus()
        if selected_item:
            key, value = self.tree.item(selected_item, "values")
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key)
            self.value_entry.delete(0, tk.END)
            self.value_entry.insert(0, value)

    def add_update_metadata(self):
        """Add or update a specific metadata key with a new value."""
        key = self.key_entry.get().strip()
        value = self.value_entry.get().strip()

        if not key or not value:
            messagebox.showwarning("Warning", "Key and Value cannot be empty.")
            return

        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        try:
            # Use exiftool to add/update metadata and prevent backup file creation
            command = ["exiftool", "-overwrite_original", f"-{key}={value}", self.file_path]
            subprocess.run(command, capture_output=True, check=True)
            self.display_metadata()  # Refresh metadata tree
            messagebox.showinfo("Success", f"Metadata key '{key}' updated/added successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to update metadata:\n{e.stderr.decode().strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def rename_metadata_key(self):
        """Rename an existing metadata key."""
        old_key = self.key_entry.get().strip()
        new_key = self.value_entry.get().strip()

        if not old_key or not new_key:
            messagebox.showwarning("Warning", "Old Key and New Key cannot be empty.")
            return

        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        try:
            # Copy old key's value to new key
            copy_command = ["exiftool", "-overwrite_original", f"-{new_key}<={old_key}", self.file_path]
            subprocess.run(copy_command, capture_output=True, check=True)

            # Remove old key
            delete_command = ["exiftool", "-overwrite_original", f"-{old_key}=", self.file_path]
            subprocess.run(delete_command, capture_output=True, check=True)

            self.display_metadata()  # Refresh metadata tree
            messagebox.showinfo("Success", f"Metadata key '{old_key}' renamed to '{new_key}'.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to rename metadata key:\n{e.stderr.decode().strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def delete_metadata_tag(self):
        """Delete a selected metadata tag."""
        key = self.key_entry.get().strip()

        if not key:
            messagebox.showwarning("Warning", "No key selected for deletion.")
            return

        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        try:
            # Use exiftool to delete metadata tag and prevent backup file creation
            command = ["exiftool", "-overwrite_original", f"-{key}=", self.file_path]
            subprocess.run(command, capture_output=True, check=True)
            self.display_metadata()  # Refresh metadata tree
            messagebox.showinfo("Success", f"Metadata key '{key}' deleted successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to delete metadata:\n{e.stderr.decode().strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def remove_all_metadata(self):
        """Remove all metadata from the file."""
        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to remove ALL metadata? This action cannot be undone.",
            icon="warning"
        )
        if not confirm:
            return

        try:
            # Use exiftool to remove all metadata and prevent backup file creation
            command = ["exiftool", "-overwrite_original", "-all=", self.file_path]
            subprocess.run(command, capture_output=True, check=True)
            self.display_metadata()  # Refresh metadata tree
            messagebox.showinfo("Success", "All metadata has been removed.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to remove all metadata:\n{e.stderr.decode().strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def save_file(self):
        """Save the updated file."""
        if not self.file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if not save_path:
            return

        try:
            # Use exiftool to copy metadata to the new file
            command = ["exiftool", "-overwrite_original", "-o", save_path, self.file_path]
            subprocess.run(command, capture_output=True, check=True)
            messagebox.showinfo("Success", "File saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MetadataEditorApp(root)
    root.mainloop()

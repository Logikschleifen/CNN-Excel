import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class PixelExporter(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        self.select_btn = tk.Button(self, text="Select Image", command=self.select_image)
        self.select_btn.pack(fill="x")

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image file",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*")]
        )
        if not file_path:
            return
        try:
            img = Image.open(file_path)
        except (IOError, FileNotFoundError):
            messagebox.showerror("Error", "Failed to open the file. Please select a valid image.")
            return

        # Ensure correct dimensions
        if img.size != (28, 28):
            messagebox.showerror("Invalid Size", f"Image size is {img.size}. Please select a 28x28 image.")
            return

        # Convert to grayscale to get single intensity value per pixel
        gray = img.convert("L")
        pixels = list(gray.getdata())

        # Build TSV output row by row
        tsv_rows = []
        for y in range(28):
            row = pixels[y*28:(y+1)*28]
            tsv_rows.append("\t".join(str(val) for val in row))
        tsv_text = "\n".join(tsv_rows)

        # Copy to clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(tsv_text)
        self.master.update()  # now it stays on the clipboard after the window is closed

        messagebox.showinfo("Success", "Pixel data copied to clipboard! Paste into libre office calc.\nIf your using excel then have more self respect.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("28x28 Pixel Exporter")
    root.geometry("300x50")
    app = PixelExporter(master=root)
    root.mainloop()
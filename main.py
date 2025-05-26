import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from image_processor import ImageProcessor
from ocr_handler import OCRHandler

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Application")
        self.root.geometry("1200x800")

        self.image_processor = ImageProcessor()
        self.ocr_handler = OCRHandler()
        
        self.setup_ui()
        
        self.original_image = None
        self.current_image = None
        self.photo_image = None

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Image display
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Buttons
        ttk.Button(button_frame, text="Open Image", command=self.open_image).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Convert to Grayscale", command=self.convert_to_grayscale).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Add Warm Tone", command=self.add_warm_tone).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Enhance Sharpness", command=self.enhance_sharpness).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Extract Text", command=self.extract_text).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=5, padx=5)

        # Text display
        self.text_display = tk.Text(main_frame, height=10, width=80)
        self.text_display.grid(row=2, column=0, columnspan=2, pady=10)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.update_image_display()
                self.text_display.delete(1.0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")

    def update_image_display(self):
        if self.current_image:
            # Resize image to fit display while maintaining aspect ratio
            display_size = (800, 600)
            display_image = self.current_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            self.photo_image = ImageTk.PhotoImage(display_image)
            self.image_label.configure(image=self.photo_image)

    def convert_to_grayscale(self):
        if self.current_image:
            self.current_image = self.image_processor.convert_to_grayscale(self.current_image)
            self.update_image_display()

    def add_warm_tone(self):
        if self.current_image:
            if self.current_image.mode != 'RGB':
                self.current_image = self.current_image.convert('RGB')
            self.current_image = self.image_processor.add_warm_tone(self.current_image)
            self.update_image_display()

    def enhance_sharpness(self):
        if self.current_image:
            self.current_image = self.image_processor.enhance_sharpness(self.current_image)
            self.update_image_display()

    def extract_text(self):
        if self.current_image:
            text = self.ocr_handler.extract_text(self.current_image)
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, text)

    def save_image(self):
        if self.current_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    self.current_image.save(file_path)
                    messagebox.showinfo("Success", "Image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
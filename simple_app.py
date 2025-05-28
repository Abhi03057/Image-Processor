import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_processor import ImageProcessor

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Processing App")
        self.root.geometry("800x600")
        
        self.image_processor = ImageProcessor()
        self.setup_ui()
        
        self.original_image = None
        self.current_image = None
        self.photo = None
        
    def setup_ui(self):
        # Upload button
        self.upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)
        
        # Image display
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        
        # Control buttons
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)
        
        tk.Button(controls_frame, text="Grayscale", command=self.convert_to_grayscale).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Warm Tone", command=self.add_warm_tone).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Sharpen", command=self.enhance_sharpness).pack(side=tk.LEFT, padx=5)
        tk.Button(controls_frame, text="Restore Original", command=self.restore_original).pack(side=tk.LEFT, padx=5)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image.copy()
            self.update_display()
            
    def update_display(self):
        if self.current_image:
            # Resize image to fit display
            display_size = (600, 400)
            image_copy = self.current_image.copy()
            image_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(image_copy)
            self.image_label.config(image=self.photo)
            
    def convert_to_grayscale(self):
        if self.current_image:
            self.current_image = self.image_processor.convert_to_grayscale(self.current_image)
            self.update_display()
            
    def add_warm_tone(self):
        if self.current_image:
            if self.current_image.mode != 'RGB':
                self.current_image = self.current_image.convert('RGB')
            self.current_image = self.image_processor.add_warm_tone(self.current_image)
            self.update_display()
            
    def enhance_sharpness(self):
        if self.current_image:
            self.current_image = self.image_processor.enhance_sharpness(self.current_image)
            self.update_display()
            
    def restore_original(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.update_display()

def main():
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
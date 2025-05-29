import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from image_processor import ImageProcessor
from ocr_handler import OCRHandler

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Processing App")
        self.root.geometry("900x700")

        self.image_processor = ImageProcessor()
        self.ocr_handler = OCRHandler()
        
        self.original_image = None
        self.current_image = None
        self.photo = None

        self.setup_ui()

    def setup_ui(self):
        self.upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)

        btns = [
            ("Grayscale", self.convert_to_grayscale),
            ("Warm Tone", self.add_warm_tone),
            ("Sharpen", self.enhance_sharpness),
            ("Gaussian Blur", self.gaussian_blur),
            ("Median Blur", self.median_blur),
            ("Sepia", self.sepia_filter),
            ("Brightness/Contrast", self.brightness_contrast),
            ("Rotate", self.rotate_image),
            ("Flip Horizontal", self.flip_horizontal),
            ("Flip Vertical", self.flip_vertical),
            ("Edge Detect", self.edge_detection),
            ("OCR Extract Text", self.extract_text),
            ("Restore Original", self.restore_original),
        ]

        for (text, cmd) in btns:
            btn = tk.Button(controls_frame, text=text, command=cmd)
            btn.pack(side=tk.LEFT, padx=3, pady=3)

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
            display_size = (700, 500)
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

    def gaussian_blur(self):
        if self.current_image:
            self.current_image = self.image_processor.apply_gaussian_blur(self.current_image)
            self.update_display()

    def median_blur(self):
        if self.current_image:
            self.current_image = self.image_processor.apply_median_blur(self.current_image)
            self.update_display()

    def sepia_filter(self):
        if self.current_image:
            self.current_image = self.image_processor.apply_sepia(self.current_image)
            self.update_display()

    def brightness_contrast(self):
        if self.current_image:
            brightness = simpledialog.askfloat("Brightness", "Enter brightness (e.g. 1.0):", minvalue=0.0, maxvalue=3.0)
            contrast = simpledialog.askfloat("Contrast", "Enter contrast (e.g. 1.0):", minvalue=0.0, maxvalue=3.0)
            if brightness is not None and contrast is not None:
                self.current_image = self.image_processor.adjust_brightness_contrast(
                    self.current_image, brightness, contrast)
                self.update_display()

    def rotate_image(self):
        if self.current_image:
            angle = simpledialog.askinteger("Rotate", "Enter rotation angle (degrees):")
            if angle is not None:
                self.current_image = self.image_processor.rotate_image(self.current_image, angle)
                self.update_display()

    def flip_horizontal(self):
        if self.current_image:
            self.current_image = self.image_processor.flip_horizontal(self.current_image)
            self.update_display()

    def flip_vertical(self):
        if self.current_image:
            self.current_image = self.image_processor.flip_vertical(self.current_image)
            self.update_display()

    def edge_detection(self):
        if self.current_image:
            self.current_image = self.image_processor.edge_detection(self.current_image)
            self.update_display()

    def extract_text(self):
        if self.current_image:
            text = self.ocr_handler.extract_text(self.current_image)
            messagebox.showinfo("OCR Extracted Text", text if text else "No text detected.")

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

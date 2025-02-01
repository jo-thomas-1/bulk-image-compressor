import os
import sys
from PIL import Image
from tqdm import tqdm

class ImageCompressor:
    def __init__(self, input_folder, output_folder, quality=80, max_width=1024):
        """
        Initializes the ImageCompressor with input folder, output folder, and quality setting.
        :param input_folder: Path to the folder containing images to be compressed.
        :param output_folder: Path where compressed images will be saved.
        :param quality: Quality setting for image compression (default: 80).
        :param max_width: Maximum width for resized images (default: 1024 pixels).
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality = quality
        self.max_width = max_width
        self.images = self._get_images()
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def _get_images(self):
        """
        Retrieves a list of image files from the input folder.
        :return: List of image filenames.
        """
        return [f for f in os.listdir(self.input_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]

    def compress_images(self):
        """
        Compresses all images in the input folder and saves them to the output folder.
        """
        total_images = len(self.images)
        if total_images == 0:
            print("No images found in the input folder.")
            return
        
        print(f"Found {total_images} images. Starting compression...")
        
        # Loop through each image and compress it
        for index, image_name in enumerate(tqdm(self.images, desc="Compressing", unit="image")):
            self._compress_image(image_name)
            print(f"Compressed: {index + 1}/{total_images} - Remaining: {total_images - (index + 1)}")
        
        print("Compression complete!")

    def _compress_image(self, image_name):
        """
        Compresses a single image and saves it to the output folder.
        :param image_name: Name of the image file to compress.
        """
        input_path = os.path.join(self.input_folder, image_name)
        output_path = os.path.join(self.output_folder, os.path.splitext(image_name)[0] + ".webp")

        with Image.open(input_path) as img:
            img = img.convert("RGB")  # Ensuring RGB format for compatibility
            
            # Resize image if it exceeds max_width
            if img.width > self.max_width:
                new_height = int((self.max_width / img.width) * img.height)
                img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save as WebP format for better compression
            img.save(output_path, format="WebP", quality=self.quality, optimize=True)

if __name__ == "__main__":
    """
    Main script execution: Parses command-line arguments and starts the compression process.
    """
    if len(sys.argv) < 3:
        print("Usage: python bulk_image_compressor.py <input_folder> <output_folder> [quality] [max_width]")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    max_width = int(sys.argv[4]) if len(sys.argv) > 4 else 1024
    
    # Create an instance of ImageCompressor and start compression
    compressor = ImageCompressor(input_folder, output_folder, quality, max_width)
    compressor.compress_images()

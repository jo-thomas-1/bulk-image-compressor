import os
import sys
from PIL import Image
from tqdm import tqdm

class ImageCompressor:
    def __init__(self, input_folder, output_folder, quality=80, resize=False, max_width=1024, output_format='jpeg'):
        """
        Initializes the ImageCompressor with input folder, output folder, and quality setting.
        :param input_folder: Path to the folder containing images to be compressed.
        :param output_folder: Path where compressed images will be saved.
        :param quality: Quality setting for image compression (default: 80).
        :param resize: Flag to enable/disable resizing (default: False).
        :param max_width: Maximum width for resized images (default: 1024 pixels).
        :param output_format: Desired output image format (default: jpeg). Supports 'jpeg', 'png', 'webp'.
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality = quality
        self.resize = resize
        self.max_width = max_width
        self.output_format = output_format.lower()
        self.images = self._get_images()
        
        # Validate output format
        if self.output_format not in ['jpeg', 'png', 'webp']:
            print("Invalid output format. Defaulting to 'jpeg'.")
            self.output_format = 'jpeg'
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def _get_images(self):
        """
        Retrieves a list of image files from the input folder.
        :return: List of image filenames.
        """
        return [f for f in os.listdir(self.input_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp', 'tiff', 'gif', 'bmp'))]

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
        with tqdm(total=total_images, desc="Compressing", unit="image") as pbar:
            for index, image_name in enumerate(self.images):
                self._compress_image(image_name)
                pbar.update(1)
                # Print out file count status of image compressions
                # tqdm.write(f"Compressed: {index + 1}/{total_images} - Remaining: {total_images - (index + 1)}")
        
        print("Compression complete!")

    def _compress_image(self, image_name):
        """
        Compresses a single image and saves it to the output folder.
        If compression fails, logs the error and continues with remaining images.
        :param image_name: Name of the image file to compress.
        """
        input_path = os.path.join(self.input_folder, image_name)
        output_path = os.path.join(self.output_folder, os.path.splitext(image_name)[0] + f".{self.output_format}")

        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")  # Ensuring RGB format for compatibility
                
                # Resize image if resizing is enabled and it exceeds max_width
                if self.resize and img.width > self.max_width:
                    new_height = int((self.max_width / img.width) * img.height)
                    img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save the image in the requested format
                img.save(output_path, format=self.output_format.upper(), quality=self.quality, optimize=True)
        
        except Exception as e:
            tqdm.write(f"Error :: {input_path} :: {e}")

if __name__ == "__main__":
    """
    Main script execution: Parses command-line arguments and starts the compression process.
    """
    if len(sys.argv) < 3:
        print("Usage: python bulk_image_compressor.py <input_folder> <output_folder> [quality] [resize] [max_width] [output_format]")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    quality = int(sys.argv[3]) if len(sys.argv) > 3 else 80
    resize = bool(int(sys.argv[4])) if len(sys.argv) > 4 else False
    max_width = int(sys.argv[5]) if len(sys.argv) > 5 else 1024
    output_format = sys.argv[6] if len(sys.argv) > 6 else 'jpeg'
    
    # Create an instance of ImageCompressor and start compression
    compressor = ImageCompressor(input_folder, output_folder, quality, resize, max_width, output_format)
    compressor.compress_images()

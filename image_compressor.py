import os
import sys
import argparse
from PIL import Image
from tqdm import tqdm

class ImageCompressor:
    def __init__(self, input_folder, output_folder, quality=80, resize=False, max_width=1024, output_format='jpeg', recursive=False, break_structure=False):
        """
        Initializes the ImageCompressor with input folder, output folder, and quality setting.
        :param input_folder: Path to the folder containing images to be compressed.
        :param output_folder: Path where compressed images will be saved.
        :param quality: Quality setting for image compression (default: 80).
        :param resize: Flag to enable/disable resizing (default: False).
        :param max_width: Maximum width for resized images (default: 1024 pixels).
        :param output_format: Desired output image format (default: jpeg). Supports 'jpg', 'jpeg', 'png', 'webp'.
        :param recursive: Flag to enable recursive image search (default: False).
        :param break_structure: Flag to break folder structure in output (default: False).
        """

        # Check if input folder exists
        if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
            raise FileNotFoundError(f"Error: Input folder '{input_folder}' does not exist or is not a directory.")
        
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.quality = quality
        self.resize = resize
        self.max_width = max_width
        self.output_format = output_format.lower()
        self.recursive = recursive
        self.break_structure = break_structure
        self.images = self._get_images()
        
        # Validate output format
        if self.output_format in ['jpg', 'jpeg']:
            self.output_format = 'jpeg'
        elif self.output_format not in ['jpeg', 'png', 'webp']:
            print("Invalid output format. Defaulting to 'jpeg'.")
            self.output_format = 'jpeg'
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def _get_images(self):
        """
        Retrieves a list of image files from the input folder. If recursive is enabled, it processes subdirectories.
        :return: List of tuples containing image file paths and their corresponding output paths.
        """
        image_files = []
        if self.recursive:
            for root, _, files in os.walk(self.input_folder):
                for file in files:
                    if file.lower().endswith(('jpg', 'jpeg', 'png', 'webp', 'tiff', 'gif', 'bmp')):
                        input_path = os.path.join(root, file)
                        if self.break_structure:
                            output_dir = self.output_folder
                        else:
                            relative_path = os.path.relpath(root, self.input_folder)
                            output_dir = os.path.join(self.output_folder, relative_path)
                        output_path = os.path.join(output_dir, os.path.splitext(file)[0] + f".{self.output_format}")
                        image_files.append((input_path, output_path))
        else:
            for file in os.listdir(self.input_folder):
                if file.lower().endswith(('jpg', 'jpeg', 'png', 'webp', 'tiff', 'gif', 'bmp')):
                    input_path = os.path.join(self.input_folder, file)
                    output_path = os.path.join(self.output_folder, os.path.splitext(file)[0] + f".{self.output_format}")
                    image_files.append((input_path, output_path))
        return image_files

    def compress_images(self):
        """
        Compresses all images in the input folder and saves them to the output folder while maintaining structure if enabled.
        """
        total_images = len(self.images)
        if total_images == 0:
            print("No images found in the input folder.")
            return
        
        print(f"Found {total_images} images. Starting compression...")
        
        with tqdm(total=total_images, desc="Compressing", unit="image") as pbar:
            for index, (input_path, output_path) in enumerate(self.images):
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self._compress_image(input_path, output_path)
                pbar.update(1)
                tqdm.write(f"Compressed: {index + 1}/{total_images} - Remaining: {total_images - (index + 1)}")
                
        print("Compression complete!")

    def _compress_image(self, input_path, output_path):
        """
        Compresses a single image and saves it to the output folder.
        If compression fails, logs the error and continues with remaining images.
        :param input_path: Path of the image file to compress.
        :param output_path: Destination path where compressed image will be saved.
        """
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
            error_msg = f"Error :: {input_path} :: {os.path.getsize(input_path)} :: {e}"
            tqdm.write(error_msg)
            with open("error_log.txt", "a") as log_file:
                log_file.write(error_msg + "\n")


if __name__ == "__main__":
    """
    Main script execution: Parses command-line arguments using argparse and starts the compression process.
    """
    parser = argparse.ArgumentParser(description="Bulk Image Compressor")
    parser.add_argument("input_folder", type=str, help="Path to the folder containing images to compress")
    parser.add_argument("output_folder", type=str, help="Path where compressed images will be saved")
    parser.add_argument("--quality", type=int, default=80, help="Quality setting for image compression (default: 80)")
    parser.add_argument("--resize", action="store_true", help="Enable resizing of images")
    parser.add_argument("--max_width", type=int, default=1024, help="Maximum width for resized images (default: 1024)")
    parser.add_argument("--output_format", type=str, default='jpeg', choices=['jpeg', 'png', 'webp'], help="Desired output format (default: jpeg)")
    parser.add_argument("--recursive", action="store_true", help="Enable recursive search for images in subdirectories")
    parser.add_argument("--break_structure", action="store_true", help="Break folder structure in output directory")
    
    args = parser.parse_args()
    
    try:
        compressor = ImageCompressor(args.input_folder, args.output_folder, args.quality, args.resize, args.max_width, args.output_format, args.recursive, args.break_structure)
        compressor.compress_images()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

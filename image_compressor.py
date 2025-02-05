import os
import sys
import argparse
import multiprocessing
import psutil
from PIL import Image
from tqdm import tqdm
from multiprocessing import Manager, Queue

def worker_init(q):
    """
    Initializes worker processes with a shared progress queue.
    :param q: Multiprocessing queue to track progress updates.
    """
    global progress_queue
    progress_queue = q

class ImageCompressor:
    """
    A class to compress images in bulk with optional parallel processing.
    Supports maintaining folder structure, resizing, and adaptive worker scaling.
    """

    def __init__(self, input_folder, output_folder, quality=80, resize=False, max_width=1024, output_format='jpeg', recursive=False, break_structure=False, parallel=False):
        """
        Initializes the ImageCompressor with user-specified options.
        
        :param input_folder: Path to the folder containing images to compress.
        :param output_folder: Path where compressed images will be saved.
        :param quality: Quality setting for image compression (default: 80).
        :param resize: Flag to enable/disable resizing (default: False).
        :param max_width: Maximum width for resized images (default: 1024 pixels).
        :param output_format: Desired output image format (default: jpeg). Supports 'jpeg', 'png', 'webp'.
        :param recursive: Whether to search for images in subdirectories.
        :param break_structure: Whether to flatten directory structure in output.
        :param parallel: Enable parallel processing for faster compression.
        """

        # Check if input folder specified is valid
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
        self.parallel = parallel
        self.images = self._get_images()
        
        # Validate output format
        if self.output_format in ['jpg', 'jpeg']:
            self.output_format = 'jpeg'
        elif self.output_format not in ['jpeg', 'png', 'webp']:
            print("Invalid output format. Defaulting to 'jpeg'.")
            self.output_format = 'jpeg'
        
        # Ensure output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
    def _get_images(self):
        """
        Retrieves a list of image files from the input folder.
        :return: List of tuples containing (input_path, output_path).
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
        Compresses all images based on user settings.
        Uses parallel processing if enabled.
        """

        total_images = len(self.images)
        if total_images == 0:
            print("No images found in the input folder.")
            return
        
        print(f"Found {total_images} images. Starting compression...")
        
        if self.parallel:
            self._compress_images_parallel()
        else:
            with tqdm(total=total_images, desc="Compressing", unit="image") as pbar:
                for input_path, output_path in self.images:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    self._compress_image(input_path, output_path)
                    pbar.update(1)
        
        print("Compression complete!")
    
    def _compress_images_parallel(self):
        """
        Compress images in parallel mode using multiple worker processes.
        Dynamically adjusts workers based on system load.
        """

        num_cores = multiprocessing.cpu_count()
        system_load = psutil.cpu_percent()

        print(f"CPU Status :::: CPU Cores: {num_cores} | CPU Load: {system_load}")

        if system_load <= 25:
            num_cores = max(1, (num_cores // 2) + 1)
        elif system_load <= 50:
            num_cores = max(1, num_cores // 2)
        else:
            num_cores = 1
        
        print(f"Using {num_cores} worker processes for parallel compression.")
        
        with Manager() as manager:
            progress_queue = manager.Queue()
            pool = multiprocessing.Pool(processes=num_cores, initializer=worker_init, initargs=(progress_queue,))
            workers = {pool.apply_async(self._compress_image, args=(input_path, output_path, idx)) for idx, (input_path, output_path) in enumerate(self.images)}
            
            with tqdm(total=len(self.images), desc="Total Progress", unit="image") as pbar:
                completed = 0
                while completed < len(self.images):
                    progress_queue.get()
                    completed += 1
                    pbar.update(1)
            pool.close()
            pool.join()
    
    def _compress_image(self, input_path, output_path, worker_id=None):
        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")
                if self.resize and img.width > self.max_width:
                    new_height = int((self.max_width / img.width) * img.height)
                    img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                img.save(output_path, format=self.output_format.upper(), quality=self.quality, optimize=True)
                if worker_id is not None:
                    progress_queue.put(worker_id)
        except Exception as e:
            error_msg = f"Error :: {input_path} :: {e}"
            tqdm.write(error_msg)
            with open("error_log.txt", "a") as log_file:
                log_file.write(error_msg + "\n")

if __name__ == "__main__":
    """
    Main script execution: Parses command-line arguments and starts the compression process.
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
    parser.add_argument("--parallel", action="store_true", help="Enable parallel processing for faster compression")
    
    args = parser.parse_args()
    
    try:
        compressor = ImageCompressor(args.input_folder, args.output_folder, args.quality, args.resize, args.max_width, args.output_format, args.recursive, args.break_structure, args.parallel)
        compressor.compress_images()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

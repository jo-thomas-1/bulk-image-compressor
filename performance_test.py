import unittest
import time
import os
from image_compressor import ImageCompressor

class TestImageCompressorPerformance(unittest.TestCase):
    def setUp(self):
        """ Set up test environment """
        self.test_input = "test_images"
        self.test_output = "compressed_images"
        os.makedirs(self.test_input, exist_ok=True)
        os.makedirs(self.test_output, exist_ok=True)
        self.compressor = ImageCompressor(self.test_input, self.test_output, quality=85, resize=True, max_width=800, output_format='jpg')

        # Create multiple sample images for performance testing
        for i in range(10):
            sample_image_path = os.path.join(self.test_input, f"sample_{i}.jpg")
            with open(sample_image_path, "wb") as f:
                f.write(os.urandom(1024 * 1024))  # Create a 1MB random file to simulate an image

    def test_compression_speed(self):
        """ Measure the time taken to compress multiple images """
        start_time = time.time()
        self.compressor.compress()
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"Compression took {elapsed_time:.2f} seconds for 10 images.")
        self.assertLess(elapsed_time, 10, "Compression is too slow.")

    def tearDown(self):
        """ Clean up after tests """
        for folder in [self.test_input, self.test_output]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)

if __name__ == "__main__":
    unittest.main()

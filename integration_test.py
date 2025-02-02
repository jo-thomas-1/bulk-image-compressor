import unittest
import os
from image_compressor import ImageCompressor

class TestImageCompressorIntegration(unittest.TestCase):
    def setUp(self):
        """ Set up test environment """
        self.test_input = "test_images"
        self.test_output = "compressed_images"
        os.makedirs(self.test_input, exist_ok=True)
        os.makedirs(self.test_output, exist_ok=True)
        self.compressor = ImageCompressor(self.test_input, self.test_output, quality=85, resize=True, max_width=800, output_format='jpg')

    def test_full_compression_process(self):
        """ Test the full image compression pipeline """
        # Place a sample image in the input folder for testing
        sample_image_path = os.path.join(self.test_input, "sample.jpg")
        with open(sample_image_path, "wb") as f:
            f.write(os.urandom(1024 * 1024))  # Create a 1MB random file to simulate an image
        
        # Run compression
        self.compressor._compress_image(self)
        
        # Verify output
        compressed_images = os.listdir(self.test_output)
        self.assertGreater(len(compressed_images), 0, "No images were compressed.")

    def tearDown(self):
        """ Clean up after tests """
        for folder in [self.test_input, self.test_output]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)

if __name__ == "__main__":
    unittest.main()

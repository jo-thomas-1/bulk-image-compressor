import unittest
import os
from image_compressor import ImageCompressor

class TestImageCompressorEdgeCases(unittest.TestCase):
    def setUp(self):
        """ Set up test environment """
        self.test_input = "test_images"
        self.test_output = "compressed_images"
        os.makedirs(self.test_input, exist_ok=True)
        os.makedirs(self.test_output, exist_ok=True)
        self.compressor = ImageCompressor(self.test_input, self.test_output, quality=85, resize=False, max_width=800, output_format='jpg')

    def test_empty_folder(self):
        """ Test compression when input folder is empty """
        self.compressor.compress()
        compressed_images = os.listdir(self.test_output)
        self.assertEqual(len(compressed_images), 0, "Output folder should be empty for an empty input folder.")

    def test_corrupt_image(self):
        """ Test behavior when encountering a corrupt image """
        corrupt_image_path = os.path.join(self.test_input, "corrupt.jpg")
        with open(corrupt_image_path, "wb") as f:
            f.write(b"not_an_image")  # Writing invalid data
        
        self.compressor.compress()
        compressed_images = os.listdir(self.test_output)
        self.assertEqual(len(compressed_images), 0, "Corrupt image should not be processed.")

    def tearDown(self):
        """ Clean up after tests """
        for folder in [self.test_input, self.test_output]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)

if __name__ == "__main__":
    unittest.main()

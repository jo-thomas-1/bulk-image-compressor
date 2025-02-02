import unittest
import os
from image_compressor import ImageCompressor

class TestImageCompressor(unittest.TestCase):
    def setUp(self):
        """ Set up test environment """
        self.test_input = "test_images"
        self.test_output = "compressed_images"
        os.makedirs(self.test_input, exist_ok=True)
        os.makedirs(self.test_output, exist_ok=True)
        self.compressor = ImageCompressor(self.test_input, self.test_output, quality=85, resize=False, max_width=800, output_format='jpg')
    
    def test_initialization(self):
        """ Test if ImageCompressor initializes correctly """
        self.assertEqual(self.compressor.input_folder, self.test_input)
        self.assertEqual(self.compressor.output_folder, self.test_output)
        self.assertEqual(self.compressor.quality, 85)
    
    def test_get_images_empty(self):
        """ Test if _get_images() returns an empty list when no images exist """
        images = self.compressor._get_images()
        self.assertEqual(len(images), 0)
    
    def tearDown(self):
        """ Clean up after tests """
        os.rmdir(self.test_input)
        os.rmdir(self.test_output)

if __name__ == "__main__":
    unittest.main()

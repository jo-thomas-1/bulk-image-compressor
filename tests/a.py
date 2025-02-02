from image_compressor import ImageCompressor

def test_image_compressor():
    try:
        compressor = ImageCompressor(input_folder="input", output_folder="output")
        print("ImageCompressor initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize ImageCompressor: {e}")

if __name__ == "__main__":
    test_image_compressor()

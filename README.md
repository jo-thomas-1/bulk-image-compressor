# Bic - Bulk Image Compressor

## Overview

**Bic** is a high-performance Python-based tool for compressing large batches of images efficiently. It supports parallel processing, maintains EXIF metadata, and offers multiple optimization features to balance speed and quality.

---

## Features

✅ **Batch Compression:** Process entire folders of images at once.  
✅ **Parallel Processing:** Automatically optimizes CPU usage for faster compression.  
✅ **EXIF Data Preservation:** Ensures image metadata (orientation, etc.) is retained.  
✅ **Lossy & Lossless Compression:** Supports JPEG, PNG, and WebP formats.  
✅ **Resizing Support:** Optionally resize images while compressing.  
✅ **Recursive Processing:** Scan subdirectories for images.  
✅ **Flexible Output Structure:** Maintain or flatten folder structures.  
✅ **Error Handling & Logging:** Logs failed operations for debugging.  

---

## Installation

Ensure you have **Python 3.7+** installed. Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the script with the required arguments:

```bash
python image_compressor.py <input_folder> <output_folder> [options]
```

### Arguments

| Argument       | Description |
|---------------|-------------|
| `input_folder` | Path to the folder containing images to compress. |
| `output_folder` | Destination folder for compressed images. |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--quality` | 80 | Set compression quality (0-100). |
| `--resize` | False | Enable resizing of images. |
| `--max_width` | 1024 | Max width when resizing images. |
| `--output_format` | jpeg | Choose output format (`jpeg`, `png`, `webp`). |
| `--recursive` | False | Scan subdirectories for images. |
| `--collapse` | False | Flatten directory structure in output. |
| `--parallel` | False | Enable parallel processing. |

### Example Commands

#### Basic Compression
```bash
python image_compressor.py input_folder output_folder
```

#### Compress with Resizing
```bash
python image_compressor.py input_folder output_folder --resize --max_width 800
```

#### Parallel Processing for Speed
```bash
python image_compressor.py input_folder output_folder --parallel
```

#### Scan and Preserve Folder Structure
```bash
python image_compressor.py input_folder output_folder --recursive
```

#### Scan and Flatten Output Folder
```bash
python image_compressor.py input_folder output_folder --recursive --collapse
```

---

## Parallel Processing

Parallel processing improves speed by distributing workload across CPU cores. The tool:
- Automatically detects available cores.
- Adjusts worker count based on system load.
- Uses a progress bar (`tqdm`) to track compression progress.

---

## EXIF Metadata Handling

EXIF metadata (including orientation) is preserved for JPEG images. This ensures images maintain their original rotation when viewed in applications.

---

## Error Handling

- Errors are logged in `error_log.txt`.
- Any failed images are skipped to avoid crashes.

---

## Future Enhancements

- Implement GPU acceleration for faster processing.
- Improve adaptive load balancing for parallel execution.

---

## License

This project is open-source under the **MIT License**. Feel free to contribute!

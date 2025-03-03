# Vorix AIO - The All I One File Converter

Vorix AIO is a powerful, locally running file converter that supports **image, video, audio, document, and OCR-based conversions**. It enables users to seamlessly convert files without relying on online tools, ensuring privacy and speed.

## Features

- **Image Conversion**: Convert between PNG, JPG, WEBP, and GIF.
- **Audio Conversion**: Convert MP3, WAV, AAC, and FLAC files.
- **Video Conversion**: Convert MP4, AVI, MKV, and MOV files.
- **Document Conversion**: Convert PDFs to DOCX, ODT, and TXT.
- **OCR-based PDF Creation**: Extract text from images (PNG, JPG) and compile them into a searchable PDF.
- **Drag & Drop Support**: Easily select files or drag and drop them into the UI.

## Installation Guide

### Step 1: Download Vorix AIO

1. Download the latest release from **[GitHub Releases](https://github.com/spydude2w1/Vorix/releases/tag/Vorix)**.
2. Extract the downloaded ZIP file.

### Step 2: Install Dependencies

Before running Vorix AIO, install the required Python packages:

```sh
pip install -r requirements.txt
```

### Step 3: Download and Set Up FFmpeg

Vorix AIO requires **FFmpeg** for audio/video conversion.

1. Download FFmpeg from: **[FFmpeg Official Site](https://ffmpeg.org/download.html)**.
2. Extract the folder and \*\*rename it to \*\*\`\`.
3. Move the **entire **********\`\`********** folder** into the same directory as `vorix.exe` or `main.py`.

### Step 4: Run Vorix AIO

Once everything is set up, you can run the application:

```sh
python main.py
```

Or, if using the compiled version, simply double-click `vorix.exe`.

## Usage Instructions

1. Open Vorix AIO.
2. Drag & Drop or select a file.
3. Choose the desired output format.
4. Click **Convert** and wait for the process to complete.
5. The converted file will be saved in the same directory as the original file.

## Notes

- Ensure FFmpeg is correctly placed in the **Vorix AIO directory** before converting audio or video files.
- OCR-based conversion requires **Tesseract OCR**, which is already bundled with Vorix AIO.

## License

Vorix AIO is an open-source project. Feel free to contribute and improve it!

---

For issues or feature requests, visit **[GitHub Issues](https://github.com/spydude2w1/Vorix/releases/tag/Vorix)**.


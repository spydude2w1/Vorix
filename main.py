import flet as ft
import os
import pytesseract
from PIL import Image
from pathlib import Path
import pdf2image
from docx import Document
from fpdf import FPDF

def main(page: ft.Page):
    page.title = "Vorix File Converter"
    page.window_width = 800  # Set window width
    page.window_height = 600  # Set window height
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    # Set Tesseract path (assuming it's bundled with the app)
    tesseract_path = os.path.join(os.getcwd(), "tesseract", "tesseract.exe")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    selected_files = []  # Store selected file paths
    selected_format = None
    use_ocr = False  # Toggle for OCR vs Regular Conversion
    selected_ocr_language = "eng"

    ocr_languages = {
        "English": "eng",
        "Hindi": "hin",
        "Oriya": "ori",
        "Malayalam": "mal",
        "Kannada": "kan",
        "Tamil": "tam",
        "Telugu": "tel",
        "Bengali": "ben",
        "Gujarati": "guj"
    }

    format_options = {
        "Audio": ["MP3", "WAV", "AAC", "FLAC", "OGG", "M4A"],
        "Video": ["MP4", "AVI", "MKV", "MOV", "WMV", "FLV"],
        "Image": ["PNG", "JPG", "WEBP", "GIF", "BMP", "TIFF"],
        "Document": ["DOCX", "ODT", "TXT", "PDF", "RTF", "HTML"],
    }

    def set_ocr_language(e):
        nonlocal selected_ocr_language
        selected_ocr_language = ocr_languages[e.control.value]
        page.update()

    def detect_file_type(file):
        ext = Path(file).suffix.lower()
        if ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff"]:
            return "Image"
        elif ext in [".pdf"]:
            return "Document"
        elif ext in [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"]:
            return "Audio"
        elif ext in [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"]:
            return "Video"
        return None

    def update_selected_files():
        if selected_files:
            file_type_detected = detect_file_type(selected_files[0])
            if file_type_detected:
                format_buttons.controls = [
                    ft.ElevatedButton(fmt, on_click=lambda e, f=fmt: set_format(f))
                    for fmt in format_options[file_type_detected]
                ]
                selected_format_text.value = "Select Format"
            else:
                selected_format_text.value = "Unsupported File Type"
                format_buttons.controls = []
            status_circle.bgcolor = "#77dd77"  # Green when a file is selected
            selected_files_text.controls[1].value = os.path.basename(selected_files[0])
        else:
            status_circle.bgcolor = "#ff6961"  # Red when no file is selected
            selected_files_text.controls[1].value = "No Files Selected"
        page.update()

    def toggle_ocr(e):
        nonlocal use_ocr
        use_ocr = e.control.value
        update_selected_files()

    def set_format(fmt):
        nonlocal selected_format
        selected_format = fmt
        selected_format_text.value = f"Selected Format: {fmt}"
        page.update()

    def convert_pdf_to_text(pdf_path):
        poppler_path = os.path.join(os.getcwd(), "poppler", "Library", "bin")
        images = pdf2image.convert_from_path(pdf_path, poppler_path=poppler_path)
        text = "\n".join([pytesseract.image_to_string(img, lang=selected_ocr_language) for img in images])
        return text

    def save_text_as_docx(text, output_path):
        doc = Document()
        doc.add_paragraph(text)
        doc.save(output_path)

    def convert_images_to_pdf(image_paths, output_path):
        pdf = FPDF()
        for image_path in image_paths:
            pdf.add_page()
            pdf.image(image_path, x=10, y=10, w=pdf.w - 20)
        pdf.output(output_path)

    def convert_images_to_text(image_paths):
        text = ""
        for image_path in image_paths:
            text += pytesseract.image_to_string(Image.open(image_path), lang=selected_ocr_language) + "\n"
        return text

    def convert_images(image_paths, output_format):
        for image_path in image_paths:
            img = Image.open(image_path)
            output_file = os.path.splitext(image_path)[0] + f".{output_format.lower()}"
            img.save(output_file)
            update_log(f"Converted: {image_path} -> {output_file}")

    import subprocess

    ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")

    def convert_documents(e):
        if not selected_files or not selected_format:
            update_log("No files selected or format not chosen!")
            return
        
        progress_bar.visible = True
        page.update()
        
        for file in selected_files:
            try:
                file_type = detect_file_type(file)
                if file_type == "Audio" or file_type == "Video":
                    output_ext = selected_format.lower()
                    output_file = os.path.splitext(file)[0] + f".{output_ext}"
                    subprocess.run([ffmpeg_path, "-i", file, output_file])
                    update_log(f"Converted: {file} -> {output_file}")
                elif file_type == "Image" and selected_format == "PDF":
                    output_file = os.path.splitext(file)[0] + ".pdf"
                    convert_images_to_pdf([file], output_file)
                    update_log(f"Converted: {file} -> {output_file}")
                elif file_type == "Image":
                    convert_images([file], selected_format)
                elif file_type == "Image" and use_ocr:
                    text = convert_images_to_text([file])
                    output_file = os.path.splitext(file)[0] + ".docx"
                    save_text_as_docx(text, output_file)
                    update_log(f"Converted: {file} -> {output_file}")
                elif use_ocr:
                    text = convert_pdf_to_text(file)
                else:
                    with open(file, "r", encoding="utf-8") as f:
                        text = f.read()
                
                if file_type == "Document":
                    output_ext = selected_format.lower()
                    output_file = os.path.splitext(file)[0] + f".{output_ext}"
                    
                    if selected_format == "DOCX":
                        save_text_as_docx(text, output_file)
                    else:
                        with open(output_file, "w", encoding="utf-8") as f:
                            f.write(text)
                    
                    update_log(f"Converted: {file} -> {output_file}")
            except Exception as ex:
                update_log(f"Error converting {file}: {ex}")
        
        progress_bar.visible = False
        page.update()

    def update_log(message):
        conversion_log.content.value += f"\n{message}"
        page.update()

    def pick_files(e):
        file_picker.pick_files(allow_multiple=True)

    file_picker = ft.FilePicker(on_result=lambda e: (selected_files.clear(), selected_files.extend([f.path for f in e.files]) if e.files else None, update_selected_files()))

    status_circle = ft.Container(width=12, height=12, bgcolor="#ff6961", border_radius=50)
    selected_files_text = ft.Row([
        status_circle,
        ft.Text("No Files Selected", size=14, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    ocr_toggle_button = ft.Switch(label="Enable OCR", on_change=toggle_ocr)
    ocr_language_dropdown = ft.Dropdown(
        label="Select OCR Language",
        options=[ft.DropdownOption(lang) for lang in ocr_languages.keys()],
        on_change=set_ocr_language,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    format_buttons = ft.Row(
        controls=[], alignment=ft.MainAxisAlignment.CENTER, spacing=10
    )
    selected_format_text = ft.Text("Select a File First", size=14, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER)

    progress_bar = ft.ProgressBar(width=500, visible=False, bgcolor=ft.Colors.GREY_800)
    conversion_log = ft.Container(
        content=ft.Text("Conversion Log:", size=14, color=ft.Colors.WHITE70, text_align=ft.TextAlign.CENTER),
        width=500,
        expand=True,
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
        padding=10,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    convert_button = ft.ElevatedButton(
        "Convert", 
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(15, 10, 15, 10)
        ),
        on_click=convert_documents,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    pick_files_button = ft.ElevatedButton(
        "Select Files",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=ft.Padding(15, 10, 15, 10)
        ),
        on_click=pick_files,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    def show_menu(menu):
        for m in menus:
            m.visible = False
        menu.visible = True
        page.update()

    audio_menu = ft.Column(
        controls=[
            ft.Text("Vorix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.Text("Audio Conversion", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            selected_files_text,
            format_buttons,
            selected_format_text,
            ft.Row(
                controls=[pick_files_button, convert_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        visible=False,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    video_menu = ft.Column(
        controls=[
            ft.Text("Vorix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.Text("Video Conversion", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            selected_files_text,
            format_buttons,
            selected_format_text,
            ft.Row(
                controls=[pick_files_button, convert_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        visible=False,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    image_menu = ft.Column(
        controls=[
            ft.Text("Vorix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.Text("Image Conversion", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            selected_files_text,
            format_buttons,
            selected_format_text,
            ft.Row(
                controls=[pick_files_button, convert_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        visible=False,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    document_menu = ft.Column(
        controls=[
            ft.Text("Vorix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.Text("Document Conversion", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            selected_files_text,
            ocr_toggle_button,
            ocr_language_dropdown,
            format_buttons,
            selected_format_text,
            ft.Row(
                controls=[pick_files_button, convert_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        visible=False,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    handwriting_menu = ft.Column(
        controls=[
            ft.Text("Vorix", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.Text("Handwriting Recognition", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            selected_files_text,
            ocr_toggle_button,
            ocr_language_dropdown,
            format_buttons,
            selected_format_text,
            ft.Row(
                controls=[pick_files_button, convert_button],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        visible=False,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    menus = [audio_menu, video_menu, image_menu, document_menu, handwriting_menu]

    sidebar = ft.Column(
        controls=[
            ft.ElevatedButton("Audio", on_click=lambda e: show_menu(audio_menu)),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.ElevatedButton("Video", on_click=lambda e: show_menu(video_menu)),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.ElevatedButton("Image", on_click=lambda e: show_menu(image_menu)),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.ElevatedButton("Document", on_click=lambda e: show_menu(document_menu)),
            ft.Divider(height=1, color=ft.Colors.GREY_700),
            ft.ElevatedButton("Handwriting", on_click=lambda e: show_menu(handwriting_menu))
        ],
        spacing=10,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        animate_scale=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT)
    )

    page.overlay.append(file_picker)

    page.add(
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(),
                ft.Stack(
                    controls=menus,
                    expand=True
                ),
                ft.VerticalDivider(),
                ft.Column(
                    controls=[
                        conversion_log,
                        progress_bar
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True
                )
            ],
            expand=True
        )
    )

    show_menu(audio_menu)  # Automatically load into the first menu

ft.app(target=main)

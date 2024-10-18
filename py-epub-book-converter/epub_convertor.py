import ebooklib
import streamlit as st
from ebooklib import epub
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from io import BytesIO
from bs4 import BeautifulSoup
import textwrap
import os
from docx import Document  # Import for Word document generation

# Helper function to convert epub to HTML
def epub_to_html(epub_file_path):
    book = epub.read_epub(epub_file_path)
    html_content = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_body_content().decode('utf-8')
        html_content.append(content)
    return "\n".join(html_content)

# Helper function to extract and clean text from epub
def epub_to_clean_text(epub_file_path):
    book = epub.read_epub(epub_file_path)
    text = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_body_content().decode('utf-8')
        # Use BeautifulSoup to clean the content and extract text
        soup = BeautifulSoup(content, 'lxml')
        text.append(soup.get_text())  # Extract text without HTML tags
    return "\n".join(text)

# Helper function to convert text to a styled PDF with text wrapping and Unicode support
def text_to_styled_pdf(text):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSerif.ttf'))  # Register Unicode font

    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = inch  # 1-inch margins
    max_width = width - 2 * margin
    y = height - margin

    p.setFont('DejaVu', 12)  # Use Unicode font

    # Split text into paragraphs
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        lines = textwrap.wrap(paragraph, width=85)  # Wrap text to fit within page width
        for line in lines:
            if y < margin + 20:  # New page if text goes off the current page
                p.showPage()
                p.setFont('DejaVu', 12)
                y = height - margin
            p.drawString(margin, y, line)
            y -= 15
        y -= 15  # Add space between paragraphs

    p.save()
    buffer.seek(0)
    return buffer

# Helper function to convert text to a Word document (.docx)
def text_to_word_doc(text):
    doc = Document()
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        if paragraph.strip():  # Only add non-empty paragraphs
            doc.add_paragraph(paragraph.strip())
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Sidebar options for conversion
st.sidebar.title("EPUB Converter")
conversion_type = st.sidebar.selectbox(
    "Choose conversion type", 
    ["EPUB to HTML", "EPUB to Human-readable Text", "EPUB to Styled PDF (Book)", "EPUB to Word (.docx)"]
)

# File uploader for EPUB file
uploaded_file = st.file_uploader("Choose an EPUB file", type="epub")

if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Save the uploaded file temporarily
    with open("temp.epub", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Option 1: EPUB to HTML
    if conversion_type == "EPUB to HTML":
        if st.button("Convert to HTML"):
            st.info("Converting EPUB to HTML...")
            html_content = epub_to_html("temp.epub")
            st.text_area("Converted HTML", html_content, height=400)
            st.download_button(label="Download HTML", data=html_content, file_name="book.html", mime="text/html")

    # Option 2: EPUB to Human-readable Text
    elif conversion_type == "EPUB to Human-readable Text":
        if st.button("Convert to Text"):
            st.info("Converting EPUB to human-readable Text...")
            text = epub_to_clean_text("temp.epub")
            st.text_area("Converted Text", text, height=400)
            st.download_button(label="Download Text", data=text, file_name="book_text.txt", mime="text/plain")

    # Option 3: EPUB to Styled PDF (Book-like)
    elif conversion_type == "EPUB to Styled PDF (Book)":
        if st.button("Convert to PDF"):
            st.info("Converting EPUB to Styled PDF (Book-like)...")
            text = epub_to_clean_text("temp.epub")
            pdf_buffer = text_to_styled_pdf(text)
            st.download_button(label="Download PDF", data=pdf_buffer, file_name="book.pdf", mime="application/pdf")

    # Option 4: EPUB to Word (.docx)
    elif conversion_type == "EPUB to Word (.docx)":
        if st.button("Convert to Word"):
            st.info("Converting EPUB to Word (.docx)...")
            text = epub_to_clean_text("temp.epub")
            word_buffer = text_to_word_doc(text)
            st.download_button(label="Download Word", data=word_buffer, file_name="book.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # Cleanup the temporary file after use
    os.remove("temp.epub")

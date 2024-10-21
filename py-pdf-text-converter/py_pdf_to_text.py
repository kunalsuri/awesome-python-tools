import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from pdfminer.high_level import extract_text as extract_text_pdfminer
from PIL import Image
import re
import os

# OCR Setup: Ensure Tesseract is installed (Update the path if needed)
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/bin/tesseract'

# Modularized function for displaying method descriptions
def display_method_description(method):
    descriptions = {
        "PyMuPDF": "PyMuPDF is a fast, lightweight PDF manipulation library that can extract text from PDFs with embedded text data.",
        "pdfminer.six": "pdfminer.six is a library for extracting and analyzing text from PDFs. It works well for extracting text from PDFs that use complex encodings.",
        "Tesseract OCR": "Tesseract OCR uses Optical Character Recognition (OCR) to extract text from scanned PDFs or images within PDFs."
    }
    st.write(descriptions.get(method, "No description available for this method."))

# Function to use PyMuPDF for text extraction
def extract_text_pymupdf(pdf_file):
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
        return text
    except Exception as e:
        st.error(f"Error extracting text using PyMuPDF: {str(e)}")
        return None

# Function to use pdfminer.six for text extraction
def extract_text_pdfminer_six(pdf_file):
    try:
        return extract_text_pdfminer(pdf_file)
    except Exception as e:
        st.error(f"Error extracting text using pdfminer.six: {str(e)}")
        return None

# Function to use Tesseract OCR for scanned PDFs
def extract_text_tesseract(pdf_file):
    try:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.read())

        # Convert PDF pages to images and apply OCR
        images = convert_from_path("temp.pdf")
        extracted_text = []
        for image in images:
            text = pytesseract.image_to_string(image)
            extracted_text.append(text)

        # Clean up the temporary file
        os.remove("temp.pdf")
        return "\n".join(extracted_text)
    except Exception as e:
        st.error(f"Error extracting text using Tesseract OCR: {str(e)}")
        if os.path.exists("temp.pdf"):
            os.remove("temp.pdf")
        return None

# Function to verify extracted text for issues
def verify_text(text):
    issues = []
    # Check for irregular whitespace
    if re.search(r'\s{4,}', text):
        issues.append("Irregular whitespace found.")
    
    # Check for broken lines
    if re.search(r'\S\n\S', text):
        issues.append("Broken lines detected.")
    
    # Check for empty lines or missing newlines
    if not re.search(r'\n', text):
        issues.append("Missing newlines.")
    
    return issues

# Sidebar setup for additional functionality
def app_sidebar():
    ### App Sidebar Section Starts ###
    st.sidebar.title('✅ Settings ⚙️')

    # Sidebar for choosing the method
    st.sidebar.header("Select Functionality")
    method = st.sidebar.radio(
        "Choose the extraction method:",
        ["PyMuPDF", "pdfminer.six", "Tesseract OCR"]
    )

    # Additional Sidebar options
    st.sidebar.markdown("---")
    st.sidebar.markdown('📖 Open-source code and ReadMe available app via this [Github Repo](https://github.com/kunalsuri/)!')

    return method

# Main App Layout with Sidebar
def main():
    st.title("📄 PDF to Text Converter with Verification")

    # App sidebar
    method = app_sidebar()

    # Display method description in the main area
    st.subheader(f"Selected Functionality: {method}")
    display_method_description(method)

    # Upload PDF file
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Extract and display/save the text
    if pdf_file and st.button("Extract Text"):
        st.info("Extracting text, please wait...")
        extracted_text = ""
        progress = st.progress(0)

        if method == "PyMuPDF":
            st.write("Using PyMuPDF for extraction...")
            extracted_text = extract_text_pymupdf(pdf_file)
        elif method == "pdfminer.six":
            st.write("Using pdfminer.six for extraction...")
            extracted_text = extract_text_pdfminer_six(pdf_file)
        elif method == "Tesseract OCR":
            st.write("Using Tesseract OCR for extraction...")
            extracted_text = extract_text_tesseract(pdf_file)

        # Update progress bar
        progress.progress(100)

        # Display extracted text
        if extracted_text:
            st.success("Text extraction successful!")
            st.text_area("Extracted Text", extracted_text, height=300)

            # Provide an option to download the extracted text
            st.download_button(
                label="Download as Text File",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain",
            )

            # Add a verification step
            if st.button("Verify Extracted Text"):
                issues = verify_text(extracted_text)
                if issues:
                    st.warning("Issues found in the extracted text:")
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.success("No issues found in the extracted text!")
        else:
            st.error("No text extracted. Please check your file or method.")

# Entry point of the app
if __name__ == "__main__":
    main()

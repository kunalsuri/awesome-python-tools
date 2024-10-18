import os
import streamlit as st
from PyPDF2 import PdfReader
import pdfplumber

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error reading {pdf_path}: {e}")
    return text

# Save text to a .txt file
def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

# Combine text files in the folder into one file
def combine_text_files(folder_path, output_file):
    combined_text = ""
    for file in os.listdir(folder_path):
        if file.endswith('.txt'):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n"
    
    save_text_to_file(combined_text, output_file)
    return combined_text

# Streamlit App
st.sidebar.title("PDF to Text and Merging App")

# Sidebar tabs
tab_selection = st.sidebar.radio("Choose an action", ("PDF to Text Conversion", "Merge Text Files"))

if tab_selection == "PDF to Text Conversion":
    st.title('PDF to Text Converter')

    # Step 1: Upload PDFs
    st.header('Upload PDFs')
    uploaded_files = st.file_uploader("Upload multiple PDF files", type=['pdf'], accept_multiple_files=True)

    # Specify output folder for text files
    output_folder = st.text_input("Specify the folder where text files will be saved", "output_texts")

    # Convert PDFs to text files
    if uploaded_files and st.button("Convert PDFs to Text"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for uploaded_file in uploaded_files:
            # Extract the text from the PDF
            pdf_name = uploaded_file.name
            text = extract_text_from_pdf(uploaded_file)
            
            # Save the extracted text to a .txt file with the same name as the PDF
            output_file = os.path.join(output_folder, pdf_name.replace(".pdf", ".txt"))
            save_text_to_file(text, output_file)
            st.success(f"Text file created: {output_file}")
        
        st.write("Conversion Complete!")

elif tab_selection == "Merge Text Files":
    st.title('Merge Text Files')

    # Step 2: Specify the folder containing text files to merge
    st.header('Merge Text Files into One')

    # Input folder containing text files
    text_folder = st.text_input("Specify the folder where text files are located", "output_texts")

    # Specify output folder for merged text file
    merge_output_folder = st.text_input("Specify the folder where the merged file will be saved", "output_texts")
    
    if st.button("Merge All Text Files"):
        if os.path.exists(text_folder):
            if not os.path.exists(merge_output_folder):
                os.makedirs(merge_output_folder)

            # Merging text files
            merge_output_file = os.path.join(merge_output_folder, "merged_file.txt")
            combined_text = combine_text_files(text_folder, merge_output_file)

            st.success(f"All text files have been merged into: {merge_output_file}")
            st.text_area("Merged Text Content (Preview)", combined_text[:2000])  # Preview first 2000 characters
        else:
            st.warning(f"The folder '{text_folder}' does not exist. Please provide a valid folder.")

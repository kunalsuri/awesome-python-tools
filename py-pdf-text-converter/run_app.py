import os
import subprocess

# Run Streamlit script using subprocess
def run_streamlit():
    streamlit_file = "Projects/python-tools-collection/py-pdf-text-converter/py_pdf_to_text.py"
    subprocess.Popen(["streamlit", "run", streamlit_file])

if __name__ == "__main__":
    run_streamlit()
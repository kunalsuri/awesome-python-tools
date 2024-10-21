import os
import subprocess
import streamlit as st

# Function to clear Streamlit cache
def clear_streamlit_cache():
    # Clear the cache programmatically using Streamlit's internal API
    st.cache_data.clear()  # Clear data cache
    st.cache_resource.clear()  # Clear resource cache
    print("Streamlit cache cleared.")

# Function to run Streamlit script
def run_streamlit():
    # Specify the path to your Streamlit script
    streamlit_file = "Projects/python-tools-collection/py-ebook-finder/online_ebook_finder_02.py"
    
    # Run the command to execute the Streamlit app
    subprocess.Popen(["streamlit", "run", streamlit_file])
    print(f"Running Streamlit app: {streamlit_file}")

if __name__ == "__main__":
    # Clear the cache first
    clear_streamlit_cache()

    # Run the Streamlit app
    run_streamlit()

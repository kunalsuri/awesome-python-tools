import os
import time
import streamlit as st
from def_merge_files import merge_files_recursive, merge_text_files, merge_xml_files


# To display a short message known as a notification "toast".
def download_toast():
    msg = st.toast('Going to the Folder...')
    time.sleep(1)
    msg.toast('Checking the Files...')
    time.sleep(1)
    msg.toast('Merging in Progress!', icon = "🥞")

# Sidebar
def app_sidebar():
    ### App Sidebar Section Starts ###
    
    st.sidebar.title('Choose ✅ Task ⚙️')

    menu_selection = st.sidebar.radio("Select Option:", ["Merge Text Files within a Single Folder", 
                                                         "Merge XML Files within a Single Folder", 
                                                         "Merge Text Files from Nested Folder"])

    # Execute function based on user selection
    if menu_selection == "Merge Text Files within a Single Folder":
        execute_merge_text_files()
    elif menu_selection == "Merge XML Files within a Single Folder":    
        execute_merge_xml_files()
    elif menu_selection == "Merge Text Files from Nested Folder":
        execute_merge_text_files_recursively()


    st.sidebar.markdown("---")
    st.sidebar.markdown('📖 Opensource Code and ReadMe available app via this [Github Repo](https://github.com/kunalsuri/)!')
### App Sidebar Section Ends ###


# Function to load default metadata from a file
def load_default_metadata(file_path="custom-metadata.txt"):
    """
    Load default metadata from the custom_metadata.txt file.
    If the file doesn't exist, use a fallback default metadata.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full path by joining the script directory and the relative file path
    full_path = os.path.join(script_dir, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'r') as file:
            return file.read()
    else:
        # Fallback default metadata if the file is not found
        return """
        # Custom metadata
        # Author: Your Name
        # Organization: Your Org
        """


# Load default metadata from the file or fallback if the file is not found
default_metadata = load_default_metadata()


def execute_merge_text_files():
    st.title("Merge Text Files within a Single Folder")

    # Input for selecting the input folder (where files to be merged are located)
    input_folder = st.text_input("Enter the Input Folder Location")

    # Input for selecting the output folder (where the merged file will be stored)
    output_folder = st.text_input("Enter the output Folder Location")

    # Input for the output file name
    output_file_name = st.text_input("Enter the Name for the Merged File", "Merged_XYZ.txt")

    # Custom metadata input with the default metadata loaded from the file
    custom_metadata = st.text_area("Space for adding Custom Metadata Text", default_metadata)

    # Button to trigger file merging
    if st.button("Merge Text Files"):
        if os.path.exists(input_folder) and os.path.exists(output_folder):
            output_file_path = os.path.join(output_folder, output_file_name)
            merge_text_files(input_folder, output_file_path, custom_metadata)
            st.success(f"Files merged successfully into {output_file_path}")
            st.balloons() #Show Balloons as success story
        else:
            st.error("Please ensure both input and output folder paths are correct.")


def execute_merge_xml_files():
    st.title("Merge XML Files within a Single Folder")

    # Input for selecting the input folder (where files to be merged are located)
    input_folder = st.text_input("Enter the Input Folder Location")

    # Input for selecting the output folder (where the merged file will be stored)
    output_folder = st.text_input("Enter the output Folder Location")

    # Input for the output file name
    output_file_name = st.text_input("Enter the Name for the Merged File", "Merged_XYZ.xml")

    # Custom metadata input with the default metadata loaded from the file
    custom_metadata = st.text_area("Space for adding Custom Metadata Text", default_metadata)

    # Button to trigger file merging
    if st.button("Merge XML Files"):
        if os.path.exists(input_folder) and os.path.exists(output_folder):
            output_file_path = os.path.join(output_folder, output_file_name)
            merge_xml_files(input_folder, output_file_path, custom_metadata)
            st.success(f"Files merged successfully into {output_file_path}")
        else:
            st.error("Please ensure both input and output folder paths are correct.")


def execute_merge_text_files_recursively():
    st.title("Merge Text Files from Nested Folders")

    # Input for selecting the input folder (where files to be merged are located)
    input_folder = st.text_input("Enter the Top Level Folder Location")

    # Input for selecting the output folder (where the merged file will be stored)
    output_folder = st.text_input("Enter the output Folder Location")

    # Input for the output file name
    output_file_name = st.text_input("Enter the Name for the Merged File", "Merged_XYZ.txt")

    # Custom metadata input with the default metadata loaded from the file
    custom_metadata = st.text_area("Custom Metadata", default_metadata)

    # Button to trigger file merging
    if st.button("Merge Files"):
        if os.path.exists(input_folder) and os.path.exists(output_folder):
            output_file_path = os.path.join(output_folder, output_file_name)
            merge_files_recursive(input_folder, output_file_path, custom_metadata)
            st.success(f"Files merged successfully into {output_file_path}")
        else:
            st.error("Please ensure both input and output folder paths are correct.")



# Streamlit UI
def main():
    # Centering the title, adding emoji, and adding vertical space
    st.markdown("<h1 style='text-align: center;'>📂 Merge File with MetaData Info 📑</h1>", unsafe_allow_html=True)
    
    # Adding vertical space
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Call the app_sidebar function (if needed)
    app_sidebar()


# Execute the main function
if __name__ == "__main__":
    main()
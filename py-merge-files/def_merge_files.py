import os
from datetime import datetime

def generate_text_metadata(file_name, file_path, custom_metadata=""):
    """
    Generates metadata for a given file.
    """
    file_stats = os.stat(file_path)
    metadata = f"""
{custom_metadata}
## Data Block Starts
## Metadata Start
## Source Name: {file_name}
## Retrieved Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Metadata End

# Data
    """
    return metadata

def merge_text_files(folder, output_file, custom_metadata):
    """
    Merges all files in the selected folder into the output file with metadata.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:  # Ensure UTF-8 encoding
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    # Write metadata
                    outfile.write(generate_text_metadata(file_name, file_path, custom_metadata))
                    outfile.write("\n")
                    # Write file content
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as infile:  # Handle BOM and encoding issues
                        outfile.write(infile.read())
                        outfile.write("\n\n### Data Block Ends ###\n")  # Mark the end of each file
        print(f"Files merged successfully into {output_file}")
    except Exception as e:
        print(f"Error while merging files: {e}")



def generate_xml_metadata(file_name, file_path, custom_metadata=""):
    """
    Generates metadata for a given file.
    """
    file_stats = os.stat(file_path)
    metadata = f"""
{custom_metadata}
<!-- 
## XML Data for file: {file_name}
## Retrieved Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-->

<!-- ## Beginning of XML Data ## -->
    """
    return metadata


def merge_xml_files(folder, output_file, custom_metadata):
    """
    Merges all files in the selected folder into the output file with metadata.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:  # Ensure UTF-8 encoding
            for file_name in os.listdir(folder):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    # Write metadata
                    outfile.write(generate_xml_metadata(file_name, file_path, custom_metadata))
                    outfile.write("\n")
                    # Write file content
                    with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as infile:  # Handle BOM and encoding issues
                        outfile.write(infile.read())
                        outfile.write("\n\n<!-- ## End of XML Data ## -->\n")  # Mark the end of each file
        print(f"Files merged successfully into {output_file}")
    except Exception as e:
        print(f"Error while merging files: {e}")


def merge_files_recursive(input_folder, output_file, default_metadata):
    """
    Merges all files in the input folder and its subdirectories into the output file with metadata.
    """
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(input_folder):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    # Write metadata
                    outfile.write(f"\n### START OF EXAMPLE | Diagram Name (or Short Description): {file_name} ### \n")
                    # outfile.write(f"\n####% Metadata Start\n")
                    # outfile.write(f"{default_metadata}")
                    # outfile.write(f"\n\n## Example Name: {file_name} ##\n")
                    # outfile.write(f"####% Metadata End\n\n")
                    outfile.write(f"\n## START OF CODE FOR EXAMPLE | Diagram Name: {file_name} ##\n\n")

                    # Write file content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(infile.read())
                        outfile.write(f"\n\n## END OF CODE ##")
                        outfile.write("\n\n### END OF EXAMPLE ### \n")
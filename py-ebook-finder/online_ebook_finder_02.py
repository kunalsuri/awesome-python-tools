import streamlit as st
from bs4 import BeautifulSoup
import requests
from streamlit_tree_select import tree_select

# Programmatically clear Streamlit cache
st.cache_data.clear()

# Function to get subjects and books from the website
def get_books_by_subject(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Assuming the structure of the webpage: Modify this according to the actual structure of the page
    subjects_section = soup.find_all('div', class_='subject')  # Example placeholder

    # Parse the subjects and their books
    books_data = {}
    
    for subject in subjects_section:
        subject_name = subject.find('h2').text  # Modify based on actual tags used
        books = subject.find_all('a')  # Assuming books are listed as links
        
        books_data[subject_name] = []
        for book in books:
            books_data[subject_name].append(book.text.strip())
    
    return books_data

# Convert the books data to a format suitable for the tree structure
def prepare_tree_data(books_by_subject):
    tree_data = []
    for subject, books in books_by_subject.items():
        subject_node = {"label": subject, "children": [{"label": book} for book in books]}
        tree_data.append(subject_node)
    return tree_data

# Main Streamlit app
def main():
    st.title("Books by Subject")

    url = "https://www.epubbooks.com/subjects"
    books_by_subject = get_books_by_subject(url)
    
    # Prepare the data in tree structure
    tree_data = prepare_tree_data(books_by_subject)
    
    # Display the tree view
    selected = tree_select(tree_data, multiple=True)
    if selected:
        st.write("You selected:", selected)

if __name__ == '__main__':
    main()

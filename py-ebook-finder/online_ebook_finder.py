import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Function to scrape downloadable eBooks from Goodreads
def scrape_goodreads_ebooks(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    # Send a request to the Goodreads eBooks page
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        st.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return pd.DataFrame()  # Return empty DataFrame in case of error
    
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Lists to hold extracted data
    titles = []
    genres = []
    download_links = []
    
    # Find all downloadable eBooks (they may have specific tags or indicators)
    books = soup.find_all('a', class_='bookTitle')
    
    # Iterate through all found books
    for book in books:
        title = book.text.strip()
        link = f"https://www.goodreads.com{book['href']}"
        
        # Try to find genre information (if present)
        genre_tag = book.find_next('a', class_='actionLinkLite bookPageGenreLink')
        genre = genre_tag.text if genre_tag else 'Unknown Genre'
        
        # Store the book information
        titles.append(title)
        genres.append(genre)
        download_links.append(link)
    
    # Create a DataFrame to hold the results
    books_df = pd.DataFrame({
        'Title': titles,
        'Genre': genres,
        'Download Link': download_links
    })
    
    return books_df

# Streamlit app
def main():
    # Set up the sidebar
    st.sidebar.title("Options")
    url = st.sidebar.text_input("Enter Goodreads eBooks URL", "https://www.goodreads.com/ebooks")
    
    # Main header for the app
    st.title("Book Finder")
    
    # Button to trigger the scraping
    if st.sidebar.button("Find Books"):
        with st.spinner("Fetching books..."):
            books_df = scrape_goodreads_ebooks(url)
            
            if not books_df.empty:
                st.success(f"Found {len(books_df)} books!")
                st.dataframe(books_df)
            else:
                st.error("No books found or failed to fetch the data.")
    
    st.sidebar.write("Enter the Goodreads eBooks URL and click 'Find Books' to display downloadable eBooks.")

# Run the Streamlit app
if __name__ == "__main__":
    main()

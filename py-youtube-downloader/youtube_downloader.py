# 12.07.2024 | Updated the cipher.py file to remove the dowloading bug for pytube v15.0.0 (based on https://github.com/pytube/pytube/issues/1954)

import streamlit as st
#from pytube import YouTube
from pytubefix import YouTube           # Started to use PyTubeFix instead of PyTube
from pytubefix.cli import on_progress
import os
import time


# Function to download YouTube video
def download_video(url):
    try:
        with st.spinner("Downloading your YouTube Video, Please Wait..."):
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download('downloads')
            #stream.download(output_path=os.path.expanduser("~/Desktop"))
        st.success("Download completed!")
        st.balloons() #Show Balloons as success story
    except Exception as e:
        st.error(f"Error occurred: {e}")

def execute_youtube_downloader():
    # Write your code for test1 here
    st.text("YouTube Downloader")
    # Input field for YouTube URL
    url = st.text_input("Enter YouTube video URL:", "")

    if st.button("Download"):
        if url:
            download_toast()
            download_video(url)
        else:
            st.warning("Please enter a valid YouTube URL.")


# Function to download YouTube video
def download_video_mp3(url):
    try:
        with st.spinner("Downloading the MP3 audio of your YouTube Video, Please Wait..."):
            yt = YouTube(url, on_progress_callback = on_progress)
            stream = yt.streams.get_audio_only()
            stream.download(mp3=True)

        st.success("MP3 from YouTube Video Downloaded!")
        st.balloons() #Show Balloons as success story
    except Exception as e:
        st.error(f"Error occurred: {e}")

def execute_youtube_downloader_mp3():
    # Write your code for test1 here
    st.text("YouTube Downloader MP3 Only")
    # Input field for YouTube URL
    url = st.text_input("Enter YouTube video URL:", "")

    if st.button("Download"):
        if url:
            download_toast()
            download_video_mp3(url)
        else:
            st.warning("Please enter a valid YouTube URL.")

# Function to read all video files in the "downloads" folder
def read_videos():
    videos = []
    folder_path = os.path.join(os.path.dirname(__file__), "downloads")
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith((".mp4", ".avi", ".mov")):
                videos.append(os.path.join(folder_path, file))
    return videos


def execute_select_video_local():
    st.text("Play the Videos in Dowloads Folder")
    videos = read_videos()
    selected_video = st.selectbox("Select a video:", videos, format_func=lambda x: os.path.basename(x))
    if selected_video:
        st.video(selected_video)


def execute_video_player():
    st.text("Play the Videos from the Local Drive")
    selected_video = st.file_uploader("Select a Video file:", type=['mp4', 'avi', 'mov'])
    if st.button("Play Video"):
        if selected_video:
            st.video(selected_video)
        else:
            st.warning("Please select a video file.")


# To display a short message known as a notification "toast".
def download_toast():
    msg = st.toast('Going to the YouTube Site...')
    time.sleep(1)
    msg.toast('Checking the URL...')
    time.sleep(1)
    msg.toast('Download in Progress!', icon = "🥞")


# Sidebar
def app_sidebar():
    ### App Sidebar Section Starts ###
    
    st.sidebar.title('✅ Settings ⚙️')

    menu_selection = st.sidebar.radio("Select Option:", ["Downloader: YouTube Videos", "Downloader: YouTube MP3 from URL", "Checkout Download Folder", "Browse More Videos"])

    # Execute function based on user selection
    if menu_selection == "Downloader: YouTube Videos":
        execute_youtube_downloader()
    elif menu_selection == "Downloader: YouTube MP3 from URL":    
        execute_youtube_downloader_mp3()
    elif menu_selection == "Checkout Download Folder":
        execute_select_video_local()
    elif menu_selection == "Browse More Videos":
        execute_video_player()

    st.sidebar.markdown("---")
    st.sidebar.markdown('📖 Opensource Code and ReadMe available app via this [Github Repo](https://github.com/kunalsuri/)!')
### App Sidebar Section Ends ###


# Streamlit UI
def main():
    st.title("Your Video Utility App")
    app_sidebar()

# Execute the main function
if __name__ == "__main__":
    main()
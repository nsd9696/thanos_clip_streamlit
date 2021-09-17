import streamlit as st
import search_app
import info_app
import similarity_app
import vid_search_app

pages = {
    "thanos_info": info_app,
    "thanos_image_search": search_app,
    "thanos_video_search": vid_search_app,
}    
st.image('thanos_search_logo.png', width=150)
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))
page = pages[selection]
page.app()
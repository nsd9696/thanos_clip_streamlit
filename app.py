import streamlit as st
import search_app
import similarity_app
import vid_search_app

pages = {
    "thanos_search": search_app,
    "thanos_vid_search": vid_search_app,
    "thanos_similarity": similarity_app
}    
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(pages.keys()))
page = pages[selection]
page.app()
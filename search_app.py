from search_api import *
import streamlit as st
import io
from PIL import Image
def app():
    
    st.header("Thanos Search")
    imageText = st.text_input("Search Image")
    if imageText:
        with st.spinner(text = 'Getting Images from Unsplash and sorting with clip ...'):
            
            imgSimScore, upSplashImages = getSortedQuery(imageText)
            images = [linkToImage(img) for img, score in imgSimScore]
            simScore = [f'Sim Score: {score:.2f}' for img, score in imgSimScore]
            upSplashImages = [linkToImage(img) for img in upSplashImages]
            upSplashIx = [i+1 for i in range(len(upSplashImages))]
            st.header("Thanos Search Result")
            st.image(images, width = 300, caption = simScore)
            
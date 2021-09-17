from search_api import *
import streamlit as st
import io
from PIL import Image
def app():
    
    st.header("Thanos Search")
    imageText = st.text_input("Search Image", value='a man with earphones')
    run_button = st.button("Thanos run")
    if run_button and imageText:
        with st.spinner(text = 'Getting Images from Unsplash and sorting with clip ...'):
            
            imgSimScore, upSplashImages = getSortedQuery(imageText)
            images = [linkToImage(img) for img, score in imgSimScore]
            simScore = [f'Sim Score: {score:.2f}' for img, score in imgSimScore]
            upSplashImages = [linkToImage(img) for img in upSplashImages]
            upSplashIx = [i+1 for i in range(len(upSplashImages))]
            st.header("Thanos Search Result")
            st.image(images, width = 300, caption = simScore)
    
    with st.expander("Sample Result"):
        st.image('thanos_image_search_sample.png')
    with st.expander("See explanation"):
        st.write("""
        - 해당 demo는 Unsplash api를 활용하여 입력한 text 내용으로 이미지를 검색한 뒤 가장 유사한 의미의 이미지를 추천해줍니다.
        - 현재는 text 입력에 영어만 가능합니다.
        - 사용할 수 있는 이미지 api가 있다면 더욱 다양하게 활용가능합니다.
        - api가 아닌 원본 이미지를 사용할 경우 해당 이미지를 미리 압축하여 이후 더 빠른 검색이 가능합니다.
        """)
            
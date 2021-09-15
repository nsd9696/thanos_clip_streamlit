from requests.api import options
from vid_search_api import *
import streamlit as st
import io

def app():

    st.header("Thanos Video Search")
    st.text("Upload Video or pre-compressed pkl file")
    vid_file = st.file_uploader(label="Upload Video", type=['avi','mp4'])
    encode_vid = st.button("Encode Video")
    if encode_vid:
        vid_data, vid_fps = convertVideoToArray(vid_file)
        with st.spinner(text = "Encoding Video"):
            print('start vid encoding')
            vid_data_processed = framePreprocess(vid_data)
            vid_encoded_frames = encodeFrame(vid_data_processed)

        textInput = st.text_input(label="Query Text")
        top_num = st.slider('How many top frames', 0, 20, 1)
        convert_button = st.button("Thanos run")
                
        if convert_button:
            encoded_text = encodeText(textInput)
            print('text encoded')
            print('start sim')
            simScore_list = getSimScore(vid_encoded_frames, encoded_text)
            top_frames = topSimScore(top_num, simScore_list)
            top_frames_num, top_frames_time, top_frames_image = showTopFrames(top_frames, vid_fps, vid_data)
            top_frames_image = arrayToImage(top_frames_image)
            st.header("Thanos Search Result")
            st.image(top_frames_image, width = 300, caption = top_frames_time)



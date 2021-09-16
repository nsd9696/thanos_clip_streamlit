from requests.api import options
from vid_search_api import *
import streamlit as st
import io
import pickle
import json
import pandas as pd
import xmltodict

def app():

    st.header("Thanos Video Search")
    st.text("Upload Video or pre-compressed json file")
    vid_file = st.file_uploader(label="Upload Video", type=['avi','mp4','json'])
    textInput = st.text_input(label="Query Text")
    convert_button = st.button("Thanos run")
    if vid_file and textInput and convert_button:
        print(vid_file.type)
        if str(vid_file.type) != "application/json": #file type is not json
            vid_data, vid_fps = convertVideoToArray(vid_file)
            with st.spinner(text = "Encoding Video"):
                print('start vid encoding')
                vid_data_processed = framePreprocess(vid_data)
                vid_encoded_frames = encodeFrame(vid_data_processed)

            with st.spinner(text = "Thanos Searching"):
                encoded_text = encodeText(textInput)
                print('text encoded')
                print('start sim')
                simScore_list = getSimScore(vid_encoded_frames, encoded_text)
                top_frames = topSimScore(20, simScore_list)
                top_frames_num, top_frames_time, top_frames_image = showTopFrames(top_frames, vid_fps, vid_data)
                top_frames_image = arrayToImage(top_frames_image)
                st.header("Thanos Search Result")
                st.image(top_frames_image, width = 300, caption = top_frames_time)

            download_file(vid_encoded_frames,vid_fps)

        else: # file type is json: already compressed
            with st.spinner(text = "Thanos Searching"):
                # with open(vid_file, 'r') as st_json:
                # vid_xml = vid_file.read()
                vid_json = json.load(vid_file)

                vid_fps = float(vid_json['vid_fps'])
                vid_encoded_frames = [torch.Tensor(i) for i in vid_json['vid_encoded_frames']]
                encoded_text = encodeText(textInput)
                print('text encoded')
                print('start sim')
                simScore_list = getSimScore(vid_encoded_frames, encoded_text)
                top_frames = topSimScore(20, simScore_list)
                top_frames_num, top_frames_time = showTopSeconds(top_frames, vid_fps)
                df_result = pd.DataFrame(top_frames_time, columns=['time(second)'])
                st.header("Thanos Search Result")
                st.write(df_result)

            download_df(df_result)
        




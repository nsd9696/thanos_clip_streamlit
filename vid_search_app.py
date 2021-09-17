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
        
    with st.expander("Sample Result"):
        st.image('thanos_vid_search_query1.png')
        st.image('thanos_vid_search_result1.png')
        st.image('thanos_vid_search_query2.png')
        st.image('thanos_vid_search_result2.png')
    with st.expander("See explanation"):
        st.write("""
        - 해당 demo는 비디오에서 입력한 text 내용과 가장 유사한 의미의 영상 구간을 추천해줍니다.
        - 비디오 전처리를 위해 1분 30초 이하 길이의 영상을 입력할 것을 권장드립니다.
        - 현재는 text 입력에 영어만 가능합니다.
        - avi 또는 mp4 파일을 업로드 할 경우 영상 구간과 함께 해당 장면을 함께 보여줍니다. 또한 압축된 비디오 data를 json 형태로 다운로드 받을 수 있습니다.
        - 이미 압축된 json 파일을 입력할 경우 매우 빠른 서치가 가능합니다. 결과로는 장면 이미지를 제외한 영상 구간에 대한 정보를 csv 형태로 제공합니다.
        """)



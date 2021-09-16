import torch
import clip
import os
import sys
import numpy as np
import torchvision
import streamlit as st
from PIL import Image
from tqdm import tqdm
import pickle
import base64
import io
import json

device = 'cpu'
model, preprocess = clip.load("ViT-B/32", device = 'cpu')

@st.cache
def convertVideoToArray(input_video):
    vid_torch = torchvision.io.read_video(input_video) 
    vid_data = np.array(vid_torch[0])
    vid_fps = vid_torch[2]['video_fps']  
    return vid_data, vid_fps

@st.cache
def framePreprocess(vid_data):
    vid_data_processed = [preprocess(Image.fromarray(f)) for f in vid_data]
    return vid_data_processed

@st.cache
def encodeFrame(vid_data_processed):
    vid_encoded_frames = []

    with torch.no_grad():
        for f in tqdm(vid_data_processed):
            image_features = model.encode_image(f.unsqueeze(0))
            vid_encoded_frames.append(image_features)
    
    return vid_encoded_frames

@st.cache
def encodeText(input_text):
    tokenizedText = clip.tokenize(input_text)
    with torch.no_grad():
        encoded_text = model.encode_text(tokenizedText)
    
    return encoded_text

def getSimScore(vid_encoded_frames, encoded_text):
    simScore_list = []
    for i,f in tqdm(enumerate(vid_encoded_frames)):
        simScore = torch.matmul(encoded_text, f.T)[0][0]
        simScore_list.append([i,simScore])
    
    return simScore_list

def topSimScore(top_num, simScore_list):
    sorted_simScore_list = sorted(simScore_list, key = lambda x: x[1], reverse=True)
    top_frames = sorted_simScore_list[:top_num]
    return top_frames

def showTopFrames(top_frames, vid_fps, vid_data):
    top_frames_num = list(np.array(top_frames).T[0].astype(int))
    top_frames_time = list((np.array(top_frames_num )/ vid_fps).astype(int))
    top_frames_image = [vid_data[i] for i in top_frames_num]

    return top_frames_num, top_frames_time, top_frames_image

def showTopSeconds(top_frames, vid_fps):
    top_frames_num = list(np.array(top_frames).T[0].astype(int))
    top_frames_time = list((np.array(top_frames_num )/ vid_fps).astype(int))
    return top_frames_num, top_frames_time

def arrayToImage(top_frames_image):
    return [Image.fromarray(i) for i in top_frames_image]

def download_file(_file,vid_fps):
    json_temp = {"vid_fps": vid_fps, "vid_encoded_frames": [i.tolist() for i in _file]}
    json_dumped = json.dumps(json_temp)
    b64 = base64.b64encode(json_dumped.encode('utf-8')).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="new_file.json">Download json</a>'
    st.write(href, unsafe_allow_html=True)

def download_df(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode('utf-8')).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="new_file.csv">Download csv</a>'
    st.write(href, unsafe_allow_html=True)

#输出为json
import streamlit as st
import pandas as pd
from moviepy.editor import VideoFileClip
import cv2
import json

def save_data(res):
    
    json_string = json.dumps(res,indent=4)
    with open('/Users/cesar/Downloads/label_res.json', 'w') as file:
        file.write(json_string)
    
    

def load_data(op1,op2,s,e):
    event={
        'type':'',
        'player':[],
        'start':'',
        'end':''
    }
    if(op1=='挡拆'):
        event['type']=1
    elif(op1=='无球掩护'):
        event['type']=2
    elif(op1=='手递手'):
        event['type']=3
    
    for i in op2:
        event['player'].append(i[1])
        
    event['start']=s
    event['end']=e    
    
    return event


def web2(video_file_path,video_duration,frame_count):
    
    col1, col2= st.columns([3,1])
    
    with col1:
        video_file = open(video_file_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        
    with col2:
        options1 = ['挡拆', '无球掩护', '手递手']
        selected_option1 = st.radio('配合类型', options1)
        options2 = ['P1', 'P2', 'P3','P4','P5']
        selected_option2 = st.multiselect('执行球员', options2)
        start_frame=st.text_input('开始帧',value='',key='start')
        end_frame=st.text_input('结束帧',value='',key='end')

        
        st.session_state['res']['frame_count']=frame_count
        if st.button('添加'):
            st.session_state['res']['events'].append(load_data(selected_option1,selected_option2,start_frame,end_frame))
            st.session_state['res_df'].append(load_data(selected_option1,selected_option2,start_frame,end_frame))
        if st.button('导出结果'):
            save_data(st.session_state['res'])
            st.write('结果已保存为label_res.json')
    
    st.sidebar.dataframe( st.session_state['res_df'])
    

if __name__=='__main__':
    video_file_path = '/Users/cesar/Downloads/1696750694862807.mp4'
    # 使用 moviepy 读取视频
    video = VideoFileClip(video_file_path)
    # 获取视频的总时长（以秒为单位）
    video_duration = video.duration
    video1 = cv2.VideoCapture(video_file_path)
    # 获取视频的帧数
    frame_count = int(video1.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if 'res_df' not in st.session_state:
        st.session_state['res_df']=[]
    
    if 'res' not in st.session_state:
        st.session_state['res']={
            'frame_count':0,
            'events':[]
        }
        
    
    web2(video_file_path,video_duration,frame_count)
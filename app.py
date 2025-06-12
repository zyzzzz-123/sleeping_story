import streamlit as st
import os
import random
from datetime import date, datetime, timedelta
from mutagen.mp3 import MP3
import base64
from streamlit_autorefresh import st_autorefresh

# 配置
STORY_DIR = "story_records"
MAX_PER_DAY = 2  # 每天最多抽取数量

# 获取今天日期
TODAY = str(date.today())

# 初始化 session_state
if 'drawn_files' not in st.session_state or st.session_state.get('drawn_date') != TODAY:
    st.session_state['drawn_files'] = []
    st.session_state['drawn_date'] = TODAY

if 'current_file' not in st.session_state:
    st.session_state['current_file'] = None

if 'auto_play' not in st.session_state:
    st.session_state['auto_play'] = False
if 'auto_start_time' not in st.session_state:
    st.session_state['auto_start_time'] = None
if 'auto_duration' not in st.session_state:
    st.session_state['auto_duration'] = None
if 'auto_files' not in st.session_state:
    st.session_state['auto_files'] = []
if 'auto_index' not in st.session_state:
    st.session_state['auto_index'] = 0
if 'auto_audio_start' not in st.session_state:
    st.session_state['auto_audio_start'] = None

# 获取所有 mp3 文件
NEW_DIR = os.path.join(STORY_DIR, "new")
if os.path.exists(NEW_DIR):
    new_files = [f for f in os.listdir(NEW_DIR) if f.endswith('.m4a')]
    new_files = [os.path.join('new', f) for f in new_files]
else:
    new_files = []
all_files = [f for f in os.listdir(STORY_DIR) if f.endswith('.m4a')]
all_files = [f for f in all_files if not f.startswith('new/')]  # Exclude new/ from main list
all_files = new_files + all_files  # Prioritize new_files
remaining_files = list(set(all_files) - set(st.session_state['drawn_files']))

st.set_page_config(page_title="小章给你讲睡前故事", page_icon="🌙", layout="centered")
st.title("🌙 小章给你讲睡前故事")

if len(st.session_state['drawn_files']) >= MAX_PER_DAY:
    st.info("故事已经抽完了，明天再来吧～")
else:
    if st.button('随机来一个故事'):
        if remaining_files:
            chosen = random.choice(remaining_files)
            st.session_state['drawn_files'].append(chosen)
            st.session_state['current_file'] = chosen
            st.session_state['auto_play'] = False
        else:
            st.info("故事已经抽完了，明天再来吧～")

    # 展示故事
    current_file = st.session_state.get('current_file')
    if current_file:
        st.subheader(f"开始听故事吧！")
        if current_file.startswith('new/'):
            audio_path = os.path.join(STORY_DIR, current_file)
        else:
            audio_path = os.path.join(STORY_DIR, current_file)
        with open(audio_path, 'rb') as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/m4a')

    # 自动顺序播放功能
    st.markdown('---')
    st.header('自动顺序播放')
    minutes = st.number_input('倒计时（分钟）', min_value=1, max_value=120, value=10, step=1, key='auto_timer_input')
    if st.button('开始自动播放'):
        st.session_state['auto_play'] = True
        st.session_state['auto_start_time'] = datetime.now()
        st.session_state['auto_duration'] = timedelta(minutes=minutes)
        st.session_state['auto_files'] = [f for f in all_files if f not in st.session_state['drawn_files']]
        st.session_state['auto_index'] = 0
        st.session_state['auto_audio_start'] = st.session_state['auto_start_time']

    if st.session_state['auto_play']:
        # 自动刷新，每1秒刷新一次
        st_autorefresh(interval=1000, key='auto_refresh')
        now = datetime.now()
        elapsed = now - st.session_state['auto_start_time']
        remain = st.session_state['auto_duration'] - elapsed
        # 判断是否到时或播放完所有文件
        if remain.total_seconds() <= 0 or st.session_state['auto_index'] >= len(st.session_state['auto_files']):
            st.session_state['auto_play'] = False
            st.success("倒计时结束，自动停止播放！")
        else:
            auto_files = st.session_state['auto_files']
            idx = st.session_state['auto_index']
            # 修正：推进auto_index和auto_audio_start到当前应该播放的音频
            audio_start = st.session_state['auto_audio_start']
            while idx < len(auto_files):
                fname = auto_files[idx]
                audio_path = os.path.join(STORY_DIR, fname)
                audio = MP3(audio_path)
                duration = int(audio.info.length)
                audio_elapsed = (now - audio_start).total_seconds()
                if audio_elapsed >= duration:
                    idx += 1
                    audio_start = audio_start + timedelta(seconds=duration)
                else:
                    break
            # 更新session_state
            st.session_state['auto_index'] = idx
            st.session_state['auto_audio_start'] = audio_start
            # 如果还有音频可播
            if idx < len(auto_files):
                fname = auto_files[idx]
                audio_path = os.path.join(STORY_DIR, fname)
                with open(audio_path, 'rb') as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'''
                <audio controls autoplay>
                  <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                  你的浏览器不支持 audio 元素。
                </audio>
                '''
                st.subheader(f"正在播放：{fname}")
                st.markdown(audio_html, unsafe_allow_html=True)
                st.info(f"自动播放中，剩余 {remain.seconds//60} 分 {remain.seconds%60} 秒")
            else:
                st.session_state['auto_play'] = False
                st.success("所有故事已播放完！")
    else:
        st.info('点击上方按钮，随机获取一个故事吧~') 
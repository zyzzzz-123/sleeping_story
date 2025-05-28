import streamlit as st
import os
import random
from datetime import date

# 配置
STORY_DIR = "story_records/converted"
MAX_PER_DAY = 2  # 每天最多抽取数量

# 获取今天日期
TODAY = str(date.today())

# 初始化 session_state
if 'drawn_files' not in st.session_state or st.session_state.get('drawn_date') != TODAY:
    st.session_state['drawn_files'] = []
    st.session_state['drawn_date'] = TODAY

# 获取所有 mp3 文件
all_files = [f for f in os.listdir(STORY_DIR) if f.endswith('.mp3')]
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
        else:
            st.info("故事已经抽完了，明天再来吧～")

    # 展示故事
    current_file = st.session_state.get('current_file')
    if current_file:
        st.subheader(f"故事：{current_file}")
        audio_path = os.path.join(STORY_DIR, current_file)
        with open(audio_path, 'rb') as f:
            audio_bytes = f.read()
        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.info('点击上方按钮，随机获取一个故事吧~') 
import os
import subprocess

SRC_DIR = 'story_records'
DST_DIR = os.path.join(SRC_DIR, 'converted')

os.makedirs(DST_DIR, exist_ok=True)

for filename in os.listdir(SRC_DIR):
    if filename.endswith('.mp3'):
        src_path = os.path.join(SRC_DIR, filename)
        dst_path = os.path.join(DST_DIR, filename)
        cmd = [
            'ffmpeg',
            '-y',  # 覆盖输出
            '-i', src_path,
            '-ar', '44100',  # 采样率 44.1kHz
            '-ac', '2',      # 立体声
            '-b:a', '128k',  # 比特率 128kbps
            dst_path
        ]
        print(f'正在转码: {filename} ...')
        subprocess.run(cmd, check=True)
print('全部转码完成，输出在 story_records/converted/') 
from interface import pipeline
import soundfile as sf
import numpy as np

# 读取音频文件
from pydub import AudioSegment

# 使用 pydub 打开音频文件
audio_segment = AudioSegment.from_file('/root/autodl-tmp/kzou/LLM-based-AI-Assistant/test.mp3')
audio_segment = audio_segment.set_frame_rate(16000).set_channels(1).set_sample_width(2)
# 将音频数据导出为 PCM 编码的字节流
audio = audio_segment.raw_data


pipeline(audio)
import os.path

from pydub import AudioSegment
import opuslib_next

class Opus_Encoder:
    def __init__(self):
        self.sample_rate = 16000
        self.channel_count = 1
        self.sample_width = 2

        self.opus_sample_rate = 10000
        self.opus_channel_count = 1
        self.

    def audio_to_opus(self, audio_path):
        #解析文件路径
        file_type = os.path.splitext(audio_path)[1]
        if file_type:
            file_type = file_type.lstrip('.')
        #加载音频文件
        audio = AudioSegment.from_file(audio_path, file_type)
        #设置单声道
        audio = audio.set_channels(self.channel_count)
        #设置采样频率
        audio = audio.set_frame_rate(self.sample_rate)
        #设置位宽
        audio = audio.set_sample_width(self.sample_width)
        #计算总时长，单位是s
        duration = len( audio)
        print( f"音频总时长：{duration} 秒")
        #获取原始的PCM数据
        raw_data = audio.raw_data
        print( f"原始PCM数据大小：{len(raw_data)} 字节")
        #初始化编码器
        encode = opuslib_next.Encoder.init(self.opus_sample_rate,self.opus_channel_count,opuslib_next.APPLICATION_AUDIO)

        for i in range(0,len(raw_data),960):
            # 获取当前的PCM数据
            frame_data = raw_data[i:i+960]
            #编码
            opus_data = encode(frame_data,960)




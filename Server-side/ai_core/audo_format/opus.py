import os.path
import numpy as np
from pydub import AudioSegment
import opuslib_next

class Opus_Encoder:
    def __init__(self):
        self.sample_rate = 16000
        self.channel_count = 1
        self.sample_width = 2

        self.opus_sample_rate = 16000
        self.opus_channel_count = 1
        self.opus_sample_width = 2
        self.opus_frame_time = 60 # 会影响传送个esp32的速率

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
        duration = len( audio) / 1000
        print( f"音频总时长：{duration} 秒")
        #获取原始的PCM数据
        raw_data = audio.raw_data
        print( f"原始PCM数据大小：{len(raw_data)} 字节")
        #初始化编码器
        encode = opuslib_next.Encoder(self.opus_sample_rate,self.opus_channel_count,opuslib_next.APPLICATION_AUDIO)
        #获取每帧的采样数,计算1ms的采样率，诚每帧的采样时间即可。
        frame_num = int(self.opus_sample_rate /  1000 * self.opus_frame_time )
        #计算每帧的采样字节数
        frame_byte_num = frame_num * self.opus_sample_width * self.opus_channel_count
        opus_dates = []
        for i in range(0,len(raw_data),frame_byte_num):
            # 获取当前的PCM数据
            frame_data = raw_data[i:i+frame_byte_num]
            frame_length = len(frame_data)
            #单独处理最后一帧，不满一帧补0
            if frame_length < frame_byte_num:
                frame_data += b'\x00' * (frame_byte_num - frame_length)

            # 转换为bytes数据原始数据是二进制流
            np_frame = np.frombuffer(frame_data, dtype=np.int16)
            np_bytes = np_frame.tobytes()
            # 编码
            opus_data = encode.encode(np_bytes, frame_num)
            opus_dates.append(opus_data)
        return opus_dates,duration

if __name__ == '__main__':
    opus = Opus_Encoder()
    data = opus.audio_to_opus('output.mp3')
    print(data)

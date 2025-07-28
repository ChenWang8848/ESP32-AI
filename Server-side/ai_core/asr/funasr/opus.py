import os.path
import wave
import numpy as np
from pydub import AudioSegment
import opuslib_next

class Opus_Encoder:
    _instance = None # 单例模式，在每次创建时，会检查是否已经创建过，如果已经创建过，则直接返回
    def __init__(self):
        self.sample_rate = 16000
        self.channel_count = 1
        self.sample_width = 2

        self.opus_sample_rate = 16000
        self.opus_channel_count = 1
        self.opus_sample_width = 2
        self.opus_frame_time = 60 # 会影响传送个esp32的速率
        self.opus_frame_size = int(self.opus_sample_rate /  1000 * self.opus_frame_time )
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
        frame_num = self.opus_frame_size
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

    # 保存二进制流的pous数据
    def save_opus_raw(self, opus_data, save_path):
        with open(save_path, 'wb') as f: # python中低层的迭代器，能够直接读取一帧一帧的数据。
            for frame in opus_data:
                f.write(len(frame).to_bytes(4,byteorder='big'))
                f.write(frame)

    def load_opus_raw(self, opus_path):
        frames = []
        with open(opus_path, 'rb') as f:
            while True:
                frame_len = int.from_bytes(f.read(4), byteorder='big')
                if frame_len == 0:
                    break
                frame = f.read(frame_len)
                frames.append(frame)
        return  frames
    def opus_to_audio(self, output_file, opus_data: list[ bytes]) -> str:
        #初始化解码器
        decode = opuslib_next.Decoder(self.opus_sample_rate,self.opus_channel_count)
        pcm_data = []
        for frame in opus_data:
            try:
                #解码
                pcm_frame = decode.decode(frame,self.opus_frame_size )
                pcm_data.append(pcm_frame)
            except opuslib_next.OpusError as e:
                print(f'解码失败:{e}')

        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(self.opus_channel_count)
            wf.setsampwidth(self.opus_sample_width)
            wf.setframerate(self.opus_sample_rate)
            wf.writeframes(b''.join(pcm_data))
        return output_file


if __name__ == '__main__':
    opus = Opus_Encoder()
    data = opus.audio_to_opus('output.mp3')
    print(data)
    opus.save_opus_raw(data[0], 'output.opus')
    data = opus.load_opus_raw('output.opus')
    print(data)
    opus.opus_to_audio('outpus.mp3',data)

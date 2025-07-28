from funasr import AutoModel
import sys
from .opus import Opus_Encoder

import soundfile
import os


# chunk_size = [0, 10, 5] #[0, 10, 5] 600ms, [0, 8, 4] 480ms
# encoder_chunk_look_back = 4 #number of chunks to lookback for encoder self-attention
# decoder_chunk_look_back = 1 #number of encoder chunks to lookback for decoder cross-attention
#
# model = AutoModel(model="paraformer-zh-streaming", model_revision="v2.0.4")
#
# wav_file = os.path.join(model.model_path, "example/asr_example.wav")
# speech, sample_rate = soundfile.read(wav_file)
# chunk_stride = chunk_size[1] * 960 # 600ms
#
# cache = {}
# total_chunk_num = int(len((speech)-1)/chunk_stride+1)
# for i in range(total_chunk_num):
#     speech_chunk = speech[i*chunk_stride:(i+1)*chunk_stride]
#     is_final = i == total_chunk_num - 1
#     res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back, decoder_chunk_look_back=decoder_chunk_look_back)
#     print(res)

class FunAsr:

    def __init__(self,config):
        self.dir = config.get("output_dir")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(self.current_dir, "model")
        self.model = AutoModel(model= self.model_dir , model_revision="v2.0.4")

    def audio_file_to_text(self, audio_file_path):
        res = self.model.generate(input=audio_file_path)
        return res[0]['text']
    def opus_file_to_text(self,opus_data, audio_file_path):
        opus = Opus_Encoder()
        output_file = opus.opus_to_audio(audio_file_path,opus_data)
        return self.audio_file_to_text(output_file)

if __name__ == "__main__":
    fun_asr = FunAsr()
    res = fun_asr.audio_file_to_text("output2.wav")
    print(res)
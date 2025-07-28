import asyncio
import os
from ai_core.llm.chatglm import ChatGLM
from ai_core.tts.edge_tts import EdgeTTS
from ai_core.util.util import Util
from ai_core.asr.funasr.fun_asr import FunAsr
from ai_core.asr.funasr.opus import Opus_Encoder

if __name__ == '__main__':
    config = Util.get_config()
    # llm = ChatGLM(config.get('LLM').get('ChatGLM'))
    # resource = llm.gnerate_response('你好')
    # tts = EdgeTTS(config.get('TTS').get('EdgeTTS'))
    # output_files = asyncio.run(tts.gnerate_response(resource, 'output.mp3'))
    #播放
    #os.system(f'start {output_files}')

    fun_asr = FunAsr(config.get('ASR').get('FunASR'))

    opus = Opus_Encoder()
    data = opus.load_opus_raw('output.opus')
    print(data)
    resource = fun_asr.opus_file_to_text(data,'1.wav')

    # esp32传过来的是opus的数据，希望能够直接进行处理

    print( resource)





import asyncio
import os
from ai_core.llm.chatglm import ChatGLM
from ai_core.tts.edge_tts import EdgeTTS

if __name__ == '__main__':
    llm = ChatGLM()
    resource = llm.gnerate_response('你好')
    tts = EdgeTTS()
    output_files = asyncio.run(tts.gnerate_response(resource, 'output.mp3'))
    #播放
    os.system(f'start {output_files}')
    print( resource)





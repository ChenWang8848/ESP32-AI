import edge_tts

class EdgeTTS:
    def __init__(self,config):
        self.voice = config.get("voice")

    async def gnerate_response(self, user_input, audio_path):
        communication = edge_tts.Communicate(user_input,self.voice)
        await communication.save(audio_path)
        return audio_path



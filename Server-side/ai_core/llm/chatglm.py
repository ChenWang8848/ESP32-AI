from openai import OpenAI
class ChatGLM:
    def __init__(self,config):
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name')
        self.url = config.get('url')
        self.client = OpenAI(api_key=self.api_key, base_url=self.url)

    def gnerate_response(self, user_input):
        dialogs = [
            {'role': 'system', 'content': '用幽默风趣的语言进行回答'},
            {'role': 'user', 'content': user_input},
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=dialogs,
        )
        return response.choices[0].message.content

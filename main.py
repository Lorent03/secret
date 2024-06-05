import http.client
import json

class Bot:
    def __init__(self, api_key, bot_id, base_url="api.coze.com"):
        self.api_key = api_key
        self.bot_id = bot_id
        self.base_url = base_url
        self.conversation_id = None
        self.chat_history = []

    def ask(self, user, query, stream=False):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*'
        }

        data = {
            'bot_id': self.bot_id,
            'user': user,
            'query': query,
            'stream': stream,
            'chat_history': self.chat_history
        }

        if self.conversation_id:
            data['conversation_id'] = self.conversation_id

        conn = http.client.HTTPSConnection(self.base_url)
        conn.request("POST", "/open_api/v2/chat", body=json.dumps(data), headers=headers)
        
        response = conn.getresponse()
        response_data = response.read().decode()

        if response.status == 200:
            response_json = json.loads(response_data)
            self.conversation_id = response_json.get('conversation_id')
            messages = response_json.get('messages', [])
            for message in messages:
                self.chat_history.append(message)
            return messages
        else:
            return f"Error: {response.status} - {response_data}"

def main():
    api_key = "pat_8BIXdKJUqnzXN1vh9CEMLDkh6LZP63cYPxtrd1Duc5TXK7Oqlm7hXSfyTYp2Fr8b"
    bot_id = "7376391267590651909"
    user_id = "7376391267590488069"
    bot = Bot(api_key, bot_id)

    print("Bot: Привет! Задайте мне вопрос.")
    while True:
        question = input("Вы: ")
        if question.lower() in ['exit', 'quit', 'выход']:
            print("Bot: До свидания!")
            break
        messages = bot.ask(user_id, question)
        for message in messages:
            if message['role'] == 'assistant':
                print(f"Bot: {message['content']}")

if __name__ == "__main__":
    main()

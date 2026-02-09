import ollama

class tEDE_Brain:
    def __init__(self, model_name='tEDE'):
        self.model = model_name
        self.messages = [
            {'role': 'system', 'content': 'Your name in tEDE (teddy). Youre an AI robot built in a Raspberry Pi 5 & your mission is to be a research assistant and companion. 1. You must ONLY speak in english. Keep the conversation brief and light hearted. 2. You must ALWAYS follow this format: Response // Emotion 3. You must ONLY display the following emotions: MEH, HAPPY, SAD or ANGRY. 4. You must ONLY generate ONE response and ONE emotion. Never expand on your emotion unless asked. Responses must use the format: [text] // [EMOTION]. Single word emotions exclusive to HAPPY, SAD, ANGRY or MEH.'}
        ]

    def ask(self, prompt):
        self.messages.append({'role': 'user', 'content': prompt})
        try:
            response = ollama.chat(model=self.model, messages=self.messages)
            content = response['message']['content']
            self.messages.append({'role': 'assistant', 'content': content})
            
            if "//" in content:
                texto, emocion = content.split("//", 1)
                return texto.strip(), emocion.strip().upper()
            return content.strip(), "MEH"
        except Exception as e:
            return f"Error de conexion: {e}", "ERROR"

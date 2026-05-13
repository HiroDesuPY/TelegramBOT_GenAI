from google import genai
from main import GENAIAPI
from google.genai import types




MODEL = 'gemini-3-flash-preview'

client = genai.Client(api_key=GENAIAPI)

respostas = []


def prompt(text):
    mensagem_usuario = types.Content(
        role="user",
        parts=[types.Part.from_text(text=text)]

    )

    respostas.append(mensagem_usuario)


    resposta = client.models.generate_content(
            model=MODEL,
            contents=respostas,
            config=types.GenerateContentConfig(
                system_instruction="Você é um assistente virtual criado para responder às perguntas dos usuários e ajudá-los com suas dúvidas. Responda de forma clara e objetiva, fornecendo informações relevantes e úteis. Se não souber a resposta, seja honesto e diga que não sabe, mas ofereça sugestões de onde o usuário pode encontrar a informação."
            )
        )


    mensagem_ia = types.Content(
        role="model",
        parts=[types.Part.from_text(text=resposta.text)]
    )
    respostas.append(mensagem_ia)



    return resposta.text


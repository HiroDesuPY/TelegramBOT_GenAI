from main import TELEGRAMKEY
import telebot
from telebot import types
from ai import prompt


bot = telebot.TeleBot(TELEGRAMKEY)

usuarios = {}

@bot.message_handler(commands=['start'])
def start_ia(message):
    usuarios[message.chat.id] = True
    bot.send_message(message.chat.id, "Olá! Eu sou o HirosBot, um assistente virtual criado para responder às suas perguntas e ajudá-lo com suas dúvidas. Sinta-se à vontade para me perguntar qualquer coisa ou solicitar informações. Estou aqui para ajudar! Pressione o botão 'Sair' a qualquer momento para encerrar a conversa.")



@bot.callback_query_handler()
def handle_callback_query(call: types.CallbackQuery):
    match call.data:
        case "start":
            usuarios[call.message.chat.id] = True
            bot.send_message(call.message.chat.id, "Olá! Eu sou o HirosBot, um assistente virtual criado para responder às suas perguntas e ajudá-lo com suas dúvidas. Sinta-se à vontade para me perguntar qualquer coisa ou solicitar informações. Estou aqui para ajudar! Pressione o botão 'Sair' a qualquer momento para encerrar a conversa.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Sair", callback_data="sair")))


        case 'about':
            bot.send_message(call.message.chat.id, "Este é um bot de teste para o GenAI. Ele foi criado para demonstrar como usar o GenAI em um bot do Telegram. Ele pode responder a mensagens e interagir com os usuários usando botões inline. Fique à vontade para testar e explorar suas funcionalidades!")


        case "sair":
            bot.send_message(call.message.chat.id, "Até mais! Se precisar de ajuda novamente, é só me chamar :).")
            usuarios[call.message.chat.id] = False




@bot.message_handler(func=lambda message: usuarios.get(message.chat.id))
def conversaria(message):
    if message.text.lower() == "sair":
        usuarios[message.chat.id] = False
        bot.send_message(message.chat.id, "Até mais! Se precisar de ajuda novamente, é só me chamar :).")
        return

    markup = types.InlineKeyboardMarkup()
    sair = types.InlineKeyboardButton("Sair", callback_data="sair")
    markup.add(sair)
    try:
        resposta = prompt(message.text)
        bot.send_message(message.chat.id, resposta, reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, f"Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde. Erro: {e}", reply_markup=markup)
        print(f"Erro ao processar a mensagem: {e}")





@bot.message_handler(func=lambda message: True)
def start(message):
    texto = "Olá, eu sou um bot de teste para o GenAI. Clique no botão abaixo para começar a conversar comigo!"
    markup = types.InlineKeyboardMarkup()

    start = types.InlineKeyboardButton("Start", callback_data="start")
    about = types.InlineKeyboardButton("About", callback_data="about")

    markup.add(start)
    markup.add(about)


    bot.send_message(message.chat.id, texto, reply_markup=markup)







bot.polling(none_stop=True, timeout=90)
#########################################################

from config import bot
import config
from time import sleep
import re
import logic
import database.db as db
import telebot
import ast
from telebot import types

stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
crossIcon = u"\u274C"

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    
#########################################################

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,
                                              callback_data="['value', '" + value + "', '" + key + "']"),
        types.InlineKeyboardButton(text=crossIcon,
                                   callback_data="['key', '" + key + "']"))

    return markup
    
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)

    if (call.data.startswith("['key'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Here are the values of stringList",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')



'''
Encargado de recibir la petición de "Registrarse" como cliente.
En la cual se completan los datos
'''


@bot.message_handler(regexp=r"^(Registrar usuario|ru)$")
def en_registrarse(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    text = 'Registrar nuevo usuario (Favor responder el siguiente mensaje)'
    bot.send_message(
		message.chat.id, 
		text, 
		parse_mode="Markdown") 
    
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    text = '¿Cuál es tu número de documento?'
    bot.send_message(
		message.chat.id, 
		text, 
		parse_mode="Markdown") 

'''
Encargado de recibir la respuesta a la pregunta "¿Cuál es tu número de documento?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es tu número de documento?")
def en_registrarse_documento(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    """ parts = re.match(
		r"^([+]?([0-9]+)$", 
		message.text)
    
    documento = float(parts[2]) """
    
    usuario = logic.obtener_usuario_registro(message.from_user.id)
    if usuario is None:
        logic.crear_nuevo_usuario(message.from_user.id, message.text)
        pregunta = 'Y ¿Como te llamas?'
        bot.send_message(message.chat.id, pregunta, parse_mode="Markdown")
        
    else:
        pregunta = 'El usuario ya existe en el sistema \r\n deseas actualizar los datos? (Si | No): '
        bot.send_message(message.chat.id, pregunta, parse_mode="Markdown")
        #datos = {'documento_identidad': message.text}
        #logic.actualizar_datos_modelo(usuario, datos)
    


'''
Encargado de recibir la respuesta a la pregunta "¿Cuál es tu número de teléfono?"
'''


@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "Y ¿Como te llamas?")
def en_registrarse_telefono(message):    
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    cliente = logic.obtener_cliente_registro(message.from_user.id)
    datos = {'telefono': message.text}
    logic.actualizar_datos_modelo(cliente, datos)
    text = 'Selecciona el tipo de usuario'
    bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.send_message(chat_id=message.chat.id,
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')
    

######################################################################


@bot.message_handler(commands=['help'])
def on_command_help(message):
	bot.send_chat_action(message.chat.id, 'typing')

	bot.send_message(
		message.chat.id, 
		logic.get_help_message (), 
		parse_mode="Markdown") 
  
#########################################################

if __name__ == '__main__':
    bot.polling(timeout=20)
    
#########################################################
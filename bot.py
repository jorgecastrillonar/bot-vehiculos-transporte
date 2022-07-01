##############################################################################
from config import bot
from time import sleep
import re
import logic
import decorators
import database.db as db
import ast
from telebot import types
from models.Usuario import Usuario
from models.TipoUsuario import TipoUsuario

#user = Usuario()

prueba = {'id': '','documento': ''}
##############################################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
##############################################################################
@bot.message_handler(commands=['start'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    emojiExito = decorators.emojis_exito()
    bot.send_message(
		message.chat.id, 
		emojiExito, 
		parse_mode="Markdown") 

##########################################################################

"""
Encargado de recibir la petición de registrar un nuevo usuario.
"""
@bot.message_handler(regexp=r"^(Registrar usuario|nuevo usuario|crear usuario|Cu|cu)$")
def registrar_nuevo_usuario(message, flag=False):
    
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    if flag == False:
        text = 'Registrar nuevo usuario (Favor responder el siguiente mensaje)'
        bot.send_message(
            message.chat.id, 
            text, 
            parse_mode="Markdown") 
    
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    text = '¿Cuál es el número de documento del usuario?'
    bot.send_message(
		message.chat.id, 
		text, 
		parse_mode="Markdown") 
##############################################################################
"""
Metodo que recibe la respuesta para almacenar al usuario
"""
@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "¿Cuál es el número de documento del usuario?")
def registrar_documento(message, flag=False):
    if flag == False:
        parts = re.match(
            r"(?:^|[^\-\d])(\d+){1,10}", 
            message.text)
    else:
        parts = 1

    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    if parts == None:
        text = 'Lo siento no puedo recibir datos diferentes a numeros. \r\nRepitamos el proceso.'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        registrar_nuevo_usuario(message, flag=True)      
    else:
        usuario = logic.obtener_usuario_documento(message.text)
        if usuario is None:
            
            logic.crear_nuevo_usuario(message.text)
            ############### REFACTOR: CAMBIAR DE GLOBAL A INSTANCIA
            #user.documento_identidad = message.text
            ############### REFACTOR: CAMBIAR DE GLOBAL A INSTANCIA
            globales = globals()
            globales['prueba'] = {'id': message.from_user.id, 'documento': message.text}
            
            text = 'Y ¿Como se llama el usuario?'
            bot.send_message(message.chat.id, text, parse_mode="Markdown")  
        else:
            text = 'El usuario ya existe en el sistema \r\ndeseas actualizar los datos? (Si | No): '
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
            
##############################################################################        
"""
Metodo que actualiza el nombre del usuario 
y lanza el teclado en pantalla
"""
@bot.message_handler(func=lambda message: message.reply_to_message != None and message.reply_to_message.text == "Y ¿Como se llama el usuario?")
def registro_tipo_usuario(message):       
    parts = re.match(
		r"[a-zA-ZÀ-ÖØ-öø-ÿ-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*", 
		message.text)
    
    globales = globals()
    ############### REFACTOR: CAMBIAR DE GLOBAL A INSTANCIA
    if globales['prueba']['id'] != message.from_user.id:
        pass
    else:
        if parts == None:
            text = 'Lo siento no puedo recibir datos diferentes a letras.'+ decorators.emojis_excepcion 
            +'\r\n \r\nRepitamos el proceso.'
            bot.send_message(message.chat.id, text, parse_mode="Markdown")
            registrar_documento(message, flag=True)    
        else:
            usuario = logic.obtener_usuario_documento(globales['prueba']['documento'])
            datos = {'nombre_completo': message.text}
            logic.actualizar_datos_modelo(usuario, datos)
            
            ##REFACTOR EXTRACT##
            bot.send_chat_action(message.chat.id, 'typing')
            sleep(1)        
            text = 'Selecciona el tipo de usuario'
            bot.send_message(message.chat.id,
                            text,
                            reply_markup=makeKeyboard(),
                            parse_mode='HTML')
############################################################################################
"""
Metodo encargado de recibir la respuesta del teclado en pantalla y procesarla.
"""
@bot.callback_query_handler(func=lambda message: message)
def handle_query(message):
    if (message.data.startswith("['value'")):
        print(f"message.data : {message.data} , type : {type(message.data)}")
        print(f"ast.literal_eval(message.data) : {ast.literal_eval(message.data)} , type : {type(ast.literal_eval(message.data))}")
        globales = globals()
        keyFromCallBack = ast.literal_eval(message.data)[2]
        usuario = logic.obtener_usuario_documento(globales['prueba']['documento'])
        datos = {'tipo_usuario_id': keyFromCallBack}
        logic.actualizar_datos_modelo(usuario, datos)
        ############### REFACTOR: CAMBIAR DE GLOBAL A INSTANCIA
        globales = globals()
        text = 'Felicidades, terminaste el registro. '+decorators.emojis_exito()
        bot.send_message(
            globales['prueba']['id'],
            text,
            parse_mode='Markdown'
        )
###########################################################################################
""" 
Metodo que permite generar el teclado en pantalla para la seleccion de tipo_usuario 
@return markup Respuestaa con el teclado creado.
"""
def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    objectTipoUsuario = logic.obtener_tipo_usuario()
    for t in objectTipoUsuario:
        markup.add(types
        .InlineKeyboardButton(text=t.nombre,
        callback_data="['value', '" + t.nombre + "', '" + str(t.id) + "']"))    
    return markup
############################################################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
############################################################################################
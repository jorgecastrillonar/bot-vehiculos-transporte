#########################################################

from ast import Import
from statistics import mode
##############################################################################
from config import bot
from time import sleep
import re
import logic
import decorators
import database.db as db
from models.Revision import Revision
from models.Vehiculo import Vehiculo
from models.TipoVehiculo import TipoVehiculo
from telebot import types
import ast
from models.Usuario import Usuario
from models.TipoUsuario import TipoUsuario
from models.VehiculoRevision import VehiculoRevision

vehiculo = Vehiculo()
revision = Revision()

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

##############################################################################

'''
Contruir teclado en pantalla
@return datos_listar Lista de elementos a mostrar
'''
def makeKeyboard(datos_listar, tipo):
    markup = types.InlineKeyboardMarkup()

    for item in datos_listar:
        markup.add(types.InlineKeyboardButton(text=item.nombre,callback_data="['"+ tipo +"', '" + str(item.id) + "']"))

    return markup

#########################################################
 
'''
Contruir teclado en pantalla
@return datos_listar Lista de elementos a mostrar
'''
def makeKeyboardVehiculos(vehiculos):
    markup = types.InlineKeyboardMarkup()

    for item in vehiculos:
        markup.add(types.InlineKeyboardButton(text=item.placa,callback_data="['lista_vehiculos', '" + str(item.placa) + "']"))

    return markup

#########################################################

"""
Recibe la petición para registrar un nuevo vehículo
"""
@bot.message_handler(regexp=r"^(registrar vehículo|registrar vehiculo|rh)$")
def commando_registrar_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    response = bot.reply_to(message, "¿Cuál es la placa del vehículo?")
    bot.register_next_step_handler(response, proceso_placa)

#########################################################

def proceso_placa(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    placa = message.text
    vehiculo.placa = placa

    
    if len(placa) == 6 and re.match(r'^[A-Z|a-z]{3}[0-9]{3}$', placa):
        response = bot.reply_to(message, '¿Cuál es la marca del vehículo?')
        bot.register_next_step_handler(response, proceso_marca)
    else:
        response = bot.reply_to(message, "La placa debe tener 6 caracteres y debe ser un dato alfanumerico, ¿Cuál es la placa del vehículo?")
        bot.register_next_step_handler(response, proceso_placa)
    
#########################################################


def proceso_marca(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    marca = message.text
    vehiculo.marca = marca
    
    if re.match(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$', marca):
        response = bot.reply_to(message, '¿Cuál es el modelo del vehículo')
        bot.register_next_step_handler(response, proceso_modelo)
    else:
        response = bot.reply_to(message, "La marca no debe contener caracteres especiales, ¿Cuál es la marca del vehículo?")
        bot.register_next_step_handler(response, proceso_marca)
    
    
    
#########################################################

def proceso_modelo(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    modelo = message.text
    vehiculo.modelo = modelo
    
    
    lista_tipo_vehiculos = logic.listar_tipos_vehiculos()
    
    if modelo.isdigit():
        bot.send_message(message.chat.id,
                     "Selecciona el tipo de vehículo",
                     reply_markup=makeKeyboard(lista_tipo_vehiculos, 'vehiculo'),
                     parse_mode='HTML')
        
    else:
        response = bot.reply_to(message, 'El modelo solo debe ser un dato numérico, ¿Cuál es el modelo del vehículo')
        bot.register_next_step_handler(response, proceso_modelo)

########################################################

@bot.message_handler(regexp=r"^(realizar revision|rr)$")
def commando_realizar_revision(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    response = bot.reply_to(message, "¿Cuál es el nivel de aceite del vehículo? (en mililitros mL)")
    bot.register_next_step_handler(response, proceso_nivel_aceite)

########################################################

def proceso_nivel_aceite(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    revision.nivel_aceite = message.text
    
    
    if revision.nivel_aceite.isdigit():
        response = bot.reply_to(message, "¿Cuál es el nivel de liquido de frenos del vehículo? (en mililitros mL)")
        bot.register_next_step_handler(response, proceso_nivel_liquido_frenos)
        
    else:
        response = bot.reply_to(message, 'El nivel de aceite debe ser un dato numérico, ¿Cuál es el nivel de aceite del vehículo? (en mililitros mL)')
        bot.register_next_step_handler(response, proceso_nivel_aceite)


########################################################

def proceso_nivel_liquido_frenos(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    revision.nivel_liquido_frenos = message.text
    
    
    if revision.nivel_liquido_frenos.isdigit():
        response = bot.reply_to(message, "¿Cuál es el nivel de refrigerante del vehículo? (en mililitros mL)")
        bot.register_next_step_handler(response, proceso_nivel_refrigerante)
        
    else:
        response = bot.reply_to(message, 'El nivel de liquido de frenos debe ser un dato numérico, ¿Cuál es el nivel de liquido de frenos del vehículo? (en mililitros mL)')
        bot.register_next_step_handler(response, proceso_nivel_liquido_frenos)

########################################################

def proceso_nivel_refrigerante(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    revision.nivel_refrigerante = message.text
    
    
    if revision.nivel_refrigerante.isdigit():
        response = bot.reply_to(message, "¿Cuál es el nivel de liquido de dirección del vehículo? (en mililitros mL)")
        bot.register_next_step_handler(response, proceso_nivel_liquido_direccion)
        
    else:
        response = bot.reply_to(message, 'El nivel de refrigerante debe ser un dato numérico, ¿Cuál es el nivel de refrigerante del vehículo? (en mililitros mL)')
        bot.register_next_step_handler(response, proceso_nivel_refrigerante)

########################################################

def proceso_nivel_liquido_direccion(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    revision.nivel_liquido_direccion = message.text
    
    
    if revision.nivel_liquido_direccion.isdigit():
        vehiculos = logic.listar_vehiculos()
    
        bot.send_message(message.chat.id,
                     "Seleccione el vehículo para realizar la revisión",
                     reply_markup=makeKeyboardVehiculos(vehiculos),
                     parse_mode='HTML')
        
    else:
        response = bot.reply_to(message, 'El nivel de liquido de dirección debe ser un dato numérico, ¿Cuál es el nivel de liquido de dirección del vehículo? (en mililitros mL)')
        bot.register_next_step_handler(response, proceso_nivel_liquido_direccion)

########################################################

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
            
            objectTipoUsuario = logic.obtener_tipo_usuario()
            
            ##REFACTOR EXTRACT##
            bot.send_chat_action(message.chat.id, 'typing')
            sleep(1)        
            text = 'Selecciona el tipo de usuario'
            bot.send_message(message.chat.id,
                            text,
                            reply_markup=makeKeyboard(objectTipoUsuario,'usuario'),
                            parse_mode='HTML')
############################################################################################
"""
Metodo encargado de recibir la respuesta del teclado en pantalla y procesarla.
"""
@bot.callback_query_handler(func=lambda message: message)
def handle_query(message):
    print(message.data)
    if (message.data.startswith("['usuario'")):
        print(f"message.data : {message.data} , type : {type(message.data)}")

        #print(f"ast.literal_eval(message.data) : {ast.literal_eval(message.data)} , type : {type(ast.literal_eval(message.data))}")
        globales = globals()
        keyFromCallBack = ast.literal_eval(message.data)[1]
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
        
    if (message.data.startswith("['vehiculo'")):
        id_tipo_vehiculo = ast.literal_eval(message.data)[1]
        vehiculo_nuevo = logic.registrar_vehiculo(vehiculo.placa,vehiculo.marca,vehiculo.modelo,id_tipo_vehiculo)
        
        bot.reply_to(
            message.message,
            f"\U0001F697 Se registró el vehículo con placas: {vehiculo_nuevo.placa}, marca: {vehiculo_nuevo.marca}, modelo: {vehiculo_nuevo.modelo} y tipo vehiculo: {vehiculo_nuevo.tipo_vehiculo.nombre}" if vehiculo_nuevo is not None
            else f"El vehículo ya se encuentra registrado.")
    
    if (message.data.startswith("['lista_vehiculos'")):
        placa = ast.literal_eval(message.data)[1]
        nueva_revision = logic.registrar_revision(revision)
        
        registrar_revision = logic.registrar_revision_vehiculo(nueva_revision.id,placa)
    
        bot.reply_to(
            message.message,
            f"\U00002705 Se registró una revisión al vehículo con placas: {placa}" if registrar_revision is not None
            else f"No fue posible registrar la revisión, intenta de nuevo.") 
     
###########################################################################################

@bot.message_handler(regexp=r"^(Asignar mecánico|Asignar mecanico|am) ([0-9]+) a ([A-Za-z0-9]+)$")
def on_asignar_mecanico(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    parts = re.match(
        r"^(Asignar mecánico|Asignar mecanico|am) ([0-9]+) a ([A-Za-z0-9]+)$",
        message.text,
        flags=re.IGNORECASE)
    
    documento_identidad_usuario = int(parts[2])
    placa_vehiculo = parts[3]
    
    text = logic.asignar_mecanico (documento_identidad_usuario, placa_vehiculo)
    
    bot.reply_to(message, text, parse_mode="Markdown")
    

#########################################################

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)

############################################################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
############################################################################################
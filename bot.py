##############################################################################
from config import bot
from time import sleep
from statistics import mode
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
import prettytable as pt
from markdownTable import markdownTable
from models.VehiculoRevision import VehiculoRevision

vehiculo = Vehiculo()
revision = Revision()

user = Usuario()

prueba = {'id': '','documento': ''}
##############################################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
##############################################################################
@bot.message_handler(commands=['start'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    emojiExito = decorators.emojis_exito() + ' ' + decorators.emojis_excepcion()
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
        response = bot.reply_to(message, "La placa debe tener 6 caracteres y debe ser un dato alfanumerico de la forma AAA000, ¿Cuál es la placa del vehículo?")
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
    
    if modelo.isdigit() and len(modelo)==4:
        bot.send_message(message.chat.id,
                     "Selecciona el tipo de vehículo",
                     reply_markup=makeKeyboard(lista_tipo_vehiculos, 'vehiculo'),
                     parse_mode='HTML')
        
    else:
        response = bot.reply_to(message, 'El modelo solo debe ser un dato numérico de 4 dígitos, ¿Cuál es el modelo del vehículo')
        bot.register_next_step_handler(response, proceso_modelo)

########################################################

@bot.message_handler(regexp=r"^(realizar revision|realizar revisión|rr)$")
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
        response = bot.reply_to(message, "¿Cuál es el nivel de líquido de frenos del vehículo? (en mililitros mL)")
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
        response = bot.reply_to(message, 'El nivel de líquido de frenos debe ser un dato numérico, ¿Cuál es el nivel de líquido de frenos del vehículo? (en mililitros mL)')
        bot.register_next_step_handler(response, proceso_nivel_liquido_frenos)

########################################################

def proceso_nivel_refrigerante(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    revision.nivel_refrigerante = message.text
    
    
    if revision.nivel_refrigerante.isdigit():
        response = bot.reply_to(message, "¿Cuál es el nivel de líquido de dirección del vehículo? (en mililitros mL)")
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
        response = bot.reply_to(message, 'El nivel de líquido de dirección debe ser un dato numérico, ¿Cuál es el nivel de liquido de dirección del vehículo? (en mililitros mL)')
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
    text = '¿Cuál es el número de documento del usuario?'+decorators.emojis_pregunta()
    response = bot.reply_to(message, text)
    bot.register_next_step_handler(response, paso_documento)
 
##############################################################################
"""
Metodo que recibe la respuesta para almacenar al usuario
"""
def paso_documento(message, flag=False):
    
    if flag == False:
        parts = re.match(r'\s*\d+(?:\s+\d+)*\s*$'
                 ,message.text)
    else:
        parts = 1

    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    if parts == None:
        text = 'Lo siento no puedo recibir datos diferentes a numeros.'+decorators.emojis_excepcion()+'\r\nRepitamos el proceso.'
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
        registrar_nuevo_usuario(message, flag=True)      
    else:
        usuario = logic.obtener_usuario_documento(message.text)
        if usuario is None:
            user.documento_identidad = message.text
            text = 'Y ¿Como se llama el usuario?'+decorators.emojis_pregunta()
            response = bot.reply_to(message, text)
            bot.register_next_step_handler(response, paso_tipo_usuario)
        else:
            text = 'El usuario ya existe en el sistema \r\ndeseas actualizar los datos?'+decorators.emojis_pregunta()+'(Si | No): '
            response = bot.reply_to(message, text)
            #bot.register_next_step_handler(response, registrar_documento)   
            
##############################################################################        
"""
Metodo que actualiza el nombre del usuario 
y lanza el teclado en pantalla
"""
def paso_tipo_usuario(message):       
    parts = re.match(
		r"[a-zA-ZÀ-ÖØ-öø-ÿ-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*", 
		message.text)
    
    if parts == None:
        text = 'Lo siento no puedo recibir datos diferentes a letras.'+decorators.emojis_fallo() 
        +'\r\n \r\nRepitamos el proceso.'
        response = bot.reply_to(message, text)
        bot.register_next_step_handler(response, paso_documento(message,True))
    else:
        user.nombre_completo = message.text
        objectTipoUsuario = logic.obtener_tipo_usuario()   
        lanzar_teclado(message, objectTipoUsuario)    
############################################################################################
"""
Metodo que permite lanzar el teclado de seleccion de tipos.
"""
def lanzar_teclado(message, objeto):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)        
    text = 'Selecciona el tipo de usuario'
    bot.send_message(message.chat.id,
                    text,
                    reply_markup=makeKeyboard(objeto,'usuario'),
                    parse_mode='HTML')
############################################################################################
"""
Metodo encargado de recibir la respuesta del teclado en pantalla y procesarla.
"""
@bot.callback_query_handler(func=lambda message: message)
def handle_query(message):
    dato_seleccionado = ast.literal_eval(message.data)[1]
    if (message.data.startswith("['usuario'")):

        usuario = logic.crear_nuevo_usuario(user.documento_identidad,user.nombre_completo, dato_seleccionado)
        
        bot.reply_to(
            message.message,
            f''+decorators.emojis_exito()+decorators.emojis_exito()
            +' Se registró al usuario con \r\nDocumento: '+str(usuario.documento_identidad)
            +' \r\nMarca: '+ str(usuario.nombre_completo)         
            +' \r\nTipo de Usuario: '+str(usuario.tipo_usuario.nombre) if usuario is not None
            else f'El usuario ya se encuentra registrado.'
            +decorators.emojis_excepcion()+decorators.emojis_excepcion()) 
        
    if (message.data.startswith("['vehiculo'")):
        vehiculo_nuevo = logic.registrar_vehiculo(vehiculo.placa,vehiculo.marca,vehiculo.modelo,dato_seleccionado)
        
        bot.reply_to(
            message.message,
            f"\U0001F697 Se registró el vehículo con placas: {vehiculo_nuevo.placa}, marca: {vehiculo_nuevo.marca}, modelo: {vehiculo_nuevo.modelo} y tipo vehiculo: {vehiculo_nuevo.tipo_vehiculo.nombre}" if vehiculo_nuevo is not None
            else f"El vehículo ya se encuentra registrado.")
    
    if (message.data.startswith("['lista_vehiculos'")):
        nueva_revision = logic.registrar_revision(revision)
        
        registrar_revision = logic.registrar_revision_vehiculo(nueva_revision.id,dato_seleccionado)
    
        bot.reply_to(
            message.message,
            f"\U00002705 Se registró una revisión al vehículo con placas: {dato_seleccionado}" if registrar_revision is not None
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
    
###########################################################################################
"""
Metodo que permite listar todos los registros de la tabla revision
"""
@bot.message_handler(regexp=r"^(Listar usuarios|listar usuarios|Ver usuarios|ver usuarios|ltu)$")
def listar_usuarios(message):
    data = logic.obtener_usuarios()
    table = pt.PrettyTable(['Documento', 'Nombre', 'Tipo'])
    table.align['Documento'] = 'l'
    table.align['Nombre'] = 'l'
    table.align['Tipo'] = 'l'

    for item in data:
        table.add_row([item.documento_identidad, f'{item.nombre_completo}', f'{item.tipo_usuario.nombre}'])
    bot.reply_to(message, f'<pre>{table}</pre>', parse_mode="HTML")
    
    """ markdownTable(table).setParams(row_sep = 'topbottom'
                                  , padding_width = 5, padding_weight='left').getMarkdown() """
###########################################################################################
"""
Metodo que permite listar todos los registros de la tabla revision
"""
@bot.message_handler(regexp=r"^(Listar vehiculos|listar vehiculos|Ver vehiculos|ver vehiculos|ltv)$")
def listar_vehiculos(message):
    data = logic.obtener_vehiculos()
    table = pt.PrettyTable(['Placa', 'Marca', 'Modelo','Tipo'])
    table.align['Placa'] = 'l'
    table.align['Marca'] = 'l'
    table.align['Modelo'] = 'l'
    table.align['Tipo'] = 'l'

    for item in data:
        table.add_row([item.placa, f'{item.marca}', f'{item.modelo}',f'{item.tipo_vehiculo.nombre}'])
    bot.reply_to(message, f'<pre>{table}</pre>', parse_mode="HTML")
    
    """ markdownTable(table).setParams(row_sep = 'topbottom'
                                  , padding_width = 5, padding_weight='left').getMarkdown() """
###########################################################################################
"""
Metodo que permite listar todos los registros de la tabla revision
"""
@bot.message_handler(regexp=r"^(Listar revisiones|listar revisiones|Ver revisiones|ver revisiones|ltr)$")
def listar_revisiones(message):
    data = logic.obtener_revisiones()
    table = pt.PrettyTable(['Aceite', 'Frenos', 'Refrigerante','Direccion'])
    table.align['Aceite'] = 'l'
    table.align['Frenos'] = 'l'
    table.align['Refrigerante'] = 'l'
    table.align['Direccion'] = 'l'

    for item in data:
        table.add_row([item.nivel_aceite, f'{item.nivel_liquido_frenos}', f'{item.nivel_refrigerante}',f'{item.nivel_liquido_direccion}'])
    
    bot.reply_to(message, f'<pre>{table}</pre>', parse_mode="HTML") 
    
    """ markdownTable(table).setParams(row_sep = 'topbottom'
                                  , padding_width = 5, padding_weight='left').getMarkdown() """
    
#########################################################

@bot.message_handler(regexp=r"^(Asignar dueño|asignar dueño|ad) ([0-9]+) a ([A-Za-z0-9]+)$")
def on_asignar_duenio(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    parts = re.match(
        r"^(Asignar dueño|asignar dueño|ad) ([0-9]+) a ([A-Za-z0-9]+)$",
        message.text,
        flags=re.IGNORECASE)
    
    documento_identidad_usuario = int(parts[2])
    placa_vehiculo = parts[3]
    
    text = logic.asignar_duenio (documento_identidad_usuario, placa_vehiculo)
    
    bot.reply_to(message, text, parse_mode="Markdown")
    
    
###########################################################################################

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
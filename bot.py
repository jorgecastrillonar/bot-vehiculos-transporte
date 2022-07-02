#########################################################

from ast import Import
from statistics import mode
from config import bot
import config
from time import sleep
import re
import logic
import database.db as db
from models.Vehiculo import Vehiculo
from models.TipoVehiculo import TipoVehiculo
from telebot import types


vehiculo = Vehiculo()

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    
#########################################################

'''
Contruir teclado en pantalla
@return datos_listar Lista de elementos a mostrar
'''
def makeKeyboard(datos_listar):
    markup = types.InlineKeyboardMarkup()

    for item in datos_listar:
        markup.add(types.InlineKeyboardButton(text=item.nombre,callback_data=item.id))

    return markup

#########################################################

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    print(call.data)
    vehiculo_nuevo = logic.registrar_vehiculo(vehiculo.placa,vehiculo.marca,vehiculo.modelo,call.data)
    
    bot.reply_to(
        call.message,
        f"\U0001F4B0 Se registró el vehículo con placas: {vehiculo_nuevo.placa}, marca: {vehiculo_nuevo.marca}, modelo: {vehiculo_nuevo.modelo} y tipo vehiculo: {vehiculo_nuevo.tipo_vehiculo.nombre}" if vehiculo_nuevo is not None
        else f"El vehículo ya se encuentra registrado.") 
    
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
                     reply_markup=makeKeyboard(lista_tipo_vehiculos),
                     parse_mode='HTML')
        
    else:
        response = bot.reply_to(message, 'El modelo solo debe ser un dato numérico, ¿Cuál es el modelo del vehículo')
        bot.register_next_step_handler(response, proceso_modelo)

    
    
########################################################

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)

    bot.reply_to(message, "no entiendo")

#########################################################

if __name__ == '__main__':
    bot.polling(timeout=20)
    
#########################################################
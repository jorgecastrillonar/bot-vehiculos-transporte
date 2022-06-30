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

vehiculo = Vehiculo()

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    
#########################################################

@bot.message_handler(regexp=r"^(registrar vehículo|registrar vehiculo|rh)$")
def commando_registrar_vehiculo(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    response = bot.reply_to(message, "¿Cuál es la placa del vehiculo?")
    bot.register_next_step_handler(response, proceso_placa)

#########################################################

def proceso_placa(message):
    placa = message.text
    vehiculo.placa = placa
    
    response = bot.reply_to(message, '¿Cuál es la marca del vehículo')
    bot.register_next_step_handler(response, proceso_marca)
    
#########################################################


def proceso_marca(message):
    marca = message.text
    vehiculo.marca = marca
    
    response = bot.reply_to(message, '¿Cuál es el modelo del vehículo')
    bot.register_next_step_handler(response, proceso_modelo)
    
#########################################################

def proceso_modelo(message):
    modelo = message.text
    vehiculo.modelo = modelo
    
    control = logic.registrar_vehiculo(vehiculo.placa,vehiculo.marca,vehiculo.modelo)
    
    bot.reply_to(
        message,
        f"\U0001F4B0 Se registró el vehículo con placas: {vehiculo.placa}, marca: {vehiculo.marca} y modelo: {vehiculo.modelo}")
    
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
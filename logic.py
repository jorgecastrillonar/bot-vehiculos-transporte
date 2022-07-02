import database.db as db
from datetime import datetime
from sqlalchemy import extract
from models.TipoVehiculo import TipoVehiculo
import re
from models.Vehiculo import Vehiculo

#########################################################

'''
Almacenar un vehículo en la base de datos
@param String Placa del vehículo a registrar
@param String marca del vehículo a registrar
@param Integer modelo del vehículo a registrar
@param Integer tipo de vehículo a registrar
@return Vehiculo | None Objeto de tipo Vehiculo registrado o None si no es posible regoistrarlo
'''
def registrar_vehiculo(placa, marca="",modelo=0, tipo_vehiculo=1):
    
    vehiculo = obtener_vehiculo(placa)
    
    if vehiculo is None:
        vehiculo = Vehiculo(placa,marca,modelo,tipo_vehiculo)
        db.session.add(vehiculo)
        db.session.commit()
        return vehiculo
    else:
        return None
    
    """ if len(placa) != 6:
        print("Debe tener 6 caracteres") """
        
    """ if not modelo.isdigit():
        print("El modelo debe ser un valor numerico") """
        
    """ if not placa.isalnum():
        print("La placa solo debe contener valores alfanumericos") """    
            
#########################################################

'''
Obtiene los tipos de vehiculos registrados
@return tipos_vehiculos Lista de los tipo de vehiculos
'''
def listar_tipos_vehiculos():
    tipos_vehiculos = db.session.query(TipoVehiculo).all()
    return tipos_vehiculos

#########################################################

'''
Obtiene un vehiculo filtrado por la placa
@param String Placa del vehpiculo a buscar
@return Vehiculo | None Objeto encontrado de lo contrario se retornara None
'''
def obtener_vehiculo(placa):
    vehiculo = db.session.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    return vehiculo

#########################################################
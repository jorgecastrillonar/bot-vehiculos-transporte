import database.db as db
from datetime import datetime
from sqlalchemy import extract
from models.TipoVehiculo import TipoVehiculo
import re
from models.Vehiculo import Vehiculo


def registrar_vehiculo(placa, marca="",modelo=0, tipo_vehiculo=1):
    
    vehiculo = obtener_vehiculo(placa)
    
    if vehiculo is None:
        print("No existe y voy a crearlo")
        vehiculo = Vehiculo(placa,marca,modelo,tipo_vehiculo)
        db.session.add(vehiculo)
        db.session.commit()
        return vehiculo
    else:
        print("existo y voy a mostrar el mensaje")
        return None
    
    """ if len(placa) != 6:
        print("Debe tener 6 caracteres") """
        
    """ if not modelo.isdigit():
        print("El modelo debe ser un valor numerico") """
        
    """ if not placa.isalnum():
        print("La placa solo debe contener valores alfanumericos") """
    
            


def listar_tipos_vehiculos():
    tipos_vehiculos = db.session.query(TipoVehiculo).all()
    return tipos_vehiculos

def obtener_vehiculo(placa):
    vehiculo = db.session.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    
    return vehiculo
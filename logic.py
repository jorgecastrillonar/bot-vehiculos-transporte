import database.db as db
from datetime import datetime
from sqlalchemy import extract

from models.Vehiculo import Vehiculo


def registrar_vehiculo(placa, marca="",modelo=0):
    
    vehiculo = Vehiculo(placa,marca,modelo)
    db.session.add(vehiculo)
    db.session.commit()
    
    return True
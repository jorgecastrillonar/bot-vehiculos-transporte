from pydoc import doc
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
from models.TipoUsuario import TipoUsuario
from models.Usuario import Usuario
###################################################################################
'''
Metodo que inicia con el registro de un usuario nuevo
@param string documento documento de identidad del usuario
'''
def crear_nuevo_usuario(documento):
    usuario = Usuario(documento_identidad=documento, nombre_completo='', tipo_usuario_id='')
    db.session.add(usuario)
    db.session.commit()
#############################################################################################################
'''
Metodo que actualiza un registro en la base de datos 
para cualquier modelo 
@param object modelo Representacion del modelo a actualizar
@param array datos Representacion en arreglo llave=>valor del item a actualizar
'''
def actualizar_datos_modelo(modelo, datos):
    for llave, valor in datos.items():
        setattr(modelo, llave, valor)
    db.session.commit()
#################################################################################
'''
Obtiene el usuario que se va a terminar de registrar
@param string id identificador del usuario
@return usuario El usuario encontrado
'''
def obtener_usuario_registro(id):
    usuario = db.session.query(Usuario).get(id)
    return usuario
#################################################################################
'''
Obtiene el usuario filtrado por documento de identidad
@param string documento identificador del usuario
@return usuario El usuario encontrado
'''
def obtener_usuario_documento(documento):
    usuario = db.session.query(Usuario).filter(
        Usuario.documento_identidad == int(documento)
        ).first()
    return usuario
#################################################################################
'''
Obtiene los tipos de usuario registrados en la base de datos
@return tipo_usuario Los registros TipoUsuario encontrados.
'''
def obtener_tipo_usuario():
    tipo_usuario = db.session.query(TipoUsuario).all()
    return tipo_usuario

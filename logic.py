from pydoc import doc
import database.db as db
from sqlalchemy import extract
from datetime import datetime
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
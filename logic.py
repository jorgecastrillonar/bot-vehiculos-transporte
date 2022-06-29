import database.db as db
from sqlalchemy import extract
from datetime import datetime
from models.TipoUsuario import TipoUsuario

from models.Usuario import Usuario



def actualizar_datos_modelo(modelo, datos):
    for llave, valor in datos.items():
        setattr(modelo, llave, valor)
    db.session.commit()


#######################################################

def crear_nuevo_usuario(chatId, documento):
    usuario = Usuario(chatId, documento_identidad=documento, nombre_completo='')
    db.session.add(usuario)
    db.session.commit()
    
#####################################################
def get_help_message ():
	response = (
				"Estos son los comandos y órdenes disponibles:\n"
				"\n"
				"*/start* - Inicia la interacción con el bot (obligatorio)\n"
				"*/help* - Muestra este mensaje de ayuda\n"
				"*/about* - Muestra detalles de esta aplicación\n"
				"*gane|gané|g {cantidad}* - Registra un saldo positivo\n"
				"*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n"
				"*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
				"*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes/año\n"
				"*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
				"*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
				"*listar cuentas|lc* - Lista las cuentas registradas (sólo admin)\n"
			)

	return response


'''
Obtiene el usuario que se va a terminar de registrar
@param string id identificador del usuario
@return usuario El usuario encontrado
'''


def obtener_usuario_registro(id):
    usuario = db.session.query(Usuario).get(id)
    return usuario

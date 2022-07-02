import unittest

from database.db import Session, engine, Base

import logic
from models.Usuario import Usuario
from models.Vehiculo import Vehiculo

class TestLogic(unittest.TestCase):
    
    def setUp(self):
        self.usuario_mecanico = Usuario(documento_identidad=11111, nombre_completo='nom1', tipo_usuario_id = '1')
        self.usuario_duenio = Usuario(documento_identidad=22222, nombre_completo='nom2', tipo_usuario_id = '2')
        self.usuario_mecanico2 = Usuario(documento_identidad=33333, nombre_completo='nom3', tipo_usuario_id = '1')
        self.vehiculo = Vehiculo(placa='qaz123', marca = 'renault', modelo = 2020, tipo_vehiculo_id = '1', duenio = None, mecanico = None)
        
    def test_asignar_mecanico(self):
        usu_mecanico = logic.crear_nuevo_usuario(self.usuario_mecanico.documento_identidad, self.usuario_mecanico.nombre_completo, self.usuario_mecanico.tipo_usuario_id)
        usu_duenio = logic.crear_nuevo_usuario(self.usuario_duenio.documento_identidad, self.usuario_duenio.nombre_completo, self.usuario_duenio.tipo_usuario_id)
        usu_mecanico2 = logic.crear_nuevo_usuario(self.usuario_mecanico2.documento_identidad, self.usuario_mecanico2.nombre_completo, self.usuario_mecanico2.tipo_usuario_id)
        vehiculo = logic.registrar_vehiculo(self.vehiculo.placa, self.vehiculo.marca, self.vehiculo.modelo, self.vehiculo.tipo_vehiculo_id)
        
        # no existe el usuario con el documento 111
        self.assertEqual(logic.asignar_mecanico(111, vehiculo.placa) , 'Error al asignar mecánico')
        
        # no esta registrado el vehiculo con la placa qaz567
        self.assertEqual(logic.asignar_mecanico(usu_mecanico.documento_identidad, 'qaz567') , 'Error al asignar mecánico')
        
        # no es un usuario tipo mecanico sino tipo dueño
        self.assertEqual(logic.asignar_mecanico(usu_duenio.documento_identidad, vehiculo.placa) , 'Error al asignar mecánico')
        
        # existe usuario tipo mecanico y vehiculo
        self.assertEqual(logic.asignar_mecanico(usu_mecanico.documento_identidad, vehiculo.placa) , 'Mecánico asignado correctamente')
        
        # el vehiculo ya tiene asignado un mecánico
        self.assertEqual(logic.asignar_mecanico(usu_mecanico2.documento_identidad, vehiculo.placa) , 'El vehículo ya tiene un mecánico asignado previamente')
        
        
    def test_eliminar_datos_prueba(self):
        self.vehiculo.eliminar()
        self.usuario_mecanico.eliminar()
        self.usuario_duenio.eliminar()
        self.usuario_mecanico2.eliminar()
        self.assertEqual(0, 0)
        
        
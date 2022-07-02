import unittest

from database.db import Session, engine, Base

import logic
from models.Usuario import Usuario
from models.Vehiculo import Vehiculo

class TestLogic(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.usu_mecanico = logic.crear_nuevo_usuario(documento_identidad=11111, nombre_completo='nom1', tipo_usuario_id = '1')
        self.usu_duenio = logic.crear_nuevo_usuario(documento_identidad=22222, nombre_completo='nom2', tipo_usuario_id = '2')
        self.usu_duenio2 = logic.crear_nuevo_usuario(documento_identidad=44444, nombre_completo='nom4', tipo_usuario_id = '2')
        self.usu_mecanico2 = logic.crear_nuevo_usuario(documento_identidad=33333, nombre_completo='nom3', tipo_usuario_id = '1')
        self.vehiculo = logic.registrar_vehiculo(placa='qaz123', marca = 'renault', modelo = 2020, tipo_vehiculo_id = '1')
        
    def test_asignar_mecanico(self):
        
        # no existe el usuario con el documento 111
        self.assertEqual(logic.asignar_mecanico(111, self.vehiculo.placa) , 'Error al asignar mecánico')
        
        # no esta registrado el vehiculo con la placa qaz567
        self.assertEqual(logic.asignar_mecanico(self.usu_mecanico.documento_identidad, 'qaz567') , 'Error al asignar mecánico')
        
        # no es un usuario tipo mecanico sino tipo dueño
        self.assertEqual(logic.asignar_mecanico(self.usu_duenio.documento_identidad, self.vehiculo.placa) , 'Error al asignar mecánico')
        
        # existe usuario tipo mecanico y vehiculo
        self.assertEqual(logic.asignar_mecanico(self.usu_mecanico.documento_identidad, self.vehiculo.placa) , 'Mecánico asignado correctamente')
        
        # el vehiculo ya tiene asignado un mecánico
        self.assertEqual(logic.asignar_mecanico(self.usu_mecanico2.documento_identidad, self.vehiculo.placa) , 'El vehículo ya tiene un mecánico asignado previamente')
    
        
    def test_asignar_dueño(self):
        
        # no existe el usuario con el documento 555
        self.assertEqual(logic.asignar_duenio(555, self.vehiculo.placa) , 'Error al asignar dueño')
        
        # no esta registrado el vehiculo con la placa yyy567
        self.assertEqual(logic.asignar_duenio(self.usu_duenio.documento_identidad, 'yyy567') , 'Error al asignar dueño')
        
        # no es un usuario tipo dueño sino tipo mecanico
        self.assertEqual(logic.asignar_duenio(self.usu_mecanico.documento_identidad, self.vehiculo.placa) , 'Error al asignar dueño')
        
        # existe usuario tipo dueño y vehiculo
        self.assertEqual(logic.asignar_duenio(self.usu_duenio.documento_identidad, self.vehiculo.placa) , 'Dueño asignado correctamente')
        
        # el vehiculo ya tiene asignado un dueño
        self.assertEqual(logic.asignar_duenio(self.usu_duenio2.documento_identidad, self.vehiculo.placa) , 'El vehículo ya tiene un dueño asignado previamente')    
        
        
    def test_eliminar_datos_prueba(self):
        self.usu_mecanico.eliminar()
        self.usu_duenio.eliminar()
        self.usu_duenio2.eliminar()
        self.usu_mecanico2.eliminar()
        self.vehiculo.eliminar()
        self.assertEqual(0, 0)
        
        
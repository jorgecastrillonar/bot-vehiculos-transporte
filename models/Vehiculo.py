import database.db as db
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    __tablename__ = 'vehiculo'
     
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    placa = Column('placa', String(6), nullable=False,  unique=True)
    marca = Column('marca', String(25), nullable=False)
    modelo = Column('modelo', Integer, nullable=False)
    tipo_vehiculo_id = Column('tipo_vehiculo_id', String(15), ForeignKey('tipo_vehiculo.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    duenio_id = Column('duenio_id', String(15), ForeignKey('tipo_usuario.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    mecanico_id = Column('mecanico_id', String(15), ForeignKey('tipo_usuario.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=True)

    tipo_vehiculo = relationship('TipoVehiculo', back_populates='vehiculos')
    revisiones_vehiculos = relationship('VehiculoRevision', back_populates='vehiculo')

    
    def __init__(self, placa="", marca = "", modelo = 0, tipo_vehiculo_id = 1, duenio = None, mecanico = None):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.tipo_vehiculo_id = tipo_vehiculo_id
        self.duenio_id = duenio
        self.mecanico_id = mecanico
    
    def __repr__(self):
        return f"<Vehículo {self.placa}>"
       
    def eliminar(self):
       db.Base.metadata.create_all(db.engine)
       session = db.Session()
       session.query(Vehiculo).filter(Vehiculo.placa==self.placa).delete()
       session.commit()
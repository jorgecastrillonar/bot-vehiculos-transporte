
import database.db as db
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

class VehiculoRevision(db.Base):
    __tablename__ = 'vehiculo_revision'
     
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    vehiculo_id = Column('vehiculo_id', Integer, ForeignKey('vehiculo.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    revision_id = Column('revision_id', Integer, ForeignKey('revision.id',onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    fecha_revision = Column('fecha_revision', DateTime, server_default=func.now(), nullable=False)
  
    vehiculo = relationship('Vehiculo', back_populates='revisiones_vehiculos')
    revision = relationship('Revision', back_populates='revisiones_vehiculos')
    
    def __init__(self, vehiculo_id,revision_id):
        self.vehiculo_id = vehiculo_id
        self.revision_id = revision_id


    
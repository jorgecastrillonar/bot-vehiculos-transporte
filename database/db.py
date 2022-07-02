from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine (
  'sqlite:///database/vehiculos_transporte.sqlite',
    echo=True,
    connect_args = {'check_same_thread': False})

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()


""" 
INSERT INTO tipo_usuario (nombre, descripcion) VALUES ('Dueño', 'Dato que representa al usuario de tipo dueño');
INSERT INTO tipo_usuario (nombre, descripcion) VALUES ('Mecanico', 'Dato que representa al usuario de tipo mecanico'); """
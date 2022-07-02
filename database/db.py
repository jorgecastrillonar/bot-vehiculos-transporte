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
INSERT INTO tipo_usuario (nombre, descripcion) VALUES ('Mecanico', 'Dato que representa al usuario de tipo mecanico');

INSERT INTO tipo_vehiculo (nombre, descripcion) VALUES ('Particular', 'Dato que representa al vehiculo de tipo particular');
INSERT INTO tipo_vehiculo (nombre, descripcion) VALUES ('Microbuses', 'Dato que representa al vehiculo de tipo microbus');
INSERT INTO tipo_vehiculo (nombre, descripcion) VALUES ('Buseta', 'Dato que representa al vehiculo de tipo buseta');
"""
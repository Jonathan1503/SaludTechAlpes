from saludtech.servicio_estandarizacion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla reservas e itinerarios
proceso_estandarizacion_imagen = db.Table(
    "proceso_estandarizacion_imagen",
    db.Model.metadata,
    db.Column("proceso_estandarizacion_id", db.String, db.ForeignKey("proceso_estandarizacion.id")),
    db.Column("tipo", db.String),
    db.Column("archivo", db.String),
    db.Column("archivo_estandarizado", db.String),
    db.ForeignKeyConstraint(
        ["tipo", "archivo", "archivo_estandarizado"],
        ["imagen_estandarizada.tipo", "imagen_estandarizada.archivo", "imagen_estandarizada.archivo_estandarizado"],
    )
)

class ImagenEstandarizada(db.Model):
    __tablename__ = "imagen_estandarizada"
    tipo = db.Column(db.String, nullable=False, primary_key=True)
    archivo = db.Column(db.String, nullable=False, primary_key=True)
    archivo_estandarizado = db.Column(db.String, nullable=True, primary_key=True)


class ProcesoEstandarizacion(db.Model):
    __tablename__ = "proceso_estandarizacion"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.String, nullable=False)
    fecha_actualizacion = db.Column(db.String, nullable=False)
    id_proceso_ingestion = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False, default="PENDIENTE")
    imagenes = db.relationship('ImagenEstandarizada', secondary=proceso_estandarizacion_imagen, backref='proceso_estandarizacion')

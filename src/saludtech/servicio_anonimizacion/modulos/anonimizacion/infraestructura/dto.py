from saludtech.servicio_anonimizacion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre proceso de anonimización y datos
proceso_anonimizacion_dato = db.Table(
    "proceso_anonimizacion_dato",
    db.Model.metadata,
    db.Column("proceso_anonimizacion_id", db.String, db.ForeignKey("proceso_anonimizacion.id")),
    db.Column("tipo", db.String),
    db.Column("contenido", db.String),
    db.Column("anonimizado", db.Boolean),
    db.ForeignKeyConstraint(
        ["tipo", "contenido", "anonimizado"],
        ["dato.tipo", "dato.contenido", "dato.anonimizado"]
    )
)

class Dato(db.Model):
    __tablename__ = "dato"
    tipo = db.Column(db.String, nullable=False, primary_key=True)
    contenido = db.Column(db.String, nullable=False, primary_key=True)
    anonimizado = db.Column(db.Boolean, nullable=False, primary_key=True, default=False)

class ProcesoAnonimizacion(db.Model):
    __tablename__ = "proceso_anonimizacion"
    id = db.Column(db.String, primary_key=True)
    fecha_creacion = db.Column(db.String, nullable=False)
    fecha_actualizacion = db.Column(db.String, nullable=False)
    id_partner = db.Column(db.String, nullable=False)
    datos = db.relationship('Dato', secondary=proceso_anonimizacion_dato, backref='proceso_anonimizacion')
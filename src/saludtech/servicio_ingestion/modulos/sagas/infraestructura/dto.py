from saludtech.servicio_ingestion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()
class EventoDataLog(db.Model):
    __tablename__ = "evento_datalog"
    id = db.Column(db.String, primary_key=True)
    evento = db.Column(db.String, nullable=False)
    
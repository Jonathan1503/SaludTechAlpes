-- Tablas para el servicio de anonimizacion
CREATE TABLE IF NOT EXISTS dato (
    tipo VARCHAR(255) NOT NULL,
    contenido VARCHAR(255) NOT NULL,
    anonimizado BOOLEAN NOT NULL,
    PRIMARY KEY (tipo, contenido, anonimizado)
);

CREATE TABLE IF NOT EXISTS proceso_anonimizacion (
    id VARCHAR(255) PRIMARY KEY,
    fecha_creacion VARCHAR(255) NOT NULL,
    fecha_actualizacion VARCHAR(255) NOT NULL,
    id_partner VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS proceso_anonimizacion_dato (
    proceso_anonimizacion_id VARCHAR(255) REFERENCES proceso_anonimizacion(id),
    tipo VARCHAR(255),
    contenido VARCHAR(255),
    anonimizado BOOLEAN,
    FOREIGN KEY (tipo, contenido, anonimizado) REFERENCES dato(tipo, contenido, anonimizado),
    PRIMARY KEY (proceso_anonimizacion_id, tipo, contenido, anonimizado)
);
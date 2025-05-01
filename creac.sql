-- Tabla departamento
CREATE TABLE IF NOT EXISTS public.departamento (
    id_departamento SMALLINT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla municipio
CREATE TABLE IF NOT EXISTS public.municipio (
    id_municipio SMALLINT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_departamento SMALLINT NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
);

-- Tabla paciente
CREATE TABLE IF NOT EXISTS public.paciente (
    id_paciente SERIAL PRIMARY KEY, -- SERIAL para autoincrementar en PostgreSQL
    documento VARCHAR(20) NOT NULL,
    primer_nombre VARCHAR(20) NOT NULL,
    primer_apellido VARCHAR(20) NOT NULL,
    genero CHAR(1) CHECK (genero IN ('M', 'F')), -- Restricción de género
    fecha_nacimiento DATE NOT NULL,
    estatura NUMERIC(3, 2) CHECK (estatura BETWEEN 0 AND 3), -- Formato para estatura, ej. 1.70, 2.05, etc.
    peso NUMERIC(5, 2) CHECK (peso > 0), -- Peso en kilogramos, ej. 70.50
    id_municipio SMALLINT NOT NULL,
    fecha_registro DATE NOT NULL,
    anotaciones TEXT NOT NULL,
    FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio)
);

-- Tabla metricas_tipos
CREATE TABLE IF NOT EXISTS public.metricas_tipos (
    id_metrica SMALLINT PRIMARY KEY,
    dominio VARCHAR(50) NOT NULL, -- Ejemplo: "Presión arterial", "Frecuencia cardíaca"
    unidad_medida VARCHAR(10) NOT NULL -- Ejemplo: "bpm", "mmHg"
);

-- Tabla metrica_estados
CREATE TABLE IF NOT EXISTS public.metrica_estados (
    id_estado SMALLINT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Tabla metricas_lecturas (modificada para incluir hora)
CREATE TABLE IF NOT EXISTS public.metricas_lecturas (
    id_registro BIGSERIAL PRIMARY KEY, -- BIGSERIAL para autoincrementar
    id_paciente INT NOT NULL,
    id_metrica SMALLINT NOT NULL,
    valor NUMERIC(6, 2) NOT NULL, -- Optimizado para valores de lectura, ej. 120.75
    fecha DATE NOT NULL,          -- Fecha de la medición
    hora TIME WITHOUT TIME ZONE NOT NULL, -- Hora de la medición
    id_estado SMALLINT,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_metrica) REFERENCES metricas_tipos(id_metrica),
    FOREIGN KEY (id_estado) REFERENCES metrica_estados(id_estado)
);

-- Tabla umbrales
CREATE TABLE IF NOT EXISTS public.umbrales (
    id_umbral SMALLINT PRIMARY KEY,
    id_metrica SMALLINT NOT NULL,
    valor_min NUMERIC(6, 2), -- Umbral mínimo
    valor_max NUMERIC(6, 2), -- Umbral máximo
    FOREIGN KEY (id_metrica) REFERENCES metricas_tipos(id_metrica)
);

-- Tabla alertas
CREATE TABLE IF NOT EXISTS public.alertas (
    id_alerta BIGSERIAL PRIMARY KEY, -- BIGSERIAL para autoincrementar
    id_paciente INT NOT NULL,
    id_metrica SMALLINT NOT NULL,
    fecha TIMESTAMPTZ NOT NULL, -- TIMESTAMPTZ incluye zona horaria
    descripcion VARCHAR(255), -- Descripción de la alerta
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
    FOREIGN KEY (id_metrica) REFERENCES metricas_tipos(id_metrica)
);

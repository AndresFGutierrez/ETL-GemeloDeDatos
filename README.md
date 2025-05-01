# Proyecto ETL para Gestión de Pacientes y Métricas de Salud

Este proyecto implementa un flujo ETL para gestionar datos de pacientes y métricas de salud. Extrae datos desde una base de datos MySQL, los transforma según ciertas reglas, y los carga en PostgreSQL. Además, genera datos aleatorios para simular mediciones de salud de manera continua.

## Características

- **Extracción (Extract):** Se extraen datos de las tablas de pacientes y métricas desde MySQL.
- **Transformación (Transform):** Los datos se transforman, por ejemplo, con la normalización de género y la extracción de partes del nombre.
- **Carga (Load):** Los datos transformados se cargan en PostgreSQL para su análisis posterior.
- **Generación de datos aleatorios:** Se generan datos aleatorios de métricas de salud (como presión arterial, ritmo cardíaco, etc.) y se insertan en la base de datos PostgreSQL.
- **Ejecución continua:** El proceso ETL se ejecuta de forma repetitiva con un intervalo configurable, asegurando que los datos estén siempre actualizados.

## Requisitos

- **Python 3.x**
- **Librerías necesarias:**
  - `mysql-connector`
  - `psycopg2`
  - `random`
  - `time`
  - `datetime`

Puedes instalar las librerías necesarias utilizando `pip`:

```bash
pip install mysql-connector psycopg2
```

## Estructura de la Base de Datos

- **MySQL:**
  - `paciente`: Contiene información básica del paciente (ID, documento, nombre, género, etc.).
  - `dataorigen`: Datos no procesados relacionados con las métricas de salud.
- **PostgreSQL:**
  - `paciente`: Información de pacientes, transformada y cargada.
  - `metricas_lecturas`: Mediciones de salud de los pacientes.
  - `metricas_tipos`: Tipos de métricas (ej.: presión arterial, ritmo cardíaco).
  - `alertas`: Alertas generadas en base a las métricas de salud.

## Ejecución

1. Asegúrate de tener las bases de datos MySQL y PostgreSQL configuradas correctamente.
2. Ejecuta el script Python para iniciar el proceso ETL y generar datos aleatorios:
   ```bash
   python etl_proyecto.py
   ```
3. El proceso se ejecutará indefinidamente, generando datos y actualizando la base de datos.

¡Gracias por ver este proyecto!

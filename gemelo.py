import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import Error
import time

# Variables de conexión PostgreSQL
pg_host = "localhost"
pg_port = "5432"
pg_database = "BD_PIA"
pg_user = "postgres"
pg_password = "postgres"


# Función para generar datos aleatorios e insertarlos en la tabla `metrica_lecturas`
def generar_datos_aleatorios():
    try:
        # Conexión a PostgreSQL
        conexion_pg = psycopg2.connect(
            user=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            database=pg_database,
        )
        cursor_pg = conexion_pg.cursor()

        # Simulación de datos
        cantidad_registros = 50  # Número de registros a generar
        pacientes = [1, 2, 3, 4, 5]  # IDs de pacientes simulados
        metricas = [
            1,
            2,
            3,
            4,
            5,
        ]  # IDs de métricas (ej.: Temperatura corporal, Humedad ambiente, Ritmo cardíaco)
        estados = [1, 2, 3, 4]  # Estados posibles (ej.: normal, reposo, caminando)

        for _ in range(cantidad_registros):
            id_paciente = random.choice(pacientes)
            id_metrica = random.choice(metricas)
            valor = round(
                random.uniform(50, 150), 2
            )  # Valores aleatorios (ej.: presión o frecuencia)
            fecha = datetime.now().date()
            hora = (
                datetime.now() - timedelta(minutes=random.randint(0, 1440))
            ).time()  # Horas aleatorias del día
            id_estado = random.choice(estados)

            # Mostrar datos generados antes de la inserción
            print(
                f"Insertando fila: (id_paciente={id_paciente}, id_metrica={id_metrica}, "
                f"valor={valor}, fecha={fecha}, hora={hora}, id_estado={id_estado})"
            )
            time.sleep(0.01)  # Retraso  entre impresiones

            # Inserción en la tabla `metrica_lecturas`
            insert_pg = """
            INSERT INTO metricas_lecturas (id_paciente, id_metrica, valor, fecha, hora, id_estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor_pg.execute(
                insert_pg, (id_paciente, id_metrica, valor, fecha, hora, id_estado)
            )

        # Confirmar cambios
        conexion_pg.commit()
        print(
            f"Se generaron e insertaron {cantidad_registros} registros aleatorios en `metrica_lecturas`."
        )

    except Error as e:
        print("Error al generar datos aleatorios:", e)
    finally:
        # Cerrar conexión
        if conexion_pg:
            cursor_pg.close()
            conexion_pg.close()
            print("Conexión PostgreSQL cerrada")


# Bucle infinito para generar datos indefinidamente
if __name__ == "__main__":
    while True:
        print("Generando datos aleatorios...")
        generar_datos_aleatorios()
        print("Esperando 10 segundos antes de generar más datos...")
        time.sleep(10)  # Esperar 10 segundos antes de la siguiente iteración

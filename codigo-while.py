# Librerías y paquetes de conexión
import mysql.connector
import psycopg2
from psycopg2 import Error
import time
import sys

# Variables de conexión MySQL phpmyadmin
my_host = "localhost"
my_user = "root"
my_password = ""
my_database = "prueba"
my_port = 3307

# Variables de conexión PostgreSQL
pg_host = "localhost"
pg_port = "5432"
pg_database = "BD_PIA"
pg_user = "postgres"
pg_password = "postgres"


# Función para ejecutar el flujo ETL para la tabla `paciente`
def etl_pacientes():
    try:
        # Conexión a MySQL
        conexion_mysql = mysql.connector.connect(
            host=my_host,
            user=my_user,
            password=my_password,
            database=my_database,
            port=my_port,
        )
        cursor_mysql = conexion_mysql.cursor()

        # Conexión a PostgreSQL
        conexion_pg = psycopg2.connect(
            user=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            database=pg_database,
        )
        cursor_pg = conexion_pg.cursor()

        # 1. Extracción de datos desde MySQL
        consulta_mysql = """
        SELECT 
            IDPaciente, 
            Documento, 
            Nombres, 
            Apellidos, 
            Genero, 
            FechaNacimiento, 
            Estatura, 
            Peso, 
            FechaRegistro, 
            IdMunicipio, 
            Anotaciones
        FROM Paciente;
        """
        cursor_mysql.execute(consulta_mysql)
        datos = cursor_mysql.fetchall()

        # Revisar si hay datos para procesar
        if not datos:
            print("No hay datos nuevos para procesar.")
            return

        # 2. Transformación de datos
        datos_transformados = []
        for fila in datos:
            (
                id_paciente,
                documento,
                nombres,
                apellidos,
                genero,
                fecha_nacimiento,
                estatura,
                peso,
                fecha_registro,
                id_municipio,
                anotaciones,
            ) = fila

            # Transformar el valor de género
            if genero == 1:
                genero = "M"  # Masculino
            elif genero == 2:
                genero = "F"  # Femenino
            else:
                genero = "O"  # Otro (si aplica un valor distinto)

            primer_nombre = nombres.split(" ")[0]  # Tomar solo el primer nombre
            primer_apellido = apellidos.split(" ")[0]  # Tomar solo el primer apellido

            datos_transformados.append(
                (
                    documento,
                    primer_nombre,
                    primer_apellido,
                    genero,
                    fecha_nacimiento,
                    estatura,
                    peso,
                    id_municipio,
                    fecha_registro,
                    anotaciones,
                )
            )

        # 3. Carga de datos transformados en PostgreSQL
        insert_pg = """
        INSERT INTO paciente (
            documento, 
            primer_nombre, 
            primer_apellido, 
            genero, 
            fecha_nacimiento, 
            estatura, 
            peso, 
            id_municipio, 
            fecha_registro, 
            anotaciones
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (documento) DO NOTHING;
        """  # Ignora duplicados según el campo `documento`
        for fila in datos_transformados:
            # Mostrar fila antes de ingresar
            print(f"Insertando fila en PostgreSQL: {fila}")
            cursor_pg.execute(insert_pg, fila)

        # Confirmar cambios en PostgreSQL
        conexion_pg.commit()
        print("ETL de pacientes completado con éxito.")

    except (mysql.connector.Error, Error) as e:
        print("Error en la conexión o ejecución:", e)
    finally:
        # Cerrar conexiones
        if conexion_pg:
            cursor_pg.close()
            conexion_pg.close()
            print("Conexión PostgreSQL cerrada")
        if conexion_mysql:
            cursor_mysql.close()
            conexion_mysql.close()
            print("Conexión MySQL cerrada")


# Función para ejecutar el flujo ETL para la tabla `DataOrigen`
def etl_dataorigen():
    try:
        # Conexión a MySQL
        conexion_mysql = mysql.connector.connect(
            host=my_host,
            user=my_user,
            password=my_password,
            database=my_database,
            port=my_port,
        )
        cursor_mysql = conexion_mysql.cursor()

        # Conexión a PostgreSQL
        conexion_pg = psycopg2.connect(
            user=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port,
            database=pg_database,
        )
        cursor_pg = conexion_pg.cursor()

        # 1. Extracción de datos no procesados desde MySQL
        consulta_mysql = """
        SELECT IdData, IDPaciente, Metrica, medidaValor, FechaHora, Estado
        FROM DataOrigen
        WHERE Procesado_Y = 0;
        """
        cursor_mysql.execute(consulta_mysql)
        datos = cursor_mysql.fetchall()

        # Revisar si hay datos para procesar
        if not datos:
            print("No hay datos nuevos para procesar.")
            return

        # 2. Transformación de datos
        datos_transformados = []
        for fila in datos:
            id_data, id_paciente, id_metrica, medida_valor, fecha_hora, estado = fila

            # Validar existencia del paciente en PostgreSQL
            cursor_pg.execute(
                "SELECT 1 FROM paciente WHERE id_paciente = %s", (id_paciente,)
            )
            if cursor_pg.fetchone() is None:
                print(
                    f"Paciente con ID {id_paciente} no existe en PostgreSQL. Saltando..."
                )
                continue

            fecha = fecha_hora.date()  # Extraer solo la fecha
            hora = fecha_hora.time()  # Extraer solo la hora
            datos_transformados.append(
                (id_data, id_paciente, id_metrica, medida_valor, fecha, hora, estado)
            )

        # 3. Carga de datos transformados en PostgreSQL
        insert_pg = """
        INSERT INTO metricas_lecturas (id_paciente, id_metrica, valor, fecha, hora, id_estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        for fila in datos_transformados:
            # Mostrar fila antes de ingresar
            print(f"Insertando fila en PostgreSQL: {fila}")
            cursor_pg.execute(
                insert_pg, fila[1:]
            )  # Insertar datos transformados en PostgreSQL
            # Marcar el registro como procesado en MySQL
            update_mysql = "UPDATE DataOrigen SET Procesado_Y = 1 WHERE IdData = %s;"
            cursor_mysql.execute(update_mysql, (fila[0],))

        # Confirmar cambios en ambas bases de datos
        conexion_pg.commit()
        conexion_mysql.commit()
        print("ETL de dataorigen completado con éxito.")

    except (mysql.connector.Error, Error) as e:
        print("Error en la conexión o ejecución:", e)
    finally:
        # Cerrar conexiones
        if conexion_pg:
            cursor_pg.close()
            conexion_pg.close()
            print("Conexión PostgreSQL cerrada")
        if conexion_mysql:
            cursor_mysql.close()
            conexion_mysql.close()
            print("Conexión MySQL cerrada")


# Ejecución en bucle infinito con tiempo de espera
while True:
    print("Ejecutando ETL...")
    etl_pacientes()  # Ejecutar primero ETL de pacientes
    etl_dataorigen()  # Luego, ETL de DataOrigen
    print("Esperando 15 segundos para la siguiente ejecución...")
    time.sleep(15)  # Tiempo de espera configurable (en segundos)

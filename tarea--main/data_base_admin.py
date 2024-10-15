
import psycopg2
from psycopg2 import Error
import SecretConfig

def conectar():
    try:
        # Reemplazar con los valores de configuración de tu base de datos
        DATABASE = SecretConfig.PGDATABASE
        USER = SecretConfig.PGUSER
        PASSWORD = SecretConfig.PGPASSWORD
        HOST = SecretConfig.PGHOST
        PORT = SecretConfig.PGPORT
        
        connection = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT, sslmode='require')
        return connection
    
    except (Exception, Error) as error:
        print("Error al conectar a la base de datos:", error)
        return None
def Crear_producto(connection, id, modelo, numero_serie, defecto):
    cursor = None
    try:
        # Verificar que la conexión no sea None
        if connection is not None:
            cursor = connection.cursor()
            
            # Consulta SQL con parámetros (%s) para evitar inyección SQL
            insert_query = """
            INSERT INTO Productos (id, modelo, numero_serie, defecto)
            VALUES (%s, %s, %s, %s)
            """
            
            # Ejecutar la consulta con los valores pasados como una tupla
            cursor.execute(insert_query, (id, modelo, numero_serie, defecto))
            
            # Confirmar los cambios en la base de datos
            connection.commit()
            print("Registro insertado correctamente.")
            return True  # Indicar que la inserción fue exitosa
    
    except (Exception, psycopg2.Error) as error:
        print("Error al insertar registro:", error)
        return False  # Indicar que hubo un error en la inserción
    
    finally:
        # Cerrar el cursor y la conexión si están abiertos
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
def eliminar_producto(connection, numero_serie):
    try:
        # Crear un cursor para ejecutar la consulta
        cursor = connection.cursor()
        
        # Consulta SQL para eliminar un registro basado en el número de serie
        delete_query = """DELETE FROM productos WHERE numero_serie = %s"""
        print(f"Ejecutando consulta: {delete_query} con numero de serie: {numero_serie}")
        
        # Ejecutar la consulta
        cursor.execute(delete_query, (numero_serie,))
        
        # Confirmar los cambios en la base de datos
        connection.commit()

        # Verificar si la eliminación fue exitosa
        if cursor.rowcount > 0:
            print(f"Se eliminó {cursor.rowcount} producto(s) con número de serie: {numero_serie}")
            return True
        else:
            print(f"No se encontraron productos con número de serie: {numero_serie}")
            return False
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error al eliminar el producto de la tabla:", error)
        return False
    finally:
        if connection:
            cursor.close()

#ejemplo de uso
def main():
    # Datos del nuevo producto
    id_producto = 101
    modelo_producto = "Modelo X"
    numero_serie_producto = "NS123456789"
    defecto_producto = "Rasguño en la puerta"
    
    # Llamada a la función para crear el producto
    Crear_producto(id_producto, modelo_producto, numero_serie_producto, defecto_producto)
# Ejecutar el script
if __name__ == "__main__":
    main()
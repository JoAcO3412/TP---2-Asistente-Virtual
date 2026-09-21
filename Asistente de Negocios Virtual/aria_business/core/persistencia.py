"""Persistencia de los datos del asistente (contactos, reuniones, cartera, etc.) en JSON."""

# Importa el módulo 'json' para poder leer y escribir datos en formato JSON.
import json
# Importa el módulo 'os' (Operating System) para interactuar con el sistema de archivos (ej. ver si un archivo existe).
import os

# Define una constante global con el nombre del archivo donde se guardará toda la información.
ARCHIVO_DATOS = 'datos_negocio.json'


# Define la clase PersistenciaMixin, que se sumará al AsistenteNegocios principal.
class PersistenciaMixin:
    """Mixin con las funciones de guardado y carga de datos."""

    # Asigna la constante global como un atributo de la clase para poder usarla con 'self.ARCHIVO_DATOS'.
    ARCHIVO_DATOS = ARCHIVO_DATOS

    # MÉTODO: GUARDAR DATOS EN EL ARCHIVO
    
    def guardar_datos(self):
        # Cadena de documentación del método.
        """Guarda todos los datos del asistente en un archivo JSON."""
        
        # Crea un gran diccionario llamado 'datos' que empaqueta todas las listas y diccionarios
        # que el asistente tiene actualmente en su memoria RAM.
        datos = {
            'contactos': self.contactos,
            'reuniones': self.reuniones,
            'cartera_acciones': self.cartera_acciones,
            'clientes': self.clientes,
            'historial_busquedas': self.historial_busquedas,
        }

        # Inicia un bloque try-except por si hay problemas de permisos al intentar escribir en el disco.
        try:
            # Abre (o crea si no existe) el archivo en modo escritura ('w' de write).
            # Usa 'encoding="utf-8"' para que los acentos y las 'ñ' se guarden correctamente.
            # La sentencia 'with' asegura que el archivo se cierre automáticamente al terminar.
            with open(self.ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
                # Escribe el diccionario 'datos' en el archivo 'f'.
                # 'ensure_ascii=False' respeta los caracteres en español (no los transforma en códigos raros).
                # 'indent=2' formatea el archivo JSON con saltos de línea y sangrías para que sea legible por humanos.
                json.dump(datos, f, ensure_ascii=False, indent=2)
                
        # Si algo falla al intentar guardar (por ejemplo, el disco está lleno o bloqueado)...
        except Exception as e:
            # Imprime el error exacto en la consola para poder debugearlo.
            print(f"Error al guardar datos: {e}")

    # MÉTODO: CARGAR DATOS DESDE EL ARCHIVO
    
    def cargar_datos(self):
        """Carga los datos del asistente desde el archivo JSON, si existe."""
        
        # Inicia bloque try-except por si el archivo está corrupto o mal formateado.
        try:
            # Primero verifica si el archivo 'datos_negocio.json' realmente existe en la carpeta.
            # (Si es la primera vez que abres el programa, el archivo no existirá aún).
            if os.path.exists(self.ARCHIVO_DATOS):
                
                # Si existe, lo abre en modo lectura ('r' de read) con soporte para caracteres en español.
                with open(self.ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                    # Lee todo el contenido del JSON y lo convierte de vuelta a un diccionario de Python.
                    datos = json.load(f)
                    
                    # Extrae la información usando '.get()'.
                    # La ventaja de usar '.get("clave", {})' es que si la clave no existe en el JSON
                    # (ej. porque es una versión vieja del archivo), le asigna un diccionario {} o lista [] vacía
                    # en lugar de hacer explotar el programa con un KeyError.
                    self.contactos = datos.get('contactos', {})
                    self.reuniones = datos.get('reuniones', [])
                    self.cartera_acciones = datos.get('cartera_acciones', {})
                    self.clientes = datos.get('clientes', {})
                    self.historial_busquedas = datos.get('historial_busquedas', [])
                    
        # Si ocurre algún problema al cargar (ej. alguien modificó el JSON a mano y rompió el formato)...
        except Exception as e:
            # Imprime el mensaje de error en la consola.
            print(f"Error al cargar datos: {e}")
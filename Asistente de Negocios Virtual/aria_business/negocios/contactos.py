"""Gestión de contactos comerciales (clientes, proveedores, socios, etc.)."""

# Importamos el módulo datetime para poder registrar la fecha exacta en la que se crea un contacto.
import datetime


# Definimos la clase ContactosMixin, que se sumará al AsistenteNegocios principal.
class ContactosMixin:
    """Mixin con las funciones de gestión de contactos."""

    # MÉTODO: AGREGAR UN CONTACTO NUEVO
    
    def agregar_contacto(self, nombre: str, email: str, telefono: str, tipo: str):
        """Agrega un contacto comercial (cliente, proveedor, socio, etc.)."""
        
        # Guarda (o sobreescribe si ya existe) el contacto en el diccionario 'contactos'.
        # Utiliza el 'nombre' que ingresó el usuario como la clave principal del diccionario.
        self.contactos[nombre] = {
            # Guarda el correo electrónico.
            'email': email,
            # Guarda el número de teléfono.
            'telefono': telefono,
            # Guarda el rol del contacto (ej. "cliente" o "proveedor").
            'tipo': tipo,
            # Genera la fecha actual en el momento de crear el contacto y le da el formato Día/Mes/Año.
            'fecha_agregado': datetime.datetime.now().strftime("%d/%m/%Y")
        }
        
        # Llama al método del PersistenciaMixin para guardar el nuevo contacto en el archivo JSON inmediatamente.
        self.guardar_datos()
        
        # El asistente confirma por voz que la acción fue exitosa.
        self.hablar(f"Contacto {nombre} agregado correctamente.")
        
        # Imprime un mensaje de confirmación en la consola.
        print(f"Contacto agregado: {nombre} ({tipo})")

    # MÉTODO: LISTAR TODOS LOS CONTACTOS
    
    def listar_contactos(self):
        """Lista todos los contactos comerciales registrados."""
        
        # Verifica si el diccionario de contactos está vacío (es decir, aún no agregaste a nadie).
        if not self.contactos:
            # Avisa por voz que no hay contactos.
            self.hablar("No tienes contactos registrados.")
            # Termina la ejecución del método acá, para no imprimir tablas vacías.
            return

        # Imprime un encabezado decorativo en la consola.
        print("\n" + "="*60)
        print("CONTACTOS COMERCIALES")
        print("="*60)

        # Recorre todos los elementos del diccionario 'contactos'. 
        # 'nombre' es la clave y 'datos' es el sub-diccionario que contiene email, teléfono, etc.
        for nombre, datos in self.contactos.items():
            # Imprime el nombre del contacto.
            print(f"\n{nombre}")
            # Imprime el tipo/rol (cliente, proveedor, etc.).
            print(f"   Tipo: {datos['tipo']}")
            # Imprime el email.
            print(f"   Email: {datos['email']}")
            # Imprime el teléfono.
            print(f"   Teléfono: {datos['telefono']}")
            # Imprime la fecha en la que fue guardado en el sistema.
            print(f"   Agregado: {datos['fecha_agregado']}")

        # Imprime una línea separadora al final de la lista.
        print("="*60 + "\n")
        
        # El asistente te lee en voz alta la cantidad total de contactos que tenés (usando len()).
        self.hablar(f"Tienes {len(self.contactos)} contactos registrados")

    # MÉTODO: BUSCAR UN CONTACTO ESPECÍFICO
    
    def buscar_contacto(self, nombre: str):
        """Busca un contacto específico por nombre."""
        
        # Verifica si el nombre exacto que buscamos existe como clave en el diccionario 'contactos'.
        if nombre in self.contactos:
            # Si existe, extrae todos sus datos (email, teléfono, etc.) y los guarda en la variable 'datos'.
            datos = self.contactos[nombre]
            
            # Arma un mensaje de texto amigable con el nombre, email y teléfono.
            mensaje = f"{nombre}. Email: {datos['email']}, Teléfono: {datos['telefono']}"
            
            # El asistente dicta ese mensaje por voz.
            self.hablar(mensaje)
            
            # Retorna el diccionario con la información por si otro método del programa lo necesita.
            return datos
            
        # Si el nombre NO se encuentra en el diccionario...
        else:
            # Avisa por voz que falló la búsqueda.
            self.hablar(f"No encontré a {nombre} en tus contactos")
            
            # Retorna None (nada) indicando que la búsqueda no tuvo resultados.
            return None
# Cadenas de documentación (docstring) del módulo que explica qué contiene este archivo.
"""Funciones de utilidad y entretenimiento: fecha/hora, música, chistes y navegación web."""

# Importamos la librería estándar para manejar fechas y horas.
import datetime
# Importamos la librería estándar para abrir el navegador web por defecto del sistema.
import webbrowser

# Importamos pywhatkit, una librería de automatización, y le asignamos el alias 'kit' para escribir menos código.
import pywhatkit as kit
# Importamos pyjokes, una librería que sirve para generar chistes aleatorios.
import pyjokes


# Definimos la clase UtilidadesMixin que será heredada por tu AsistenteNegocios.
class UtilidadesMixin:
    # Breve descripción de la clase.
    """Mixin con funciones auxiliares que no son estrictamente de negocio."""

    # MÉTODO: OBTENER FECHA Y HORA
    
    def obtener_fecha_hora(self):
        # Cadena de documentación del método.
        """Informa la fecha y hora actual del sistema."""
        
        # Obtenemos la fecha y hora exactas del momento en que se ejecuta esta línea.
        ahora = datetime.datetime.now()

        # Creamos una lista con los días de la semana en español para traducir el formato numérico.
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        # Creamos una lista con los meses del año en español.
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
                 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

        # Extraemos el día de la semana (0 es lunes, 6 es domingo) y buscamos su nombre en la lista.
        dia_semana = dias_semana[ahora.weekday()]
        # Extraemos el mes actual (1 a 12), le restamos 1 porque las listas en Python empiezan en 0, y buscamos su nombre.
        mes = meses[ahora.month - 1]

        # Armamos una oración formateada con el día de la semana, el número de día, el mes y el año.
        fecha_texto = f"{dia_semana} {ahora.day} de {mes} de {ahora.year}"
        # Formateamos la hora para que se vea como Horas:Minutos:Segundos (ej. 14:30:05).
        hora_texto = ahora.strftime("%H:%M:%S")

        # Imprimimos un cuadro decorativo en la terminal con los datos obtenidos.
        print("\n" + "="*60)
        print("FECHA Y HORA ACTUAL")
        print("="*60)
        print(f"Fecha: {fecha_texto}")
        print(f"Hora: {hora_texto}")
        print("="*60 + "\n")

        # El asistente dicta por voz la fecha y la hora (acá formatea la hora sin los segundos para que suene más natural).
        self.hablar(f"Hoy es {fecha_texto} y son las {ahora.strftime('%H:%M')}")

        # Retorna un diccionario con los datos por si algún otro método del asistente los necesita.
        return {'fecha': fecha_texto, 'hora': hora_texto}

    # MÉTODO: REPRODUCIR CANCIÓN EN YOUTUBE
    
    def reproducir_cancion(self, cancion: str):
        # Cadena de documentación.
        """Busca y reproduce una canción en YouTube usando pywhatkit."""
        
        # Validación de seguridad: si el string 'cancion' llega vacío, avisa y cancela la acción.
        if not cancion:
            self.hablar("No indicaste ninguna canción para reproducir")
            return

        # Iniciamos un bloque try-except para evitar que el programa falle si no hay internet o el navegador no abre.
        try:
            # El asistente avisa por voz y por consola lo que está a punto de hacer.
            self.hablar(f"Reproduciendo {cancion} en YouTube...")
            print(f"\nReproduciendo: {cancion}\n")

            # Usamos la función playonyt de pywhatkit (kit) que abre el navegador, busca la canción y le da play.
            kit.playonyt(cancion)

        # Si ocurre cualquier error técnico, lo capturamos en la variable 'e'.
        except Exception as e:
            # El asistente nos avisa por voz que falló y nos da el detalle técnico del error.
            self.hablar(f"Error al reproducir la canción: {str(e)}")

    # MÉTODO: CONTAR UN CHISTE
    
    def contar_chiste(self):
        # Cadena de documentación.
        """Cuenta un chiste aleatorio usando pyjokes para relajar el ambiente laboral."""
        
        try:
            # Intenta obtener un chiste de la base de datos de pyjokes especificando idioma español y categoría neutral.
            chiste = pyjokes.get_joke(language='es', category='neutral')
        except Exception:
            # Si el idioma español no está disponible en la versión instalada o hay un fallo,
            # recurre al chiste por defecto (que suele ser en inglés sobre programación).
            chiste = pyjokes.get_joke()

        # Imprime el chiste en la consola con un formato limpio.
        print("\n" + "="*60)
        print("CHISTE DEL DÍA")
        print("="*60)
        print(chiste)
        print("="*60 + "\n")

        # El asistente lo lee en voz alta.
        self.hablar(chiste)

    # MÉTODO: ABRIR SITIO WEB
    
    def abrir_sitio_web(self, sitio: str):
        # Cadena de documentación.
        """Abre un sitio web en el navegador predeterminado."""
        
        # Validación: si la variable 'sitio' está vacía, cancela la acción y avisa.
        if not sitio:
            self.hablar("No indicaste ningún sitio web para abrir")
            return

        try:
            # Comprueba si el texto que ingresó el usuario NO empieza con "http://" o "https://".
            if not sitio.startswith(('http://', 'https://')):
                # Si no lo tiene, se lo agrega automáticamente al principio para formar un enlace válido.
                sitio = f"https://{sitio}"

            # Avisa por voz y consola que está procediendo a abrir la página.
            self.hablar(f"Abriendo {sitio}...")
            print(f"\nAbriendo sitio web: {sitio}\n")

            # Usa el módulo estándar webbrowser para abrir el enlace en tu navegador predeterminado (Chrome, Edge, etc.).
            webbrowser.open(sitio)

        # Si algo falla (ej. el sistema operativo bloquea la acción), captura el error.
        except Exception as e:
            # Avisa del error por voz.
            self.hablar(f"Error al abrir el sitio web: {str(e)}")
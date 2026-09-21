"""Configuración y manejo de voz: síntesis (texto → voz) y reconocimiento (voz → texto)."""

# Importa 'Optional' de la librería typing para indicar que una función puede devolver un texto (str) o nada (None).
from typing import Optional

# Importa pyttsx3, la librería principal para convertir texto a voz (Text-to-Speech) de forma offline.
import pyttsx3


# Define la clase VozMixin, que le dará capacidades de habla y escucha al AsistenteNegocios principal.
class VozMixin:
    """Mixin con las capacidades de voz del asistente."""

    # MÉTODO: CONFIGURAR MOTOR DE VOZ
    
    def configurar_engine(self):
        """
        Detecta y guarda la voz preferida (no reutiliza el motor).

        pyttsx3 (driver SAPI5 de Windows) tiene un problema conocido: si se
        reutiliza el mismo objeto "engine" para hablar varias veces seguidas,
        después de la primera vez deja de responder sin dar error. Por eso
        acá solo se detecta y se guarda el ID de la voz elegida, y luego
        `hablar()` crea un motor nuevo cada vez que necesita hablar.
        """
        
        # Inicializa la variable que guardará el ID de la voz seleccionada.
        self.voz_id = None

        # Inicia bloque try-except para manejar errores al consultar las voces del sistema.
        try:
            # Obtiene la lista de todas las voces instaladas en tu sistema operativo.
            voices = self.engine.getProperty('voices')

            # Lista de nombres comunes de voces masculinas en español e inglés.
            nombres_masculinos = ['David', 'Jorge', 'Pablo', 'Mark', 'Raúl', 'Raul']
            
            # Recorre una por una las voces instaladas en tu PC.
            for voice in voices:
                # Si el nombre de la voz contiene alguno de los nombres de la lista, o la palabra 'male'...
                if any(n in voice.name for n in nombres_masculinos) or 'male' in voice.name.lower():
                    # Guarda el ID de esa voz específica para usarla más adelante.
                    self.voz_id = voice.id
                    # Imprime en consola qué voz se seleccionó automáticamente.
                    print(f"Usando voz: {voice.name}")
                    # Rompe el ciclo 'for' porque ya encontramos una voz adecuada.
                    break

            # Si terminó el ciclo y no encontró ninguna voz masculina, pero hay voces disponibles...
            if not self.voz_id and len(voices) > 0:
                # Usa por defecto la primera voz de la lista (voices[0]).
                self.voz_id = voices[0].id

        # Si falla la lectura de propiedades de voz...
        except Exception as e:
            # Imprime el error sin detener el programa.
            print(f"   [No se pudo configurar la voz: {e}]")

        # El bloque 'finally' se ejecuta SIEMPRE, haya habido error o no.
        finally:
            # El engine inicial ya no se necesita (porque cada hablar() crea el suyo).
            try:
                # Intenta detener y cerrar el motor inicial.
                self.engine.stop()
            except Exception:
                # Si da error al detenerlo, lo ignora (pass) silenciosamente.
                pass

    # MÉTODO: HABLAR (TEXTO A VOZ)
    
    def hablar(self, texto: str):
        """Convierte texto a voz y lo reproduce, usando un motor nuevo cada vez."""
        
        # Siempre imprime en la consola lo que el asistente va a decir (útil si estás sin sonido).
        print(f"[{self.nombre}]: {texto}")
        
        # Inicia bloque try-except para evitar bloqueos del programa si falla el audio.
        try:
            # ¡La clave del éxito! Crea una instancia NUEVA del motor de voz para evitar el bug de Windows.
            engine = pyttsx3.init()
            # Ajusta la velocidad de lectura (rate) a 120 palabras por minuto.
            engine.setProperty('rate', 120)
            # Ajusta el volumen al máximo (1.0).
            engine.setProperty('volume', 1.0)
            
            # Si se había guardado un ID de voz previamente...
            if getattr(self, 'voz_id', None):
                # ...le asigna esa voz específica al nuevo motor.
                engine.setProperty('voice', self.voz_id)

            # Le ordena al motor que procese el texto.
            engine.say(texto)
            # Ejecuta la acción de hablar y espera a que termine de decir la última palabra.
            engine.runAndWait()
            # Detiene y limpia este motor temporal.
            engine.stop()
            
        # Captura errores del motor de audio (ej. dispositivo de salida desconectado).
        except Exception as e:
            print(f"   [Error de voz: {e}]")

    # MÉTODO: ESCUCHAR (VOZ A TEXTO)
    
    # El método retorna un string (texto) o None si no entendió nada. El timeout por defecto es 10 segundos.
    def escuchar(self, timeout: int = 10) -> Optional[str]:
        """
        Escucha el micrófono y convierte voz a texto.

        Args:
            timeout: Tiempo máximo de escucha.

        Returns:
            Texto reconocido en minúsculas, o None si hubo un error.
        """
        
        # Importa la librería acá adentro para asegurarse de que se carga en el momento de uso.
        import speech_recognition as sr

        # Inicia bloque general de manejo de excepciones del micrófono.
        try:
            # Abre el micrófono predeterminado del sistema operativo como origen de audio (source).
            # Usa 'with' para asegurarse de que el micrófono se apague/libere al terminar.
            with sr.Microphone() as source:
                # Avisa visualmente que está listo para recibir tu comando.
                print("[Sistema]: Escuchando...")
                
                # Escucha el ruido de fondo durante medio segundo (0.5) para calibrar y eliminar el ruido ambiente.
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Graba el audio hasta que dejes de hablar, con un tiempo límite máximo (timeout).
                audio = self.recognizer.listen(source, timeout=timeout)

            # Inicia un sub-bloque try-except específico para el reconocimiento con Google.
            try:
                # Envía el audio grabado a los servidores de Google para que lo transcriba a texto, indicando que hablamos español.
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                # Imprime lo que Google entendió en la consola.
                print(f"[Usuario]: {texto}")
                # Devuelve el texto convertido totalmente a minúsculas (.lower()) para facilitar los comandos.
                return texto.lower()
                
            # Excepción: Google procesó el audio pero no pudo entender ninguna palabra (murmullos, ruido).
            except sr.UnknownValueError:
                # El asistente avisa por voz que no comprendió.
                self.hablar("No entendí. Repite por favor.")
                return None
                
            # Excepción: No hay conexión a internet, o la API de Google rechazó la petición.
            except sr.RequestError:
                # El asistente avisa que hay un problema de red.
                self.hablar("Error de conexión. Verifica tu internet.")
                return None

        # Excepción: Pasaron los 10 segundos (timeout) y el usuario no dijo nada.
        except sr.WaitTimeoutError:
            print("[Sistema]: No se detectó ningún audio, sigo escuchando.")
            return None
            
        # Atrapa cualquier otro error catastrófico con el hardware de sonido.
        except Exception as e:
            print(f"Error: {e}")
            return None
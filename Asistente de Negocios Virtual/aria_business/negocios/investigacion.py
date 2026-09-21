"""Investigación de empresas e industrias usando Wikipedia."""

# Importa la librería 'wikipedia' para poder hacer consultas directamente a la enciclopedia libre.
import wikipedia


# Define la clase InvestigacionMixin, que agregará estas capacidades de búsqueda al asistente principal.
class InvestigacionMixin:
    """Mixin con las funciones de investigación empresarial."""

    # MÉTODO: INVESTIGAR UNA EMPRESA
    
    def investigar_empresa(self, nombre_empresa: str):
        """Busca información resumida sobre una empresa (vía Wikipedia)."""
        
        # Inicia un bloque try-except. Es fundamental aquí porque la búsqueda en Wikipedia
        # requiere internet y el artículo solicitado podría no existir, lo que causaría un error.
        try:
            # Configura el idioma de las búsquedas de Wikipedia en español ("es").
            wikipedia.set_lang("es")
            
            # Busca un resumen del artículo correspondiente al 'nombre_empresa'.
            # El parámetro 'sentences=4' limita el resultado a las primeras 4 oraciones del artículo,
            # para que el asistente no lea un texto interminable.
            resultado = wikipedia.summary(nombre_empresa, sentences=4)
            
            # El asistente lee en voz alta el resumen obtenido.
            self.hablar(f"Información sobre {nombre_empresa}: {resultado}")
            
            # Imprime el texto del resumen en la consola para poder leerlo.
            print(f"\n[Empresa]: {resultado}\n")
            
        # Si la empresa no se encuentra en Wikipedia, hay múltiples resultados ambiguos o falla internet...
        except Exception:
            # Captura el error y el asistente avisa por voz que no pudo conseguir la información.
            self.hablar(f"No encontré información sobre {nombre_empresa}")

    # MÉTODO: INVESTIGAR UNA INDUSTRIA O SECTOR
    
    def investigar_industria(self, industria: str):
        # Cadena de documentación del método.
        """Investiga una industria o sector específico (vía Wikipedia)."""
        
        # Inicia el bloque de protección contra errores.
        try:
            # Nuevamente, asegura que el idioma de búsqueda sea español.
            wikipedia.set_lang("es")
            
            # Busca el artículo relacionado con la 'industria' (ej. "Inteligencia artificial", "Minería").
            # Vuelve a limitar el texto a solo 4 oraciones de resumen.
            resultado = wikipedia.summary(industria, sentences=4)
            
            # El asistente lee el resumen en voz alta.
            self.hablar(f"Información de {industria}: {resultado}")
            
            # Imprime el resumen en la consola.
            print(f"\n[Industria]: {resultado}\n")
            
        # Si ocurre un error (no se encuentra el tema, desconexión, etc.)...
        except Exception:
            # El asistente comunica que falló la búsqueda para esa industria en particular.
            self.hablar(f"No encontré información sobre la industria {industria}")
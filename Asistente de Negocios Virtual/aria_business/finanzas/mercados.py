"""Índices bursátiles principales y análisis de sectores de mercado."""

# Importa la librería Yahoo Finance y le asigna el alias 'yf'.
import yfinance as yf

# Define un diccionario constante con los principales índices bursátiles del mundo.
# La clave es un nombre simple (fácil de decir), y el valor es una tupla: (Nombre formal, Símbolo en Yahoo Finance).
# Nota: Los símbolos de índices en Yahoo Finance suelen empezar con el acento circunflejo (^).
INDICES = {
    'sp500': ('S&P 500', '^GSPC'),
    'nasdaq': ('NASDAQ', '^IXIC'),
    'dow': ('Dow Jones', '^DJI'),
    'ibex': ('IBEX 35', '^IBEX'),
    'dax': ('DAX', '^GDAXI'),
    'ftse': ('FTSE 100', '^FTSE'),
    'nikkei': ('Nikkei 225', '^N225'),
}

# Define un diccionario constante que agrupa los símbolos de las empresas más importantes por sector.
SECTORES = {
    'tecnología': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA'],
    'bancario': ['JPM', 'BAC', 'WFC', 'GS'],
    'salud': ['UNH', 'JNJ', 'PFE', 'ABBV'],
    'energía': ['XOM', 'CVX', 'SLB', 'MPC'],
    'retail': ['AMZN', 'WMT', 'TM', 'TSLA'],
    'bienes de consumo': ['KO', 'PEP', 'MCD', 'NKE'],
}


# Define la clase MercadosMixin, diseñada para integrarse al AsistenteNegocios principal.
class MercadosMixin:
    """Mixin con las funciones de índices bursátiles y sectores."""

    # Asigna los diccionarios globales como variables de clase para que los métodos puedan acceder a ellos usando 'self'.
    INDICES = INDICES
    SECTORES = SECTORES

    # MÉTODO: OBTENER UN ÍNDICE ESPECÍFICO
    
    def obtener_indice_mercado(self, indice: str):
        """Obtiene información de un índice bursátil específico."""
        
        # Busca el índice ingresado en el diccionario (convirtiéndolo a minúsculas).
        # Si NO lo encuentra, usa un valor por defecto: devuelve el mismo texto en mayúsculas como nombre y como símbolo.
        nombre_indice, simbolo = self.INDICES.get(indice.lower(), (indice.upper(), indice.upper()))

        # Inicia bloque try-except para manejar fallos de red o símbolos inexistentes.
        try:
            # El asistente avisa por voz que está consultando el índice.
            self.hablar(f"Consultando índice {nombre_indice}...")
            
            # Crea el objeto Ticker con el símbolo del índice.
            indice_data = yf.Ticker(simbolo)
            # Descarga el historial de precios del último día ('1d').
            datos = indice_data.history(period='1d')

            # Si la descarga devuelve una tabla vacía (no hay datos o el símbolo no existe)...
            if datos.empty:
                self.hablar(f"No encontré información del índice {nombre_indice}")
                # Termina la ejecución del método.
                return

            # Extrae el precio de cierre más reciente (.iloc[-1]).
            precio = datos['Close'].iloc[-1]
            
            # Imprime el resultado en consola.
            print(f"\n[{nombre_indice}]: {precio:.2f}\n")
            
            # El asistente dicta por voz el valor actual del índice.
            self.hablar(f"El índice {nombre_indice} está en {precio:.2f}")

        # Atrapa cualquier otro error inesperado.
        except Exception as e:
            self.hablar(f"Error al consultar índice: {str(e)}")

    # MÉTODO: OBTENER TODOS LOS ÍNDICES PRINCIPALES
    
    def obtener_indices_principales(self):
        """Obtiene y muestra los principales índices bursátiles mundiales."""
        
        # Imprime el encabezado decorativo en la consola.
        print("\n" + "="*60)
        print("ÍNDICES BURSÁTILES PRINCIPALES")
        print("="*60 + "\n")

        # Avisa por voz que va a iniciar la consulta masiva.
        self.hablar("Consultando índices principales...")

        # Recorre cada elemento del diccionario INDICES. Ignora las claves y toma los valores (tuplas de nombre y símbolo).
        for nombre, simbolo in self.INDICES.values():
            try:
                # Crea el Ticker y descarga el historial de 1 día para el índice actual.
                indice_data = yf.Ticker(simbolo)
                datos = indice_data.history(period='1d')
                
                # Si los datos NO están vacíos...
                if not datos.empty:
                    # Extrae el precio actual.
                    precio = datos['Close'].iloc[-1]
                    # Imprime el nombre del índice y su valor.
                    print(f"{nombre}: {precio:.2f}")
            
            # Si hay un error con UN índice en particular (ej. feriado en ese país), lo atrapa pero el bucle 'for' continúa.
            except Exception:
                print(f"{nombre}: [sin datos disponibles]")

        # Imprime la línea final decorativa.
        print("\n" + "="*60 + "\n")
        
        # Confirma por voz que terminó la consulta.
        self.hablar("Índices consultados")

    # MÉTODO: ANALIZAR UN SECTOR DE MERCADO
    
    def analizar_sector(self, sector: str):
        """Analiza un sector específico a partir de sus principales acciones."""
        
        # Busca el sector en el diccionario (en minúsculas). Si no existe, devuelve una lista vacía [].
        simbolos = self.SECTORES.get(sector.lower(), [])

        # Si la lista de símbolos quedó vacía (es decir, el sector no existe en el diccionario)...
        if not simbolos:
            # Obtiene todas las claves del diccionario de sectores y las une separadas por coma.
            sectores_disponibles = ", ".join(self.SECTORES.keys())
            
            # Avisa por voz que hubo un error.
            self.hablar(f"Sector {sector} no encontrado")
            # Muestra en consola cuáles son los sectores válidos que se pueden consultar.
            print(f"Sectores disponibles: {sectores_disponibles}")
            # Finaliza la ejecución del método.
            return

        # Imprime el encabezado en consola con el nombre del sector en mayúsculas (.upper()).
        print("\n" + "="*60)
        print(f"ANÁLISIS SECTOR: {sector.upper()}")
        print("="*60 + "\n")

        # Avisa por voz el inicio del análisis.
        self.hablar(f"Analizando sector {sector}...")

        # Crea un diccionario vacío para ir guardando el precio de cada acción de ese sector.
        precios = {}
        
        # Recorre solo los primeros 5 símbolos de la lista ([:5]) para no demorar demasiado la consulta.
        for simbolo in simbolos[:5]:
            try:
                # Consulta la API para cada símbolo.
                accion = yf.Ticker(simbolo)
                datos = accion.history(period='1d')
                
                # Si se obtienen datos correctamente...
                if not datos.empty:
                    # Extrae el precio.
                    precio = datos['Close'].iloc[-1]
                    # Lo guarda en el diccionario 'precios' usando el símbolo como clave.
                    precios[simbolo] = precio
                    # Imprime el precio de esa acción en la consola.
                    print(f"{simbolo}: ${precio:.2f}")
            
            # Si falla la consulta de una acción específica, imprime un mensaje de error y sigue con la próxima.
            except Exception:
                print(f"{simbolo}: [sin datos disponibles]")

        # Imprime línea separadora.
        print("\n" + "="*60 + "\n")

        # Verifica que se hayan podido obtener precios de al menos algunas empresas.
        if precios:
            # Calcula el precio promedio del sector: suma de todos los precios dividida por la cantidad de acciones consultadas.
            promedio = sum(precios.values()) / len(precios)
            # El asistente dicta por voz el precio promedio calculado.
            self.hablar(f"Precio promedio del sector: ${promedio:.2f}")
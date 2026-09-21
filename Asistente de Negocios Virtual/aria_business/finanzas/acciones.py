"""Análisis financiero: precio, comparación e historial de acciones."""

# Importa el módulo datetime para registrar en qué momento se hacen las búsquedas.
import datetime

# Importa la librería de Yahoo Finance y le asigna el alias 'yf'.
import yfinance as yf


# Define la clase AccionesMixin que se unirá al asistente principal.
class AccionesMixin:
    """Mixin con las funciones de análisis de acciones individuales y múltiples."""

    # MÉTODO: OBTENER PRECIO DE UNA ACCIÓN
    
    def obtener_precio_accion(self, simbolo: str):
        """Obtiene precio actual y datos fundamentales de una acción."""
        
        # Bloque try-except para manejar errores de conexión o símbolos inválidos.
        try:
            # El asistente avisa por voz que está buscando la información.
            self.hablar(f"Consultando precio de {simbolo}...")
            
            # Crea un objeto 'Ticker' de Yahoo Finance con el símbolo ingresado (ej. AAPL).
            accion = yf.Ticker(simbolo)
            # Descarga el historial de precios del último día ('1d').
            datos = accion.history(period='1d')

            # Si la tabla de datos está vacía (el símbolo no existe en la bolsa)...
            if datos.empty:
                self.hablar(f"No encontré información para {simbolo}")
                return None

            # Obtiene el precio de cierre ('Close') del último registro disponible (.iloc[-1]).
            precio = datos['Close'].iloc[-1]
            
            # Obtiene un diccionario con toda la información fundamental de la empresa.
            info = accion.info
            # Extrae el nombre largo de la empresa. Si no lo encuentra, usa el símbolo por defecto.
            empresa = info.get('longName', simbolo)
            # Extrae el sector al que pertenece. Si no hay dato, pone 'N/A'.
            sector = info.get('sector', 'N/A')
            # Extrae el P/E Ratio (Relación Precio/Beneficio).
            pe_ratio = info.get('trailingPE', 'N/A')
            # Extrae el porcentaje de dividendos que paga.
            dividendo = info.get('dividendYield', 'N/A')
            # Extrae la capitalización de mercado (cuánto vale la empresa entera).
            market_cap = info.get('marketCap', 'N/A')

            # Imprime un reporte limpio en la consola.
            print(f"\n{'='*60}")
            print(f"ANÁLISIS DE {simbolo}")
            print(f"{'='*60}")
            print(f"Empresa: {empresa}")
            print(f"Precio: ${precio:.2f}")
            print(f"Sector: {sector}")
            print(f"P/E Ratio: {pe_ratio}")
            print(f"Dividendo: {dividendo}")
            print(f"Market Cap: {market_cap}")
            print(f"{'='*60}\n")

            # El asistente dicta un resumen por voz.
            self.hablar(f"{empresa} está a ${precio:.2f}. Sector: {sector}")

            # Agrega esta búsqueda al historial interno del asistente (usando datetime para la hora exacta).
            self.historial_busquedas.append({
                'simbolo': simbolo,
                'precio': precio,
                'fecha': datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            # Guarda los datos en el archivo JSON llamando al método del PersistenciaMixin.
            self.guardar_datos()

            # Retorna un diccionario con los datos básicos por si otro método los necesita.
            return {'simbolo': simbolo, 'precio': precio, 'empresa': empresa}

        # Captura cualquier error técnico (ej. falta de internet).
        except Exception as e:
            self.hablar(f"Error al consultar acción: {str(e)}")
            return None

    # MÉTODO: ANALIZAR MÚLTIPLES ACCIONES
    
    def analizar_multiples_acciones(self):
        """Analiza y compara un grupo de acciones ingresadas por el usuario."""
        
        # Imprime encabezado.
        print("\n" + "="*60)
        print("ANÁLISIS DE MÚLTIPLES ACCIONES")
        print("="*60)

        # Pregunta al usuario cuántas acciones quiere analizar.
        self.hablar("¿Cuántas acciones deseas analizar?")
        try:
            # Convierte la entrada del usuario a un número entero (int).
            cantidad = int(input("[Tú]: Cantidad: "))
        # Si el usuario escribe letras en vez de un número...
        except ValueError:
            self.hablar("Error en la entrada")
            return

        # Crea una lista vacía para guardar los símbolos que ingrese el usuario.
        simbolos = []
        # Inicia un bucle que se repite tantas veces como 'cantidad' indicó el usuario.
        for i in range(cantidad):
            # Pide el símbolo, quita espacios (.strip()) y lo pasa a mayúsculas (.upper()).
            simbolo = input(f"[Tú]: Acción {i + 1} (símbolo): ").strip().upper()
            if simbolo:
                # Si el usuario ingresó algo, lo añade a la lista.
                simbolos.append(simbolo)

        # Diccionario para guardar los resultados de cada acción.
        datos_acciones = {}
        print("\n" + "="*60)
        print("COMPARATIVA DE ACCIONES")
        print("="*60 + "\n")

        # Recorre cada símbolo que el usuario guardó en la lista.
        for simbolo in simbolos:
            try:
                # Consulta la API de Yahoo Finance para ese símbolo.
                accion = yf.Ticker(simbolo)
                datos = accion.history(period='1d')
                info = accion.info

                # Si trajo datos válidos...
                if not datos.empty:
                    # Extrae precio, nombre y P/E ratio.
                    precio = datos['Close'].iloc[-1]
                    empresa = info.get('longName', simbolo)
                    pe_ratio = info.get('trailingPE', 'N/A')

                    # Guarda esta info en el diccionario, usando el símbolo como clave.
                    datos_acciones[simbolo] = {
                        'empresa': empresa,
                        'precio': precio,
                        'pe_ratio': pe_ratio
                    }

                    # Imprime los datos de esta acción en la consola.
                    print(f"{simbolo} ({empresa})")
                    print(f"  Precio: ${precio:.2f}")
                    print(f"  P/E: {pe_ratio}\n")
            # Si una de las acciones de la lista falla, atrapa el error pero continúa con las demás.
            except Exception:
                print(f"  [No se pudo obtener información de {simbolo}]\n")

        print("="*60 + "\n")

        # Si se logró obtener datos de al menos una acción...
        if datos_acciones:
            # Extrae solo los precios en una lista nueva usando "List Comprehension".
            precios = [d['precio'] for d in datos_acciones.values()]
            # Encuentra el valor más bajo de la lista.
            min_precio = min(precios)
            # Encuentra el valor más alto de la lista.
            max_precio = max(precios)
            # Dicta un resumen indicando los extremos de precios.
            self.hablar(f"Precio mínimo: ${min_precio:.2f}. Precio máximo: ${max_precio:.2f}")

    # MÉTODO: COMPARAR DOS ACCIONES
    
    def comparar_acciones(self, simbolo1: str, simbolo2: str):
        """Compara dos acciones entre sí, incluyendo precio y P/E ratio."""
        
        # Imprime encabezado con los dos símbolos a comparar.
        print("\n" + "="*60)
        print(f"COMPARATIVA: {simbolo1} vs {simbolo2}")
        print("="*60 + "\n")

        try:
            self.hablar(f"Comparando {simbolo1} con {simbolo2}...")

            # Crea objetos Ticker para ambas acciones.
            accion1 = yf.Ticker(simbolo1)
            accion2 = yf.Ticker(simbolo2)

            # Obtiene el historial del último día para ambas.
            datos1 = accion1.history(period='1d')
            datos2 = accion2.history(period='1d')

            # Si alguna de las dos no existe o no tiene datos, cancela la comparación.
            if datos1.empty or datos2.empty:
                self.hablar("No se encontraron datos para una de las dos acciones")
                return

            # Extrae los precios de cierre.
            precio1 = datos1['Close'].iloc[-1]
            precio2 = datos2['Close'].iloc[-1]

            # Extrae los P/E ratios.
            pe1 = accion1.info.get('trailingPE', 'N/A')
            pe2 = accion2.info.get('trailingPE', 'N/A')

            # Muestra en consola la información de la primera empresa.
            print(f"{simbolo1}")
            print(f"  Precio: ${precio1:.2f}")
            print(f"  P/E: {pe1}\n")

            # Muestra en consola la información de la segunda empresa.
            print(f"{simbolo2}")
            print(f"  Precio: ${precio2:.2f}")
            print(f"  P/E: {pe2}\n")

            # Calcula la diferencia absoluta de precio entre ambas (siempre positiva gracias a abs()).
            diferencia = abs(precio1 - precio2)
            # Calcula en qué porcentaje es más cara una respecto de la otra (basado en el precio de la más barata).
            porcentaje = (diferencia / min(precio1, precio2)) * 100 if min(precio1, precio2) else 0

            # Evalúa cuál es la más cara y genera el mensaje correspondiente.
            if precio1 > precio2:
                print(f"{simbolo1} es {porcentaje:.2f}% más cara")
                self.hablar(f"{simbolo1} es {porcentaje:.2f} por ciento más cara que {simbolo2}")
            else:
                print(f"{simbolo2} es {porcentaje:.2f}% más cara")
                self.hablar(f"{simbolo2} es {porcentaje:.2f} por ciento más cara que {simbolo1}")

            print("\n" + "="*60 + "\n")

        except Exception as e:
            self.hablar(f"Error al comparar acciones: {str(e)}")

    # MÉTODO: OBTENER HISTORIAL DE UNA ACCIÓN
    
    def obtener_historial_precio(self, simbolo: str, periodo: str = '1mo'):
        """Obtiene el historial de precio de una acción para un período dado."""
        
        # Define una lista con los códigos de períodos aceptados por Yahoo Finance.
        periodos_validos = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y']
        
        # Si el usuario ingresó un período raro, se fuerza a que use 1 mes ('1mo') por defecto.
        if periodo not in periodos_validos:
            periodo = '1mo'

        try:
            self.hablar(f"Obteniendo historial de {simbolo}...")
            
            # Crea el ticker y baja la información histórica del período solicitado.
            accion = yf.Ticker(simbolo)
            datos = accion.history(period=periodo)

            # Si no hay datos (ej. un fin de semana en '1d' o símbolo incorrecto).
            if datos.empty:
                self.hablar("No hay datos disponibles")
                return

            # Extrae el precio de cierre del PRIMER día de ese período (.iloc[0]).
            precio_inicial = datos['Close'].iloc[0]
            # Extrae el precio de cierre del ÚLTIMO día de ese período (.iloc[-1]).
            precio_final = datos['Close'].iloc[-1]
            # Encuentra el precio más alto que tuvo en todo ese lapso.
            precio_maximo = datos['Close'].max()
            # Encuentra el precio más bajo que tuvo en todo ese lapso.
            precio_minimo = datos['Close'].min()

            # Calcula la diferencia en dólares/pesos.
            cambio = precio_final - precio_inicial
            # Calcula el porcentaje de rendimiento (positivo o negativo).
            porcentaje_cambio = (cambio / precio_inicial) * 100 if precio_inicial else 0

            # Imprime el reporte detallado del rendimiento en la consola.
            print("\n" + "="*60)
            print(f"HISTORIAL: {simbolo} ({periodo})")
            print("="*60)
            print(f"Precio inicial: ${precio_inicial:.2f}")
            print(f"Precio final: ${precio_final:.2f}")
            print(f"Máximo: ${precio_maximo:.2f}")
            print(f"Mínimo: ${precio_minimo:.2f}")
            print(f"Cambio: ${cambio:.2f} ({porcentaje_cambio:.2f}%)")
            print("="*60 + "\n")

            # Dicta por voz el porcentaje de cambio obtenido.
            self.hablar(f"En {periodo}, cambio de {porcentaje_cambio:.2f} por ciento")

        except Exception as e:
            self.hablar(f"Error al obtener historial: {str(e)}")
"""Gestión y análisis de la cartera de inversiones persistente del usuario."""

# Importa la librería de Yahoo Finance y le asigna el alias 'yf'.
import yfinance as yf


# Define la clase CarteraMixin, que se integrará en el AsistenteNegocios principal.
class CarteraMixin:
    """Mixin con las funciones de cartera de inversiones."""
    
    # MÉTODO: AGREGAR POSICIÓN A LA CARTERA
    
    def agregar_posicion_cartera(self, simbolo: str, cantidad: float, precio_compra: float):
        """Agrega o actualiza una posición en la cartera de inversiones persistente."""
        
        # Guarda (o actualiza si ya existía) la información de la acción en el diccionario 'cartera_acciones'.
        # Usa el símbolo de la acción (ej. 'AAPL') como clave del diccionario.
        self.cartera_acciones[simbolo] = {
            # Guarda la cantidad de acciones compradas.
            'cantidad': cantidad,
            # Calcula y guarda cuánto dinero total se invirtió (cantidad * precio unitario).
            'inversion_inicial': cantidad * precio_compra,
            # Guarda el precio al que se compró cada acción.
            'precio_compra': precio_compra
        }
        
        # Llama al método del PersistenciaMixin para guardar estos cambios en el archivo JSON de inmediato.
        self.guardar_datos()
        
        # El asistente confirma por voz que la acción fue guardada.
        self.hablar(f"Posición de {simbolo} agregada a tu cartera.")
        # Imprime un mensaje de éxito en la consola con los detalles de la compra.
        print(f"Cartera actualizada: {simbolo} ({cantidad} acciones a ${precio_compra:.2f})")

    # MÉTODO: ANALIZAR LA CARTERA COMPLETA
    
    def analizar_cartera(self):
        """Analiza la cartera de inversiones guardada del usuario."""
        
        # Primero verifica si el diccionario de la cartera está vacío.
        if not self.cartera_acciones:
            # Si está vacío, avisa por voz y termina la ejecución del método (return).
            self.hablar("No tienes acciones en tu cartera. Agrega algunas primero.")
            return

        # Imprime un encabezado decorativo en la consola.
        print("\n" + "="*60)
        print("ANÁLISIS DE CARTERA")
        print("="*60)

        # Inicializa variables en 0 para ir sumando el valor de toda la cartera y la ganancia/pérdida total.
        valor_total = 0.0
        ganancia_total = 0.0

        # Recorre cada elemento del diccionario. 'simbolo' es la clave (ej. AAPL) y 'datos' es el diccionario con cantidad y precios.
        for simbolo, datos in self.cartera_acciones.items():
            # Inicia un bloque try-except por si falla la conexión al consultar alguna acción.
            try:
                # Crea el objeto Ticker para la acción actual.
                accion = yf.Ticker(simbolo)
                # Descarga el historial del último día para obtener el precio actual.
                datos_hist = accion.history(period='1d')
                
                # Si Yahoo Finance no devuelve datos para este símbolo...
                if datos_hist.empty:
                    # Imprime un aviso de que no hay datos y salta a la siguiente acción del ciclo (continue).
                    print(f"\n{simbolo}: [sin datos disponibles]")
                    continue

                # Extrae el precio de cierre más reciente.
                precio_actual = datos_hist['Close'].iloc[-1]
                
                # Calcula cuánto vale HOY esa posición (precio de hoy * cantidad de acciones que tenés).
                valor_posicion = precio_actual * datos['cantidad']
                
                # Calcula si vas ganando o perdiendo plata (valor de hoy - lo que pagaste originalmente).
                ganancia = valor_posicion - datos['inversion_inicial']
                
                # Calcula el porcentaje de ganancia o pérdida. (Evita división por cero si la inversión fue 0).
                porcentaje_ganancia = (ganancia / datos['inversion_inicial']) * 100 if datos['inversion_inicial'] else 0

                # Suma el valor de esta posición al total de toda tu cartera.
                valor_total += valor_posicion
                # Suma la ganancia/pérdida de esta posición a la ganancia total de la cartera.
                ganancia_total += ganancia

                # Imprime el desglose detallado para esta acción en particular.
                print(f"\n{simbolo}")
                print(f"  Cantidad: {datos['cantidad']} acciones")
                print(f"  Precio actual: ${precio_actual:.2f}")
                print(f"  Valor posición: ${valor_posicion:.2f}")
                print(f"  Ganancia/Pérdida: ${ganancia:.2f} ({porcentaje_ganancia:.2f}%)")
                
            # Si ocurre algún error técnico con esta acción específica...
            except Exception as e:
                # Imprime el error, pero el ciclo 'for' continúa con la siguiente acción de la lista.
                print(f"\n{simbolo}: [Error al consultar: {e}]")

        # Imprime los resultados finales y totales de la cartera.
        print(f"\n{'─'*60}")
        print(f"VALOR TOTAL DE CARTERA: ${valor_total:.2f}")
        print(f"GANANCIA/PÉRDIDA TOTAL: ${ganancia_total:.2f}")
        print("="*60 + "\n")

        # El asistente lee en voz alta el resumen global de tu inversión.
        self.hablar(f"Tu cartera tiene un valor total de ${valor_total:.2f} con una ganancia de ${ganancia_total:.2f}")
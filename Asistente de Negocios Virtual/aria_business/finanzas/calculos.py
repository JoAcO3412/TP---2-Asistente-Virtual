"""Cálculos empresariales clásicos: margen, ROI, punto de equilibrio, proyecciones y monedas."""

# Importa la librería yfinance (Yahoo Finance) y le asigna el alias 'yf' para usarla de forma más corta.
import yfinance as yf


# Define la clase CalculosMixin, diseñada para ser combinada (heredada) con el asistente principal.
class CalculosMixin:
    """Mixin con las funciones de cálculo financiero-empresarial."""

    # MÉTODO: CALCULAR MARGEN DE GANANCIA
    
    def calcular_margen_ganancia(self, costo: float, precio_venta: float):
        """Calcula el margen de ganancia de un producto o servicio."""
        
        # Calcula el margen en porcentaje. Usa un condicional (if precio_venta else 0) 
        # para evitar un error de "división por cero" en caso de que el precio de venta sea 0.
        margen = ((precio_venta - costo) / precio_venta) * 100 if precio_venta else 0
        
        # Calcula la ganancia en dinero (moneda) restando el costo al precio de venta.
        ganancia_unitaria = precio_venta - costo

        # Imprime los resultados en la consola con un formato limpio.
        print(f"\nANÁLISIS DE MARGEN")
        # Imprime el costo limitando los decimales a 2 (.2f).
        print(f"Costo: ${costo:.2f}")
        # Imprime el precio de venta con 2 decimales.
        print(f"Precio de venta: ${precio_venta:.2f}")
        # Imprime la ganancia en billete con 2 decimales.
        print(f"Ganancia unitaria: ${ganancia_unitaria:.2f}")
        # Imprime el porcentaje de margen con 2 decimales.
        print(f"Margen de ganancia: {margen:.2f}%\n")

        # El asistente dicta por voz el resultado final del margen.
        self.hablar(f"Margen de ganancia de {margen:.2f} por ciento")

    # MÉTODO: CALCULAR ROI (Retorno de Inversión)
    
    def calcular_roi(self, inversion_inicial: float, ganancia_neta: float):
        """Calcula el Retorno sobre la Inversión (ROI)."""
        
        # Fórmula del ROI: (Ganancia / Inversión) * 100. 
        # Nuevamente evita la división por cero si la inversión inicial es 0.
        roi = (ganancia_neta / inversion_inicial) * 100 if inversion_inicial else 0

        # Imprime el encabezado y los datos ingresados/calculados en la consola.
        print(f"\nANÁLISIS DE ROI")
        print(f"Inversión inicial: ${inversion_inicial:.2f}")
        print(f"Ganancia neta: ${ganancia_neta:.2f}")
        print(f"ROI: {roi:.2f}%\n")

        # El asistente comunica el resultado del ROI por voz.
        self.hablar(f"Tu retorno sobre la inversión es de {roi:.2f} por ciento")

    # MÉTODO: CALCULAR PUNTO DE EQUILIBRIO

    def calcular_punto_equilibrio(self, costos_fijos: float, margen_unitario: float, precio: float):
        """Calcula el punto de equilibrio (unidades e ingresos necesarios)."""
        
        # Calcula cuántas unidades se deben vender para cubrir los costos fijos.
        # Evita la división por cero si el margen es 0.
        punto_eq = costos_fijos / margen_unitario if margen_unitario else 0
        
        # Calcula cuánto dinero representan esas unidades vendidas.
        ingresos_eq = punto_eq * precio

        # Muestra en consola el desglose del cálculo.
        print(f"\nPUNTO DE EQUILIBRIO")
        print(f"Costos fijos: ${costos_fijos:.2f}")
        print(f"Margen unitario: ${margen_unitario:.2f}")
        print(f"Precio unitario: ${precio:.2f}")
        # Muestra las unidades a vender sin decimales (.0f) porque no se puede vender media unidad.
        print(f"Unidades a vender: {punto_eq:.0f}")
        print(f"Ingresos necesarios: ${ingresos_eq:.2f}\n")

        # El asistente informa por voz cuántas unidades hay que vender.
        self.hablar(f"Necesitas vender {punto_eq:.0f} unidades para alcanzar el equilibrio")

    # MÉTODO: PROYECTAR INGRESOS
    
    def proyectar_ingresos(self, ingresos_actuales: float, tasa_crecimiento: float, periodos: int):
        """Proyecta ingresos futuros a partir de una tasa de crecimiento constante."""
        
        # Imprime el encabezado mostrando por cuántos períodos se hace la proyección.
        print(f"\nPROYECCIÓN DE INGRESOS ({periodos} períodos)")
        print(f"Ingresos actuales: ${ingresos_actuales:.2f}")
        print(f"Tasa de crecimiento: {tasa_crecimiento}%")
        print("─" * 50)

        # Crea una lista vacía para ir guardando los ingresos calculados de cada período.
        proyecciones = []
        # Define una variable temporal que arranca con el valor actual.
        ingresos = ingresos_actuales

        # Inicia un bucle (loop) que se repetirá desde 1 hasta el número de períodos solicitados.
        for i in range(1, periodos + 1):
            # Aplica la fórmula de interés compuesto: valor anterior * (1 + (tasa / 100)).
            ingresos = ingresos * (1 + tasa_crecimiento / 100)
            # Guarda el nuevo valor en la lista de proyecciones.
            proyecciones.append(ingresos)
            # Imprime en consola el resultado de ese período específico.
            print(f"Período {i}: ${ingresos:.2f}")

        # Línea separadora final.
        print("─" * 50)
        
        # Toma el último valor de la lista (proyecciones[-1]) que representa el ingreso final.
        ingreso_final = proyecciones[-1]
        # Calcula cuánto creció el dinero en total restando el ingreso inicial al final.
        crecimiento_total = ingreso_final - ingresos_actuales

        # Dicta el resultado de la proyección a futuro.
        self.hablar(f"En {periodos} períodos, proyectas ingresos de ${ingreso_final:.2f}")
        # Muestra el crecimiento total en la consola.
        print(f"Crecimiento total: ${crecimiento_total:.2f}\n")

    # MÉTODO: CONVERTIR MONEDA
    
    def convertir_moneda(self, cantidad: float, moneda_origen: str, moneda_destino: str):
        """Convierte una cantidad entre dos monedas usando tasas en tiempo real."""
        
        # Inicia un bloque try-except para manejar errores (por ejemplo, si no hay internet o el código de moneda no existe).
        try:
            # Avisa por voz que está empezando la conversión.
            self.hablar(f"Convirtiendo {cantidad} {moneda_origen} a {moneda_destino}...")

            # Construye el símbolo (ticker) de conversión que usa Yahoo Finance, ejemplo: "USDEUR=X".
            par = f"{moneda_origen}{moneda_destino}=X"
            # Crea el objeto Ticker con el símbolo armado.
            tasa = yf.Ticker(par)
            # Descarga el historial de precios de ese par para el día de hoy ('1d').
            datos = tasa.history(period='1d')

            # Si la descarga devuelve un conjunto de datos vacío (la moneda no existe o está mal escrita)...
            if datos.empty:
                self.hablar(f"No encontré tasa de cambio para {moneda_origen}/{moneda_destino}")
                # Sale de la función sin continuar.
                return

            # Extrae el precio de cierre más reciente de los datos descargados.
            tasa_cambio = datos['Close'].iloc[-1]
            # Multiplica la cantidad ingresada por la tasa de cambio obtenida.
            resultado = cantidad * tasa_cambio

            # Imprime el resultado en consola.
            print(f"\nCONVERSIÓN DE MONEDAS")
            print(f"{cantidad} {moneda_origen} = {resultado:.2f} {moneda_destino}")
            # Imprime también a cuánto equivale 1 unidad de la moneda de origen con 4 decimales de precisión.
            print(f"Tasa: 1 {moneda_origen} = {tasa_cambio:.4f} {moneda_destino}\n")

            # Dicta por voz el resultado de la conversión.
            self.hablar(f"{cantidad} {moneda_origen} equivale a {resultado:.2f} {moneda_destino}")

        # Si ocurre un error de conexión, o la librería yfinance falla...
        except Exception as e:
            # Informa del error por voz, adjuntando el mensaje técnico capturado en 'e'.
            self.hablar(f"Error en conversión: {str(e)}")
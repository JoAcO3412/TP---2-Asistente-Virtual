# Importamos la librería estándar 'time' para poder hacer pausas (delays) en el código.
import time

class SalirAsistente(Exception):
    """Se lanza cuando el usuario escribe 'salir' en cualquier pregunta."""
    pass

# Definimos una clase llamada ComandosMixin. Se usa como "Mixin" para agregar esta funcionalidad a una clase principal.
class ComandosMixin:
    """Mixin que interpreta comandos de texto/voz y coordina al resto de mixins."""
    
    def pedir(self, mensaje: str) -> str:
        """Hace una pregunta por consola. Si el usuario escribe 'salir', cierra el asistente."""
        texto = input(mensaje)
        if texto.strip().lower() in ["salir", "adiós", "adios"]:
            raise SalirAsistente()
        return texto
    
    def procesar_comando(self, comando: str):
        """Interpreta el comando de texto (o voz) del usuario y ejecuta la acción."""
        
        # Verificamos si el comando está vacío (None o un texto vacío "").
        if not comando:
            # Si está vacío, salimos de la función sin hacer nada.
            return

        # --- Fecha y hora ---
        
        # Comprueba si ALGUNA de las frases de la lista está dentro de la variable 'comando'.
        if any(p in comando for p in ["qué hora es", "que hora es", "hora actual",
                                       "fecha de hoy", "qué día es", "que dia es",
                                       "fecha y hora", "hora y fecha"]):
            # Si coincide, llama al método que dice la fecha y hora.
            self.obtener_fecha_hora()

        # --- Reproducir canciones en YouTube ---
        
        # Comprueba si el comando tiene palabras clave para reproducir música.
        elif any(p in comando for p in ["reproducir", "poner canción", "poner cancion",
                                         "reproduce", "toca la canción", "toca la cancion",
                                         "poner música", "poner musica"]):
            self.hablar("¿Qué canción quieres escuchar?")
            # Pide al usuario por consola que escriba qué canción quiere y elimina espacios sobrantes con .strip().
            cancion = self.pedir("[Tú]: Escribe la canción: ").strip()
            # Si el usuario escribió algo (la variable no está vacía)...
            if cancion:
                # ...llama al método para reproducir esa canción.
                self.reproducir_cancion(cancion)

        # --- Chistes ---
        
        # Comprueba si el comando pide un chiste o algo gracioso.
        elif any(p in comando for p in ["chiste", "cuéntame algo gracioso", "cuentame algo gracioso",
                                         "hazme reír", "hazme reir"]):
            # Llama al método que cuenta un chiste.
            self.contar_chiste()

        # --- Abrir sitio web ---
        
        # Comprueba si el comando pide abrir una página web.
        elif any(p in comando for p in ["abrir sitio", "abrir página", "abrir pagina",
                                         "abrir web", "ir a la página", "ir a la pagina"]):
            self.hablar("¿Que sitio web querés abrir?")
            # Pide al usuario que escriba la dirección o nombre del sitio y limpia los espacios.
            sitio = self.pedir("[Tú]: ¿Qué sitio web querés abrir? ").strip()
            # Si el usuario ingresó un sitio válido...
            if sitio:
                # ...llama al método para abrir el navegador en ese sitio.
                self.abrir_sitio_web(sitio)

        # --- Análisis de acciones individuales ---
        
        # Verifica si piden el precio/cotización explícitamente O si mencionan "acción"/"precio"...
        elif any(p in comando for p in ["precio de", "cotización de", "cotizacion de"]) or \
                (any(p in comando for p in ["precio", "acción", "accion", "cotización", "stock"])
                 # ...pero se asegura de que NO estén pidiendo "comparar" ni analizar "múltiples" acciones.
                 and "comparar" not in comando and "múltiples" not in comando
                 and "multiples" not in comando and "varias" not in comando):
                    
            self.hablar("¿De qué acción quieres saber el precio?")
            # Pide el símbolo de la acción, quita espacios y lo convierte a MAYÚSCULAS con .upper().
            simbolo = self.pedir("[Tú]: Símbolo de la acción (AAPL, MSFT, GOOGL, etc.): ").strip().upper()
            # Si se ingresó un símbolo...
            if simbolo:
                # ...llama al método que busca el precio de esa acción específica.
                self.obtener_precio_accion(simbolo)

        # --- Análisis de múltiples acciones ---
        
        # Verifica si el usuario quiere analizar varias acciones a la vez.
        elif any(p in comando for p in ["analizar múltiples", "analizar multiples", "varias acciones"]):
            # Llama al método que maneja el análisis de un conjunto de acciones.
            self.analizar_multiples_acciones()

        # --- Historial de precios ---
        
        # Verifica si el usuario menciona la palabra "historial".
        elif "historial" in comando:
            self.hablar("¿De qué símbolo quieres ver el historial?")
            # Pide el símbolo de la acción (en mayúsculas).
            simbolo = self.pedir("[Tú]: ¿Símbolo?: ").strip().upper()
            
            self.hablar("¿Para qué período? Por ejemplo, un mes, seis meses o un año.")
            # Pide el período de tiempo; si el usuario presiona Enter sin escribir nada, usa '1mo' (1 mes) por defecto.
            periodo = self.pedir("[Tú]: ¿Período? (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y): ").strip() or '1mo'
            # Si se ingresó un símbolo...
            if simbolo:
                # ...llama al método que obtiene el historial de precios para ese período.
                self.obtener_historial_precio(simbolo, periodo)

        # --- Índices ---
        
        # Verifica si el comando menciona mercados bursátiles o índices.
        elif any(p in comando for p in ["índices", "indices", "mercado", "bolsa", "sp500", "nasdaq"]):
            # Si mencionan la palabra "índices" de forma general...
            if any(p in comando for p in ["índices", "indices"]):
                # ...muestra un resumen de los principales índices.
                self.obtener_indices_principales()
            # Si no (es decir, mencionaron un índice específico)...
            else:
                self.hablar("¿Cuál índice deseas consultar?")
                # ...pide que confirme qué índice quiere ver.
                indice = self.pedir("[Tú]: ¿Cuál índice? (sp500, nasdaq, dow, ibex, dax, ftse, nikkei): ").strip()
                # Si ingresó un índice válido...
                if indice:
                    # ...llama al método para buscar ese índice específico.
                    self.obtener_indice_mercado(indice)

        # --- Sector ---
        
        # Verifica si mencionan sector o industria, asegurando que no quieran investigar una empresa concreta.
        elif any(p in comando for p in ["sector", "industria"]) and "investigar" not in comando \
                and "información de empresa" not in comando:
            self.hablar("¿Qué sector deseas analizar?")
            # Pide al usuario que ingrese el nombre del sector.
            sector = self.pedir("[Tú]: ¿Qué sector? (tecnología, bancario, salud, energía, retail, bienes de consumo): ").strip()
            # Si ingresó un sector...
            if sector:
                # ...llama al método que analiza dicho sector.
                self.analizar_sector(sector)

        # --- Cartera de inversiones ---
        
        # Verifica si el usuario quiere agregar una acción a su portafolio personal.
        elif any(p in comando for p in ["agregar a mi cartera", "agregar posición", "agregar accion a cartera"]):
            self.hablar("¿Cuál es el símbolo de la acción a agregar?")
            # Pide el símbolo de la acción.
            simbolo = self.pedir("[Tú]: Símbolo: ").strip().upper()
            # Inicia un bloque de prueba para capturar errores si el usuario escribe texto en vez de números.
            try:
                self.hablar("¿Qué cantidad de acciones compraste?")
                # Pide la cantidad de acciones y la convierte a número decimal (float).
                cantidad = float(self.pedir("[Tú]: Cantidad de acciones: "))
                
                self.hablar("¿A qué precio de compra?")
                # Pide el precio de compra y lo convierte a número decimal (float).
                precio_compra = float(self.pedir("[Tú]: Precio de compra: "))
                # Llama al método para guardar estos datos en la cartera del usuario.
                self.agregar_posicion_cartera(simbolo, cantidad, precio_compra)
            # Si la conversión a 'float' falla (ej: el usuario escribió "cinco")...
            except ValueError:
                # ...avisa al usuario que hubo un error con los números ingresados.
                self.hablar("Error en los valores ingresados")

        # Verifica si el usuario quiere ver un resumen de las acciones que ya tiene.
        elif any(p in comando for p in ["cartera", "portafolio", "mis acciones"]):
            # Llama al método que analiza y muestra el estado del portafolio.
            self.analizar_cartera()

        # --- Comparación de acciones ---
        
        # Verifica si el comando indica que se quieren comparar dos cosas.
        elif any(p in comando for p in ["compara", "comparar", "versus", " vs "]):
            self.hablar("¿Cuál es la primera acción?")
            # Pide el símbolo de la primera acción a comparar.
            sym1 = self.pedir("[Tú]: Primera acción: ").strip().upper()
            
            self.hablar("¿Y con cuál la quieres comparar?")
            # Pide el símbolo de la segunda acción a comparar.
            sym2 = self.pedir("[Tú]: Segunda acción: ").strip().upper()
            
            # Si ambos símbolos fueron ingresados...
            if sym1 and sym2:
                # ...llama al método que hace la comparativa entre ambas.
                self.comparar_acciones(sym1, sym2)

        # --- Cálculos de margen ---
        
        # Verifica si se solicitan cálculos de ganancias o márgenes.
        elif any(p in comando for p in ["margen", "ganancia", "utilidad"]):
            # Inicia bloque para atrapar errores matemáticos/de formato.
            try:
                self.hablar("Por favor, ingresa el costo unitario.")
                # Pide y convierte a decimal el costo de un producto.
                costo = float(self.pedir("[Tú]: Costo unitario: "))
                
                self.hablar("Ahora ingresa el precio de venta.")
                # Pide y convierte a decimal el precio al que se vende.
                precio = float(self.pedir("[Tú]: Precio de venta: "))
                # Calcula y muestra el margen de ganancia.
                self.calcular_margen_ganancia(costo, precio)
            # Si el usuario no ingresó números válidos...
            except ValueError:
                # ...avisa del error.
                self.hablar("Error en los valores ingresados")

        # --- Cálculo de ROI ---
        
        # Verifica si se pide calcular el Retorno de Inversión (ROI).
        elif any(p in comando for p in ["roi", "retorno", "inversión", "inversion"]):
            try:
                self.hablar("Ingresa la inversión inicial.")
                # Pide el monto inicial invertido.
                inversion = float(self.pedir("[Tú]: Inversión inicial: "))
                
                self.hablar("Ingresa la ganancia neta.")
                # Pide cuánto dinero se ganó en neto.
                ganancia = float(self.pedir("[Tú]: Ganancia neta: "))
                # Ejecuta la fórmula del ROI.
                self.calcular_roi(inversion, ganancia)
            except ValueError:
                self.hablar("Error en los valores")

        # --- Punto de equilibrio ---
        
        # Verifica si se quiere calcular cuándo la empresa deja de perder y empieza a ganar (Breakeven).
        elif any(p in comando for p in ["equilibrio", "punto equilibrio", "breakeven"]):
            try:
                self.hablar("Ingresa los costos fijos.")
                # Pide los gastos fijos mensuales/anuales.
                costos_fijos = float(self.pedir("[Tú]: Costos fijos: "))
                
                self.hablar("Ingresa el margen unitario.")
                # Pide cuánto se gana por cada unidad vendida.
                margen = float(self.pedir("[Tú]: Margen unitario: "))
                
                self.hablar("Por último, ingresa el precio unitario.")
                # Pide el precio al público de cada unidad.
                precio = float(self.pedir("[Tú]: Precio unitario: "))
                
                # Calcula cuántas unidades hay que vender para no perder dinero.
                self.calcular_punto_equilibrio(costos_fijos, margen, precio)
            except ValueError:
                self.hablar("Error en los valores")

        # --- Proyección de ingresos ---
        
        # Verifica si el usuario quiere estimar ganancias futuras.
        elif any(p in comando for p in ["proyecta", "proyección", "proyeccion", "pronóstico", "pronostico"]):
            try:
                self.hablar("Ingresa los ingresos actuales.")
                # Pide el nivel de ingresos que se tiene hoy.
                ingresos = float(self.pedir("[Tú]: Ingresos actuales: "))
                
                self.hablar("Ingresa la tasa de crecimiento estimada en porcentaje.")
                # Pide el porcentaje estimado de crecimiento.
                tasa = float(self.pedir("[Tú]: Tasa de crecimiento (%): "))
                
                self.hablar("¿Para cuántos períodos?")
                # Pide por cuántos meses/años se quiere proyectar (como entero 'int').
                periodos = int(self.pedir("[Tú]: Número de períodos: "))
                # Ejecuta el cálculo de crecimiento compuesto.
                self.proyectar_ingresos(ingresos, tasa, periodos)
            except ValueError:
                self.hablar("Error en los valores")

        # --- Conversión de monedas ---
        # Verifica si se necesita convertir divisas.
        elif any(p in comando for p in ["moneda", "cambio", "conversión", "conversion", "dólar", "dolar", "euro"]):
            try:
                self.hablar("¿Qué cantidad deseas convertir?")
                # Pide la cantidad de dinero a convertir.
                cantidad = float(self.pedir("[Tú]: Cantidad: "))
                
                self.hablar("¿Cuál es la moneda de origen?")
                # Pide el código de la moneda que tiene actualmente el usuario.
                origen = self.pedir("[Tú]: Moneda origen (USD, EUR, MXN, ARS, etc.): ").strip().upper()
                
                self.hablar("¿A qué moneda deseas convertirla?")
                # Pide el código de la moneda a la que quiere cambiar.
                destino = self.pedir("[Tú]: Moneda destino: ").strip().upper()
                # Llama al método que hace el tipo de cambio.
                self.convertir_moneda(cantidad, origen, destino)
            except ValueError:
                self.hablar("Error en los valores")

        # --- Gestión de contactos ---
        # Verifica si el comando es para guardar un nuevo contacto.
        elif any(p in comando for p in ["agregar contacto", "nuevo contacto"]):
            self.hablar("¿Cuál es el nombre del contacto?")
            # Pide nombre, correo, teléfono y el rol de esa persona.
            nombre = self.pedir("[Tú]: Nombre: ").strip()
            
            self.hablar("¿Cuál es su correo electrónico?")
            email = self.pedir("[Tú]: Email: ").strip()
            
            self.hablar("¿Cuál es su teléfono?")
            telefono = self.pedir("[Tú]: Teléfono: ").strip()
            
            self.hablar("¿Qué tipo de contacto es? Por ejemplo, cliente, proveedor o socio.")
            tipo = self.pedir("[Tú]: Tipo (cliente/proveedor/socio): ").strip()
            
            # Guarda los datos en la libreta de direcciones.
            self.agregar_contacto(nombre, email, telefono, tipo)

        # Verifica si el usuario quiere ver su lista completa de contactos.
        elif any(p in comando for p in ["listar contactos", "mis contactos", "ver contactos"]):
            # Llama al método que imprime todos los contactos guardados.
            self.listar_contactos()

        # Verifica si el usuario necesita buscar a una persona específica en su agenda.
        elif any(p in comando for p in ["buscar contacto", "encontrar contacto"]):
            self.hablar("¿Cómo se llama el contacto que buscas?")
            # Pide el nombre de la persona a buscar.
            nombre = self.pedir("[Tú]: ¿Qué contacto buscas? ").strip()
            # Busca y muestra la información de ese contacto.
            self.buscar_contacto(nombre)

        # --- Gestión de reuniones ---
        # Verifica si el usuario quiere agendar un nuevo evento.
        elif any(p in comando for p in ["agendar", "reunión", "reunion", "programar reunión", "programar reunion"]):
            self.hablar("Vamos a agendar la reunión. ¿Cuál es el título?")
            # Pide los detalles del evento (título, fecha, hora, con quién, anotaciones).
            titulo = self.pedir("[Tú]: Título de reunión: ").strip()
            
            self.hablar("¿Para qué fecha?")
            fecha = self.pedir("[Tú]: Fecha (DD/MM/YYYY): ").strip()
            
            self.hablar("¿A qué hora?")
            hora = self.pedir("[Tú]: Hora (HH:MM): ").strip()
            
            self.hablar("¿Quiénes son los participantes?")
            participantes = self.pedir("[Tú]: Participantes: ").strip()
            
            self.hablar("¿Deseas agregar alguna nota opcional?")
            notas = self.pedir("[Tú]: Notas (opcional): ").strip()
            
            # Guarda la reunión en el sistema.
            self.agendar_reunion(titulo, fecha, hora, participantes, notas)

        # Verifica si el usuario quiere revisar su agenda de eventos.
        elif any(p in comando for p in ["mis reuniones", "listar reuniones", "ver reuniones"]):
            # Muestra las reuniones programadas.
            self.listar_reuniones()

        # --- Investigación empresarial ---
        # Verifica si se quiere buscar información general sobre una compañía.
        elif any(p in comando for p in ["investiga", "investigar", "información de empresa", "informacion de empresa"]):
            self.hablar("¿Sobre qué empresa quieres investigar?")
            # Pide el nombre de la empresa a buscar.
            empresa = self.pedir("[Tú]: ¿Qué empresa? ").strip()
            # Llama al método que recopila los datos de la empresa.
            self.investigar_empresa(empresa)

        # --- Ayuda ---
        # Verifica si el usuario no sabe qué hacer y pide el manual de instrucciones.
        elif any(p in comando for p in ["ayuda", "help", "comandos", "qué puedo"]):
            # Imprime la tabla con todos los comandos.
            self.mostrar_ayuda()

        # --- Salida ---
        # Verifica si el usuario se quiere despedir o apagar el programa.
        elif any(p in comando for p in ["adiós", "adios", "salir", "apagar"]):
            # Da un mensaje de despedida.
            self.hablar("Hasta luego. Que tengas éxito en tus negocios.")
            # Cambia esta variable a Falso. Esto es MUY IMPORTANTE porque es lo que rompe el ciclo 'while' principal.
            self.en_ejecucion = False

        # --- Comando no reconocido ---
        # Si lo que escribió el usuario no coincide con NINGÚN bloque de los anteriores (if / elif)...
        else:
            # ...le dice que no entendió y le sugiere pedir ayuda.
            self.hablar("No reconozco ese comando. Escribe 'ayuda' para ver opciones.")

    # Definimos el método que muestra el menú visual de comandos.
    def mostrar_ayuda(self):
        # Cadena de documentación.
        """Muestra todos los comandos disponibles del asistente."""
        
        # Guardamos en la variable 'ayuda' un texto multilínea (usando triple comilla) con un diseño ASCII.
        ayuda = """
  ================================================================
                       COMANDOS DISPONIBLES                      
  ================================================================

                                                                 
      ANÁLISIS FINANCIERO:                                        
     • "Precio de AAPL" / "Cotización de MSFT"                   
     • "Analizar múltiples" (varias acciones a la vez)           
     • "Comparar AAPL vs MSFT" (incluye P/E ratio)               
     • "Historial" de AAPL (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y)       
                                                                 
      CARTERA DE INVERSIONES:                                     
     • "Agregar a mi cartera" (guarda la posición)               
     • "Analizar cartera" / "Mis acciones"                       
                                                                 
      ÍNDICES Y SECTORES:                                         
     • "Ver índices" (S&P 500, Nasdaq, Dow, IBEX, DAX...)       
     • "Analizar sector [tecnología/bancario/salud/energía...]" 
                                                                 
      CÁLCULOS EMPRESARIALES:                                     
     • "Calcular margen" (costo y precio de venta)               
     • "Calcular ROI" (retorno sobre inversión)                 
     • "Punto de equilibrio"                                    
     • "Proyectar ingresos"                                     
     • "Convertir moneda" (USD a EUR, etc.)                     
                                                                 
      GESTIÓN DE CONTACTOS:                                       
     • "Agregar contacto"                                       
     • "Ver mis contactos"                                      
     • "Buscar contacto"                                        
                                                                 
      GESTIÓN DE REUNIONES:                                       
     • "Agendar reunión"                                        
     • "Ver mis reuniones"                                      
                                                                 
      INVESTIGACIÓN EMPRESARIAL:                                  
     • "Investigar [empresa]"                                   
                                                                 
      UTILIDAD Y ENTRETENIMIENTO:                                 
     • "Qué hora es" / "Fecha de hoy"                           
     • "Reproducir [canción]" (la pone en YouTube)              
     • "Cuéntame un chiste"                                     
     • "Abrir sitio [url]" (abre una página web)                
                                                                 
      ACCIONES POPULARES POR SECTOR:                              
     TECNOLOGÍA: AAPL, MSFT, GOOGL, META, NVDA, TSLA            
     BANCARIO: JPM, BAC, WFC, GS                                
     SALUD: UNH, JNJ, PFE, ABBV                                 
     ENERGÍA: XOM, CVX, SLB, MPC                                
     RETAIL: AMZN, WMT, TM                                      
                                                                 
  SALIR:                                                      
     • "Adiós"                                                  
                                                                 
 =================================================================
        """
        # Imprimimos la variable 'ayuda' en la terminal para que el usuario la vea.
        print(ayuda)
        # El asistente emite un mensaje invitando a realizar una acción.
        self.hablar("Aquí están tus opciones de comando. ¿Qué necesitas?")

    # Este es el método que arranca y mantiene vivo al programa.
    def iniciar(self):
        # Cadena de documentación.
        """Inicia el asistente de negocios, por voz o por texto según elija el usuario."""
        
        # Establece la variable de estado en True. Mientras sea True, el asistente no se apagará.
        self.en_ejecucion = True
        # Da un mensaje de bienvenida personalizado usando variables de la clase padre.
        self.hablar(f"Bienvenido a {self.nombre}. Soy tu asistente de negocios para {self.empresa}. ¿Cómo puedo ayudarte?")

        # Imprime un encabezado decorativo de inicio en la terminal.
        print("\n")
        print("==================================================================")
        print("            ASISTENTE VIRTUAL DE NEGOCIOS - ARIA BUSINESS         ")
        print("==================================================================")
        print(f"Empresa: {self.empresa}")
        print(f"Asistente: {self.nombre}")
        print("─" * 68)
        
        # Muestra automáticamente la lista de comandos al arrancar.
        self.mostrar_ayuda()

        # Pregunta al usuario si quiere usar el micrófono o el teclado. .strip() quita espacios, .lower() pasa a minúscula.
        modo = input("\n[Tú]: ¿Querés dar los comandos por VOZ o por TEXTO? (voz/texto): ").strip().lower()        # Si la respuesta empieza con la letra 'v' (ej: "voz", "v"), la variable modo_voz será True. Si no, False.
        modo_voz = modo.startswith("v")

        # Verifica qué modo eligió el usuario.
        if modo_voz:
            # Da instrucciones para el uso por micrófono.
            self.hablar("Perfecto, te voy a escuchar por el micrófono. Decime un comando cuando quieras.")
        else:
            # Da confirmación del uso por teclado.
            self.hablar("Perfecto, vamos a trabajar por texto.")

        # COMIENZA EL BUCLE PRINCIPAL (Game Loop). Este while se repetirá infinitamente hasta que 'en_ejecucion' sea False.
        while self.en_ejecucion:
            # Abrimos un bloque try-except general para evitar que el programa "explote" (crashee) si hay un error.
            try:
                # Si el usuario eligió hablar...
                if modo_voz:
                    # ...llama al método escuchar() que captura el audio y lo convierte a texto.
                    comando = self.escuchar()
                # Si eligió escribir...
                else:
                    # ...espera a que el usuario escriba en la consola, quita espacios extra y lo pasa a minúsculas.
                    comando = self.pedir("\n[Tú]: ").strip().lower()

                # Si se detectó algún comando válido (no está vacío)...
                if comando:
                    # ...le enviamos ese texto al método procesar_comando para que evalúe los if/elif y haga la tarea.
                    self.procesar_comando(comando)
                
                # Pausa de 0.3 segundos al final de cada ciclo para no saturar el procesador de la computadora.
                time.sleep(0.3)
                
            except SalirAsistente:
                self.hablar("Hasta luego. Que tengas éxito en tus negocios.")
                self.en_ejecucion = False
                
            # Si el usuario presiona Ctrl + C en la terminal (Interrupción por teclado)...
            except KeyboardInterrupt:
                # ...imprime un aviso de cierre.
                print("\n[Sistema]: Asistente cerrado.")
                # ...se despide.
                self.hablar("Hasta luego.")
                # ...y ejecuta 'break', lo que rompe forzosamente el ciclo 'while' y termina el programa.
                break
                
            # Si ocurre CUALQUIER otro error en el código (falla de internet, micrófono desconectado, etc.)...
            except Exception as e:
                # ...imprime en la consola cuál fue el error técnico exacto, pero el bucle 'while' no se rompe y sigue funcionando.
                print(f"[Error]: {e}")
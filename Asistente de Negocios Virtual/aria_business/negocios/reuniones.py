"""Gestión de reuniones y agendas de negocio."""


# Define la clase ReunionesMixin, que aportará la funcionalidad de agenda al AsistenteNegocios principal.
class ReunionesMixin:
    """Mixin con las funciones de gestión de reuniones."""

    # MÉTODO: AGENDAR UNA NUEVA REUNIÓN
    
    # Recibe los datos básicos, dejando 'notas' como opcional (si no se pasa, asume un texto vacío "").
    def agendar_reunion(self, titulo: str, fecha: str, hora: str, participantes: str, notas: str = ""):
        """Agenda una reunión de negocios."""
        
        # Crea un diccionario llamado 'reunion' para agrupar todos los datos del evento ingresados por el usuario.
        reunion = {
            # Guarda el título o asunto de la reunión.
            'titulo': titulo,
            # Guarda la fecha programada.
            'fecha': fecha,
            # Guarda la hora del encuentro.
            'hora': hora,
            # Guarda los nombres de las personas que van a participar.
            'participantes': participantes,
            # Guarda apuntes extras o detalles adicionales.
            'notas': notas,
            # Define por defecto que el estado de la nueva reunión es "programada".
            'estado': 'programada'
        }
        
        # Agrega (append) el diccionario de esta nueva reunión a la lista general 'reuniones' del asistente.
        self.reuniones.append(reunion)
        
        # Llama al método del PersistenciaMixin para guardar la lista actualizada en tu archivo JSON de forma inmediata.
        self.guardar_datos()
        
        # El asistente dicta por voz un mensaje confirmando el título, fecha y hora del evento.
        self.hablar(f"Reunión '{titulo}' agendada para {fecha} a las {hora}")
        
        # Imprime un mensaje corto en la consola validando que se guardó exitosamente.
        print(f"Reunión agendada: {titulo}")

    # MÉTODO: LISTAR TODAS LAS REUNIONES
    
    def listar_reuniones(self):
        """Lista todas las reuniones programadas."""
        
        # Verifica si la lista 'reuniones' está vacía (es decir, no hay nada agendado).
        if not self.reuniones:
            # Si está vacía, el asistente avisa por voz.
            self.hablar("No tienes reuniones programadas.")
            # Sale de la función ('return') para evitar imprimir los encabezados de una tabla que no va a tener datos.
            return

        # Imprime el encabezado decorativo de la agenda en la consola.
        print("\n" + "="*60)
        print("REUNIONES PROGRAMADAS")
        print("="*60)

        # Usa 'enumerate' para recorrer la lista. Esto permite obtener la reunión (diccionario) 
        # y al mismo tiempo llevar un contador (i). El '1' indica que 'i' empezará a contar desde 1 y no desde 0.
        for i, reunion in enumerate(self.reuniones, 1):
            # Imprime el número identificador de la reunión (ej. REUNIÓN 1, REUNIÓN 2).
            print(f"\nREUNIÓN {i}")
            
            # Imprime el título del evento.
            print(f"   Título: {reunion['titulo']}")
            # Imprime la fecha.
            print(f"   Fecha: {reunion['fecha']}")
            # Imprime el horario.
            print(f"   Hora: {reunion['hora']}")
            # Imprime con quiénes es la reunión.
            print(f"   Participantes: {reunion['participantes']}")
            
            # Verifica si el campo de notas NO está vacío.
            if reunion['notas']:
                # Solo imprime esta línea si el usuario escribió alguna nota al momento de crear la reunión.
                print(f"   Notas: {reunion['notas']}")
                
            # Imprime el estado actual (por ahora siempre será 'programada').
            print(f"   Estado: {reunion['estado']}")

        # Imprime la línea de cierre decorativa inferior.
        print("="*60 + "\n")
        
        # El asistente dice por voz cuántas reuniones totales tenés programadas usando len() para medir la lista.
        self.hablar(f"Tienes {len(self.reuniones)} reuniones programadas")
# Asistente Virtual de Negocios — ARIA BUSINESS

Asistente de gestión empresarial con análisis financiero en tiempo real,
gestión de contactos y reuniones, cálculos de negocio, investigación
empresarial y utilidades varias, todo por texto o por voz.

## Estructura del proyecto

```
aria_business/
├── main.py                  # Punto de entrada del programa
├── asistente.py             # Clase AsistenteNegocios (une todos los mixins)
├── comandos.py               # Interpretación de comandos, ayuda y ciclo principal
├── core/
│   ├── voz.py                # Síntesis y reconocimiento de voz
│   └── persistencia.py       # Guardado/carga de datos en JSON
├── finanzas/
│   ├── acciones.py           # Precio, comparación e historial de acciones
│   ├── cartera.py            # Cartera de inversiones persistente
│   ├── mercados.py           # Índices bursátiles y análisis de sectores
│   └── calculos.py           # Margen, ROI, punto de equilibrio, monedas
├── negocios/
│   ├── contactos.py          # Gestión de contactos comerciales
│   ├── reuniones.py          # Agenda de reuniones
│   └── investigacion.py      # Investigación de empresas (Wikipedia)
├── utilidades/
│   └── extras.py             # Fecha/hora, música (pywhatkit), chistes (pyjokes), sitios web
├── requirements.txt
└── datos_negocio.json        # Se crea automáticamente al usar el asistente
```

Cada archivo define un **mixin** (una clase con un grupo de funciones
relacionadas). `asistente.py` combina todos los mixins en la clase final
`AsistenteNegocios`, así el código queda separado por tema pero se sigue
usando como una sola clase (`self.hablar(...)`, `self.guardar_datos()`, etc.
funcionan igual en cualquier archivo).

## Instalación

```
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta que contiene `aria_business/`:

```
python -m aria_business.main
```

## Comandos disponibles

Ejecutá el asistente y escribí `ayuda` para ver el listado completo de
comandos (análisis financiero, cartera, índices, sectores, cálculos
empresariales, contactos, reuniones, investigación y utilidades).

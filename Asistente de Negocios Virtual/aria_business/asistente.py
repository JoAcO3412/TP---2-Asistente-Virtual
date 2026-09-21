"""
╔═══════════════════════════════════════════════════════════════╗
║          ASISTENTE VIRTUAL DE NEGOCIOS - ARIA BUSINESS         ║
║                    VERSIÓN COMPLETA v3.0                       ║
╚═══════════════════════════════════════════════════════════════╝

Proyecto: Asistente Virtual para Gestión Empresarial
Descripción: Sistema inteligente de automatización para empresarios,
             gerentes y profesionales en negocios.

Rubro: NEGOCIOS Y GESTIÓN EMPRESARIAL
Aplicabilidad: Asistente para Ejecutivos y Emprendedores

FUNCIONALIDADES PRINCIPALES:
✓ Análisis financiero en tiempo real (acciones individuales y múltiples)
✓ Comparación detallada de acciones (precio, P/E)
✓ Historial de precios por período (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y)
✓ Gestión y análisis de cartera de inversiones (persistente)
✓ Índices bursátiles principales (S&P 500, Nasdaq, Dow, IBEX, DAX, FTSE, Nikkei)
✓ Análisis de sectores (tecnología, bancario, salud, energía, retail, consumo)
✓ Cálculos empresariales (margen, ROI, punto de equilibrio, proyecciones)
✓ Conversión de monedas
✓ Gestión de contactos comerciales
✓ Gestión de reuniones y agendas
✓ Investigación de empresas e industrias (Wikipedia)
✓ Persistencia de datos en JSON
✓ Interfaz por voz (síntesis y reconocimiento) y por texto
✓ Hora y fecha actual
✓ Reproducción de canciones en YouTube (vía pywhatkit)
✓ Chistes para relajar el ambiente laboral (vía pyjokes)
✓ Apertura de sitios web (vía webbrowser)

Este módulo define la clase AsistenteNegocios, que arma todas las
funcionalidades a partir de mixins organizados por carpetas:

    core/       -> voz (síntesis/reconocimiento) y persistencia de datos
    finanzas/   -> acciones, cartera, índices/sectores, cálculos
    negocios/   -> contactos, reuniones, investigación
    utilidades/ -> fecha/hora, música, chistes
    comandos.py -> interpretación de comandos, ayuda y ciclo principal

Librerías utilizadas:
- pyttsx3: Síntesis de voz (TTS) para que el asistente hable.
- speech_recognition: Reconocimiento de voz (STT) para comandos hablados.
- pywhatkit: Reproducción de música desde YouTube.
- yfinance: Datos financieros en tiempo real (acciones, índices, monedas).
- pyjokes: Generación de chistes.
- webbrowser: Apertura de sitios web desde el asistente.
- datetime: Gestión de agenda, historial y fecha/hora actual.
- wikipedia: Búsquedas para investigación empresarial.
- json / os: Persistencia de datos.
"""

from typing import Dict, List

import pyttsx3
import speech_recognition as sr

from core.voz import VozMixin
from core.persistencia import PersistenciaMixin
from finanzas.acciones import AccionesMixin
from finanzas.cartera import CarteraMixin
from finanzas.mercados import MercadosMixin
from finanzas.calculos import CalculosMixin
from negocios.contactos import ContactosMixin
from negocios.reuniones import ReunionesMixin
from negocios.investigacion import InvestigacionMixin
from utilidades.extras import UtilidadesMixin
from comandos import ComandosMixin


class AsistenteNegocios(
    VozMixin,
    PersistenciaMixin,
    AccionesMixin,
    CarteraMixin,
    MercadosMixin,
    CalculosMixin,
    ContactosMixin,
    ReunionesMixin,
    InvestigacionMixin,
    UtilidadesMixin,
    ComandosMixin,
):
    """
    Asistente Virtual especializado en Negocios y Gestión Empresarial.
    Automatiza tareas comerciales y proporciona análisis financiero en
    tiempo real. Combina todas las capacidades (voz, finanzas, gestión
    comercial y utilidades) mediante mixins organizados en subcarpetas.
    """

    def __init__(self, nombre: str = "ARIA BUSINESS", empresa: str = "Mi Empresa"):
        """
        Inicializa el asistente de negocios.

        Args:
            nombre: Nombre del asistente.
            empresa: Nombre de la empresa del usuario.
        """
        self.nombre = nombre
        self.empresa = empresa
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.en_ejecucion = False

        # Datos persistentes
        self.contactos: Dict = {}
        self.reuniones: List = []
        self.cartera_acciones: Dict = {}
        self.clientes: Dict = {}
        self.historial_busquedas: List = []

        self.configurar_engine()
        self.cargar_datos()

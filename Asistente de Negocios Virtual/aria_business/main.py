"""Punto de entrada del Asistente Virtual de Negocios - ARIA BUSINESS."""

try:
    from asistente import AsistenteNegocios
except ImportError:
    # Permite ejecutar "python main.py" directamente desde dentro de la carpeta
    from asistente import AsistenteNegocios


def main():
    """Función principal del programa."""
    print("\n" + "="*66)
    print(" "*66)
    print("ASISTENTE VIRTUAL DE NEGOCIOS - ARIA BUSINESS".center(66))
    print(" "*66)
    print("="*66)

    nombre_empresa = input("¿Cuál es el nombre de tu empresa? ").strip() or "Mi Empresa"

    asistente = AsistenteNegocios(nombre="ARIA BUSINESS", empresa=nombre_empresa)

    try:
        asistente.iniciar()
    except KeyboardInterrupt:
        print("\n[Sistema]: Asistente finalizado.")


if __name__ == "__main__":
    main()

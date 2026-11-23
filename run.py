import argparse

from src.arranque import crear_aplicacion

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BitacoraBio 2026 · registro de experimentos (HU-01.A1)")
    parser.add_argument("--db", metavar="ARCHIVO", help="guarda los datos en una base SQLite (por ejemplo, bitacorabio.db); sin esto, los datos viven en memoria")
    argumentos = parser.parse_args()
    crear_aplicacion(argumentos.db).run(debug=False, port=5000)

# aventura/main.py
"""
Ejecutar desde la carpeta juego/ con:
    python -m aventura.main
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aventura.game import AventuraGame


def main():
    AventuraGame().run()


if __name__ == "__main__":
    main()

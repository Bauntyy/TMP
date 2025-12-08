from manim import *
import numpy as np

try:
    from geometry_classes import Dot3d, Regular_Dodecahedron
    from euler_scenes import (
        EulerFormula_01, EulerFormula_02, EulerFormula_03,
        EulerFormula_04
    )
except ImportError:
    print("Ошибка импорта. Убедитесь, что файлы geometry_classes.py и euler_scenes.py находятся в той же директории.")
    print("Или запускайте файлы напрямую:")
    print("manim -pql euler_scenes.py EulerFormula_01")


if __name__ == "__main__":
    print("Для запуска сцен используйте командную строку:")
    print("1. manim -pql main.py EulerFormula_01")
    print("2. manim -pql main.py EulerFormula_02")
    print("3. manim -pql main.py EulerFormula_03")
    print("4. manim -pql main.py EulerFormula_04")
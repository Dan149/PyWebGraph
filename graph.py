__module_errors__ = []
try:
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.parsing.sympy_parser import (
        standard_transformations,
        implicit_multiplication_application,
    )

    global sympy_module_error
except ModuleNotFoundError:
    __module_errors__.append("sympy")
try:
    from numpy import linspace
except ModuleNotFoundError:
    __module_errors__.append("numpy")
from math import *  # permet l'utilisation de formules mathématiques complexes


class Graph:  # svg 600x400
    def __init__(self, equation: str) -> None:
        self.module_errors = __module_errors__
        self.equation = equation
        self.x_values = linspace(-5, 5, 250).tolist()
        self.y_images = []  # liste images de y
        self.svg_content_list = []  # liste des attributs svg
        self.parsed_equation = 0
        if len(self.module_errors) == 0:
            transformations = standard_transformations + (
                implicit_multiplication_application,
            )
            self.parsed_equation = str(
                parse_expr(equation, transformations=transformations)
            )

    def get_y_images(self) -> None:  # définit les valeurs de y
        for x in self.x_values:  # converti en -5 6 et 0.05
            self.y_images.append(eval(self.parsed_equation))

    def create_graph(self) -> str:  # retourne un SVG dans un string
        self.svg_content_list.append(
            "<rect x='50' y='50' height='400' width='500' fill-opacity='10%' stroke='black'/> <line x1='275' x2='275' y1='50' y2='450' stroke='black'/>"
        )
        for x in range(11):
            self.svg_content_list.append(
                f"<line x1='{x*50+50}' x2='{x*50+50}' y1='50' y2='450' stroke='rgba(0,0,0,0.6)' /><text y='475px' x='{x*50+48}' font-size='16'>{x}</text>"
            )
        for x in self.x_values:
            pass
        return " ".join(self.svg_content_list)

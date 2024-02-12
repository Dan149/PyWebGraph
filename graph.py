try:
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.parsing.sympy_parser import (
        standard_transformations,
        implicit_multiplication_application,
    )

    global sympy_module_error
    sympy_module_error = False
except ModuleNotFoundError:
    sympy_module_error = True
from math import *
import os.path


class Graph:
    def __init__(self, equation: str) -> None:
        self.sympy_module_error = sympy_module_error
        self.equation = equation
        transformations = standard_transformations + (
            implicit_multiplication_application,
        )
        self.parsed_equation = str(
            parse_expr(equation, transformations=transformations)
        )

    def create_graph(self) -> str:  # retourne un SVG dans un string
        pass

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


class Graph:  # svg 600x600
    def __init__(self, equation: str) -> None:
        self.module_errors = __module_errors__
        self.equation = equation
        self.x_values = linspace(-5, 5, 500).tolist()
        self.y_images = []  # liste images de y
        self.svg_content_list = []  # liste des attributs svg
        self.parsed_equation = "0"
        self.displayed_equation = (
            "0"  # Equation prise en compte pour la génération des images
        )
        if len(self.module_errors) == 0:
            transformations = standard_transformations + (
                implicit_multiplication_application,
            )
            try:
                self.parsed_equation = str(
                    parse_expr(equation, transformations=transformations)
                )
            except:
                self.parsed_equation = "none"
            # Mise à l'echelle pour affichage:
            if "x" not in self.parsed_equation:
                self.displayed_equation = str(self.parsed_equation + "*0.5")
            elif (
                len(self.parsed_equation.split("+")) > 1
                or len(self.parsed_equation.split("-")) > 1
            ):
                if "x" not in self.parsed_equation.split("+")[-1]:
                    self.displayed_equation = str(self.parsed_equation + "*0.5")
                elif "x" not in self.parsed_equation.split("-")[-1]:
                    self.displayed_equation = str(self.parsed_equation + "*0.5")
                else:
                    self.displayed_equation = self.parsed_equation
            else:
                self.displayed_equation = self.parsed_equation

    def generate_y_images(self) -> None:  # définit les valeurs de y
        for x in self.x_values:
            try:
                self.y_images.append(eval(self.displayed_equation))
            except:  # pour les solutions nulles
                self.y_images.append(None)

    def create_graph(self) -> str:  # retourne un SVG dans un string
        self.generate_y_images()
        self.svg_content_list.append(
            f"<text font-size='18' x='50' y='25'>Equation initiale: {self.equation} | Equation simplifiée: {self.parsed_equation}</text>"
        )
        self.svg_content_list.append(
            "<rect x='50' y='50' height='500' width='500' fill-opacity='10%' stroke='black' style='z-index:-1;'/>"
        )
        self.svg_content_list.append(
            "<line x1='300' x2='300' y1='50' y2='550' stroke='black'/> <line x1='50' x2='550' y1='300' y2='300' stroke='black'/>"
        )
        y = 5
        for x in range(11):
            self.svg_content_list.append(
                f"<line x1='{x*50+50}' x2='{x*50+50}' y1='50' y2='550' stroke='rgba(0,0,0,0.2)' /> <text y='575px' x='{x*50+46}' font-size='16'>{x-5}</text>"
            )
            self.svg_content_list.append(
                f"<line x1='50' x2='550' y1='{x*50+50}' y2='{x*50+50}' stroke='rgba(0,0,0,0.2)' /> <text y='{x*50+55}' x='25' font-size='16'>{y}</text>"
            )
            y -= 1
        for i in range(len(self.x_values) - 1):
            if self.y_images[i] != None:
                if (
                    550 >= self.x_values[i] * 100 + 300
                    and 50 <= self.x_values[i] * 100 + 300
                    and 550 >= 300 + (-(self.y_images[i] * 100))
                    and 50 <= 300 + (-(self.y_images[i] * 100))
                ):
                    if self.y_images[i] == None or self.y_images[i + 1] == None:
                        pass
                    elif 550 < self.x_values[i + 1] * 100 + 300:
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*100+300}' x2='550' y1='{300+(-(self.y_images[i]*100))}' y2='{300+(-(self.y_images[i]*100))}' stroke='red'/>"
                        )
                    elif 550 < 300 + (-(self.y_images[i + 1] * 100)):
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*100+300}' x2='{self.x_values[i]*100+300}' y1='{300+(-(self.y_images[i]*100))}' y2='550' stroke='red'/>"
                        )
                    elif 50 > 300 + (-(self.y_images[i + 1] * 100)):
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*100+300}' x2='{self.x_values[i+1]*100+300}' y1='{300+(-(self.y_images[i]*100))}' y2='50' stroke='red'/>"
                        )
                    else:
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*100+300}' x2='{self.x_values[i+1]*100+300}' y1='{300+(-(self.y_images[i]*100))}' y2='{300+(-(self.y_images[i+1]*100))}' stroke='red'/>"
                        )

        return " ".join(self.svg_content_list)

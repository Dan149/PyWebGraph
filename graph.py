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
    def __init__(self, equation: str, xmin: int, xmax: int) -> None:
        self.module_errors = __module_errors__
        self.equation = equation
        try:
            xmin, xmax = int(xmin), int(xmax)
            if xmax - xmin >= 10:
                self.xmin = xmin
                self.xmax = xmax
            else:
                self.xmin = -5
                self.xmax = 5
        except:
            self.xmin = -5
            self.xmax = 5

        if (self.xmax - self.xmin) % 10 == 0:
            self.x_interval = []
            self.x_interval_step = int((self.xmax - self.xmin) / 10)
            for x in range(int(self.xmin), int(self.xmax + 1), self.x_interval_step):
                self.x_interval.append(x)
        else:
            (self.x_interval, self.x_interval_step) = linspace(
                self.xmin, self.xmax, 10, retstep=True
            )
            self.x_interval = self.x_interval.tolist()
            for x in range(len(self.x_interval)):
                self.x_interval[x] = int(ceil(self.x_interval[x]))
            self.x_interval_step = int(self.x_interval_step)
        self.x_values = linspace(self.xmin, self.xmax, self.xmax * 100).tolist()
        self.y_images = []  # liste images de y
        self.svg_content_list = []  # liste des attributs svg
        self.parsed_equation = "0"
        self.processed_equation = (
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
                self.processed_equation = str(self.parsed_equation + "*0.5")
            elif (
                len(self.parsed_equation.split("+")) > 1
                or len(self.parsed_equation.split("-")) > 1
            ):
                self.processed_equation = self.parsed_equation
                if "x" not in self.parsed_equation.split("+")[-1]:
                    self.processed_equation = str(self.parsed_equation + "*0.5")
                elif "x" not in self.parsed_equation.split("-")[-1]:
                    self.processed_equation = str(self.parsed_equation + "*0.5")

                if "x" not in self.parsed_equation.split("+")[0]:
                    self.processed_equation = str("0.5*" + self.parsed_equation)
                elif "x" not in self.parsed_equation.split("-")[0]:
                    self.processed_equation = str("0.5*" + self.parsed_equation)
            else:
                self.processed_equation = self.parsed_equation

    def generate_y_images(self) -> None:  # définit les valeurs de y
        for x in self.x_values:
            try:
                self.y_images.append(eval(self.processed_equation))
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
        if self.xmax + self.xmin == 0:
            self.svg_content_list.append(
                f"<line x1='300' x2='300' y1='50' y2='550' stroke='black'/>"
            )
        y = self.x_interval_step * 5
        x = self.xmin
        for i in range(11):
            self.svg_content_list.append(
                f"<line x1='{i*50+50}' x2='{i*50+50}' y1='50' y2='550' stroke='rgba(0,0,0,0.2)' /> <text y='575px' x='{i*50+46}' font-size='16'>{x}</text>"
            )
            self.svg_content_list.append(
                f"<line x1='50' x2='550' y1='{i*50+50}' y2='{i*50+50}' stroke='rgba(0,0,0,0.2)' /> <text y='{i*50+55}' x='25' font-size='16'>{y}</text>"
            )
            if int(x) == 0:
                self.svg_content_list.append(
                    f"<line x1='{i*50+50}' x2='{i*50+50}' y1='50' y2='550' stroke='black'/>"
                )
            if int(y) == 0:
                self.svg_content_list.append(
                    f"<line x1='50' x2='550' y1='{i*50+50}' y2='{i*50+50}' stroke='black'/>"
                )
            y -= self.x_interval_step
            x += self.x_interval_step
            if self.x_interval.index(min(self.x_interval, key=abs)) == 0:
                spacing = 50
            else:
                if (self.xmax - self.xmin) % 10 == 0:
                    spacing = 50
                else:
                    spacing = 100
        xtranslation = spacing + (
            self.x_interval.index(min(self.x_interval, key=abs)) * 50
        )
        ytranslation = 300
        scale = 1000 / (self.xmax - self.xmin)
        for i in range(len(self.x_values) - 1):
            if self.y_images[i] != None:
                if (
                    550 >= self.x_values[i] * scale + xtranslation
                    and 50 <= self.x_values[i] * scale + xtranslation
                    and 550 >= ytranslation + (-(self.y_images[i] * scale))
                    and 50 <= ytranslation + (-(self.y_images[i] * scale))
                ):
                    if self.y_images[i] == None or self.y_images[i + 1] == None:
                        pass
                    elif 550 < self.x_values[i + 1] * scale + xtranslation:
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*scale+xtranslation}' x2='550' y1='{ytranslation+(-(self.y_images[i]*scale))}' y2='{ytranslation+(-(self.y_images[i]*scale))}' stroke='red'/>"
                        )
                    elif 550 < ytranslation + (-(self.y_images[i + 1] * scale)):
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*scale+xtranslation}' x2='{self.x_values[i]*scale+xtranslation}' y1='{ytranslation+(-(self.y_images[i]*scale))}' y2='550' stroke='red'/>"
                        )
                    elif 50 > ytranslation + (-(self.y_images[i + 1] * scale)):
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*scale+xtranslation}' x2='{self.x_values[i+1]*scale+xtranslation}' y1='{ytranslation+(-(self.y_images[i]*scale))}' y2='50' stroke='red'/>"
                        )
                    else:
                        self.svg_content_list.append(
                            f"<line x1='{self.x_values[i]*scale+xtranslation}' x2='{self.x_values[i+1]*scale+xtranslation}' y1='{ytranslation+(-(self.y_images[i]*scale))}' y2='{ytranslation+(-(self.y_images[i+1]*scale))}' stroke='red'/>"
                        )

        return " ".join(self.svg_content_list)

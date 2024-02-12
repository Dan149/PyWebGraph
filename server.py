import cherrypy
import os.path
from os import remove
import atexit

#
from graph import Graph


def exit_handler():
    if os.path.isfile("./static/fonction.png"):
        remove("./static/fonction.png")


atexit.register(exit_handler)


conf = {
    "global": {
        "server.socket_host": "127.0.0.1",
        "server.socket_port": 8080,
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.dirname(os.path.abspath(__file__)) + "/static",
    }
}


class Site:
    def __init__(self):
        self.head = """
  <!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyWebGraph - Tracé de courbe</title>
  <link rel="stylesheet" href="style.css"/>
</head>
  """

    def index(self, fonction=None):
        if fonction != None:
            g = Graph(fonction)
            if g.sympy_module_error:
                script = "alert(\"La bibliothèque Sympy est une dépendence du Serveur PyWebGraph, veuillez l'installer avec 'python3 -m pip install sympy'.\")"
            g.create_graph()
        return f"""
  {self.head}
  <body>
  <h1> Tracé de courbe </h1>
  <h3>Notice:</h3> <ul>
  <li> La fonction ne doit présenter qu'une inconnue, nommée x.</li><li> Les fonctions trigonométriques sont acceptés dans l'expression sous forme: cos(nombre), etc... </li><li> La racine carrée est également utilisable avec sqrt(nombre).</li></ul>
  <form action="index" method="get>
  <label for="fonction">Fonction mathématique:</label>
  <input type="text" name="fonction" placeholder="Entrer une fonction mathématique..." required/>
    <input type="submit" value="Valider"/>
    </form>
    <img src="fonction.png" style="width:50%; display:block; margin:0 auto;"/>
    <script>{script}</script>
    </body>
    </html>"""

    index.exposed = True


cherrypy.quickstart(Site(), config=conf)

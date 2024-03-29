import cherrypy
import os.path

#
from graph import Graph


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
</head>
  """

    def index(self, fonction="0", xmin=-5, xmax=5, stepCheckbox=None):
        script = ""
        svg_content = ""
        g = Graph(fonction, xmin, xmax)
        if len(g.module_errors) != 0:
            script = f"alert(\"Des dépendances de Serveur PyWebGraph ne sont pas satisfaites, veuillez installer les bibliothèques: {' '.join(g.module_errors)}. Utilisez la commande: 'python3 -m pip install {' '.join(g.module_errors)}'.\")"
        else:
            svg_content = g.create_graph()
        return f"""
  {self.head}
  <body>
  <h1> Tracé de courbe </h1>
  <h3>Notice:</h3> <ul>
  <li> La fonction ne doit présenter qu'une inconnue, nommée x.</li>
  <li>De manière générale, toute propriété de la bibliothèque python "math" est utilisable (ex: sqrt(), sin(), cos(), tan(), pi).</li>
  <li>L'intervalle inclusif minimal est 10 (établi par défaut entre -5 et 5).</li>
  </ul>
  <form action="index" method="get>
  <label for="fonction">Fonction mathématique:</label>
  <input type="text" name="fonction" placeholder="Entrer une fonction mathématique..." value={fonction} required/>
  <label for="stepCheckbox">Arrondir les axes et l'intervalle:</label>
  <input type="checkbox" name="stepCheckbox" id="step-checkbox"/>
  <label for="xmin">Xmin</label>
  <input type="number" width="20px" value="{xmin}" name="xmin" min="-5000" max="4995" id="xmin-input" step="1" required/>
    <label for="xmax">Xmax</label>
  <input type="number" width="20px" value="{xmax}" name="xmax" min="-4995" max="5000" id="xmax-input" step="1" required/>
    <input type="submit" value="Valider"/>
    </form>
    <svg width="600px" height="600px" style="display:block; margin:80px auto; border:1px solid black; border-radius: 20px;">{svg_content}</svg>
    <div style="position:fixed; bottom:0; right:5px; color: grey;">PyWebGraph | Copyright Daniel Falkov 2024, tous droits réservés.</div>
    <script>{script}</script>
    <script src="./script.js" type="text/javascript"></script>
    </body>
    </html>"""

    index.exposed = True


cherrypy.quickstart(Site(), config=conf)

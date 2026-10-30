"""Application Todo : une petite liste de tâches (API web avec Flask)."""
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

# En local : lit le fichier .env s'il existe (jamais commité)
load_dotenv()

# Configuration lue dans l'environnement, plus rien en dur
APP_TITLE = os.environ.get("APP_TITLE", "Ma liste de tâches")
# Secret : aucune valeur par défaut
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")


class TodoList:
    """Une liste de tâches gardée en mémoire."""

    def __init__(self):
        self.taches = []

    def ajouter(self, texte):
        """Ajoute une tâche à la fin de la liste."""
        texte = texte.strip()
        if not texte:
            raise ValueError("Une tâche ne peut pas être vide")
        self.taches.append(texte)
        return self.taches

    def supprimer(self, index):
        """Supprime la tâche à la position index (0 = la première)."""
        del self.taches[index]

    def vider(self):
        """Supprime toutes les tâches."""
        self.taches.clear()


app = Flask(__name__)
liste = TodoList()


@app.route("/")
def accueil():
    return jsonify(titre=APP_TITLE, nombre_de_taches=len(liste.taches))


@app.route("/health")
def sante():
    """Contrôle de santé : répond « ok » si l'application tourne."""
    return jsonify(statut="ok")


@app.route("/taches", methods=["GET"])
def lister():
    return jsonify(liste.taches)


@app.route("/taches", methods=["POST"])
def creer():
    donnees = request.get_json(silent=True) or {}
    try:
        liste.ajouter(donnees.get("texte", ""))
    except ValueError as erreur:
        return jsonify(erreur=str(erreur)), 400
    return jsonify(liste.taches), 201


@app.route("/taches/<int:index>", methods=["DELETE"])
def effacer(index):
    try:
        liste.supprimer(index)
    except IndexError:
        return jsonify(erreur="Tâche introuvable"), 404
    return jsonify(liste.taches)


@app.route("/taches", methods=["DELETE"])
def tout_effacer():
    """Vide la liste : réservé à l'administrateur."""
    if not ADMIN_TOKEN:
        return jsonify(erreur="Jeton administrateur non configuré"), 503
    if request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify(erreur="Accès refusé"), 403
    liste.vider()
    return jsonify(liste.taches)


if __name__ == "__main__":
    # 0.0.0.0 : accessible depuis l'extérieur (indispensable dans Docker)
    app.run(host="0.0.0.0", port=5000)

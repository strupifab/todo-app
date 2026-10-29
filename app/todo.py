"""Application Todo : une petite liste de tâches (API web avec Flask)."""
from flask import Flask, jsonify, request

# Configuration de l'application
APP_TITLE = "Ma liste de tâches"
ADMIN_TOKEN = "admin-123"  # valeur écrite en dur : à corriger au lab 11


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
        # del self.taches[index]
        pass

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
    if request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify(erreur="Accès refusé"), 403
    liste.vider()
    return jsonify(liste.taches)


if __name__ == "__main__":
    # 0.0.0.0 : accessible depuis l'extérieur (indispensable dans Docker)
    app.run(host="0.0.0.0", port=5000)

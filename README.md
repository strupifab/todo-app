# Application Todo
![Build](https://github.com/<vous>/todo-app/actions/workflows/build.yml/badge.svg)

Une petite API web de liste de tâches, écrite en Python avec Flask.
C'est l'application « fil rouge » de la formation.

## Lancer l'application (dans le terminal de l'EC2)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/todo.py
```

Puis ouvrez http://<IP-EC2>:5000 dans le navigateur de votre PC
(le port 5000 doit être ouvert à « Mon IP » dans le groupe de sécurité).

## Essayer l'API (dans un 2e terminal de l'EC2)

```bash
curl http://localhost:5000/taches
curl -X POST -H "Content-Type: application/json" \
     -d '{"texte": "Acheter du pain"}' http://localhost:5000/taches
curl -X DELETE http://localhost:5000/taches/0
curl http://localhost:5000/health
```

## Lancer les tests

```bash
pytest -v
```

# Image de départ officielle : Linux + Python 3.12, version allégée
FROM python:3.12-slim
#FROM python:3.12
 
# Dossier de travail dans le conteneur
WORKDIR /app
 
# 1) Les dépendances d'abord (elles changent rarement : cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# 2) Le code ensuite (il change souvent)
COPY app/ ./app/
 
# Port utilisé par l'application
EXPOSE 5000
 
# Commande lancée au démarrage du conteneur
CMD ["python", "app/todo.py"]

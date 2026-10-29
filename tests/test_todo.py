import pytest
 

from app.todo import TodoList, app
 

# --- Tests unitaires de la classe TodoList ---------------------------


def test_liste_vide_au_depart():
    liste = TodoList()
    assert liste.taches == []


def test_ajouter_tache():
    # 1. Préparer
    liste = TodoList()
    # 2. Agir
    liste.ajouter("Acheter du pain")
    # 3. Vérifier
    assert liste.taches == ["Acheter du pain"]


def test_supprimer_tache():
    liste = TodoList()
    liste.ajouter("Acheter du pain")
    liste.supprimer(0)
    assert len(liste.taches) == 0


def test_tache_vide_refusee():
    liste = TodoList()
    with pytest.raises(ValueError):
        liste.ajouter("   ")


# --- Tests de l'API web (intégration) --------------------------------


def test_api_health():
    client = app.test_client()
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.get_json() == {"statut": "ok"}


def test_api_ajouter_puis_lister():
    client = app.test_client()
    client.post("/taches", json={"texte": "Appeler Tom"})
    reponse = client.get("/taches")



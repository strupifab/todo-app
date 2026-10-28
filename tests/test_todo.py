from app.todo import TodoList


def test_ajouter_tache():
    # 1. Préparer
    liste = TodoList()
    # 2. Agir
    liste.ajouter("Acheter du pain")
    # 3. Vérifier
    assert len(liste.taches) == 1

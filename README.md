##🎬 Movie Explorer

Une application full-stack qui permet d’explorer des films au hasard et de générer des résumés grâce à l’intelligence artificielle.

## 📦 Fonctionnalités

- Ajouter des films avec leurs acteurs via FastAPI
- Récupérer un film au hasard depuis la base de données
- Générer des résumés engageants grâce à un modèle LLM (via Groq)
- Explorer les informations dans une interface interactive avec Streamlit

## 🛠 Technologies Utilisées

- **FastAPI** : Backend API
- **PostgreSQL** : Base de données
- **LangChain + Groq** : Génération de résumés
- **Streamlit** : Interface utilisateur frontend

## 📁 Structure du Projet

```
Practice Exam/
├── main_fastapi.py           # Backend FastAPI
├── main_streamlit.py         # Frontend Streamlit
├── database.py               # Configuration de la connexion à la base
├── models.py                 # Modèles SQLAlchemy
├── schemas.py                # Modèles Pydantic
├── .env                      # Variables d'environnement
└── requirements.txt          # Dépendances Python
```

## 🚀 Lancement

### Lancer le backend FastAPI

```bash
uvicorn main_fastapi:app --reload
```

### Ajouter des films (obligatoire avant d’utiliser l’app)

```json
{
  "title": "Inception",
  "year": 2010,
  "director": "Christopher Nolan",
  "actors": [
    {"actor_name": "Leonardo DiCaprio"},
    {"actor_name": "Joseph Gordon-Levitt"},
    {"actor_name": "Elliot Page"},
    {"actor_name": "Tom Hardy"}
  ]
}
```

### Lancer le frontend Streamlit

```bash
streamlit run main_streamlit.py
```

## ❓ Questions / Réponses

### Question 1 : Pourquoi est-il nécessaire de valider (commit) l’enregistrement principal (Movies) avant de créer les enregistrements liés (Actors) ?

✅ **Réponse** : La clé étrangère `movie_id` dans la table `Actors` fait référence à l’ID du film dans la table `Movies`. Cette valeur `id` est généralement générée automatiquement par la base de données (auto-increment ou séquence). Il faut donc commit le film pour que son ID soit disponible lors de l'ajout des acteurs.

---

### Question 2 : Différence entre lazy loading et eager loading (joinedload) dans SQLAlchemy ?

✅ **Réponse** :

- **Lazy Loading** : Les relations sont chargées uniquement lors du premier accès. Cela peut entraîner plusieurs requêtes SQL (problème N+1).
- **Eager Loading (ex: `joinedload`)** : Les relations sont chargées directement via une jointure SQL. Cela réduit le nombre de requêtes, mais peut charger trop de données.

---

### Question 3 : Comment formater la liste des acteurs pour un prompt LLM ?

✅ **Réponse** :

- Un seul acteur → `"Leonardo DiCaprio"`
- Deux acteurs → `"Leonardo DiCaprio and Joseph Gordon-Levitt"`
- Plusieurs acteurs → `"Leonardo DiCaprio, Joseph Gordon-Levitt, and Tom Hardy"`


    ##  Auteur

- Mohamed Rhouma – 

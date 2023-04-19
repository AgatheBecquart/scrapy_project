import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')
client = MongoClient(ATLAS_KEY)
db = client["Top250"]
films_collection = db["Top_films"]

# Fonction de recherche multicritère
def search_by_criteria(title, actor, genre, min_rating, max_duration):
    criteria = {}
    if title:
        criteria["titre"] = {"$regex": title, "$options": "i"}
    if actor:
        criteria["casting"] = {"$regex": actor, "$options": "i"}
    if genre:
        criteria["genre"] = genre
    if min_rating:
        criteria["note"] = {"$gte": str(min_rating)}
        print(min_rating)
    if max_duration:
        criteria["duree"] = {"$lte": max_duration}
    results = films_collection.find({"$and": [criteria]}).sort("note", -1)
    return list(results)

# Interface Streamlit
st.title("Recherche de films")

# Champs de recherche
st.header("Critères de recherche")
title_query = st.text_input("Titre")
actor_query = st.text_input("Acteur")
genre_query = st.text_input("Genre")
rating_query = st.slider("Note minimale", 0.0, 10.0, 0.0, 0.1)
max_duration_query = st.slider("Durée maximale (en minutes)", 0, 300, 0, 10)

# Bouton de recherche
if st.button("Rechercher"):
    # Recherche avec les critères sélectionnés
    results = search_by_criteria(title_query, actor_query, genre_query, rating_query, max_duration_query)
    if results:
        st.write(f"Résultats pour la recherche :")
        for result in results:
            st.write(result["titre"][0])
    else:
        st.write("Aucun résultat trouvé.")

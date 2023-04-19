import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
ATLAS_KEY= os.getenv('ATLAS_KEY')

# Connect to MongoDB cluster
client = MongoClient(ATLAS_KEY)

# Select the database and collections
db = client["Top250"]
films_collection = db["Top_films"]
series_collection = db["Top_series"]

# Page de recherche
def recherche():
    st.title("Recherche de films et séries")
    
    # Propose de chercher un film ou une série
    choix = st.radio("Rechercher un/e", options=["Film", "Série"])
    
    # Define function for searching films
    def search_films(name=None, actors=None, genre=None, duration=None, note=None):
        print("Je suis dans la fonction search_films")
        query = {}
        if name:
            query["titre"] = {"$regex": name, "$options": "i"}
        if actors:
            query["casting"] = {"$regex": actors, "$options": "i"}
        if genre:
            query["genre"] = genre
        if note:
            query["note"] = {"$gte": str(note)}
        if duration:
            query["duree"] = {"$lte": duration}
        return list(films_collection.find(query))

    # Define function for searching series
    def search_series(name=None, actors=None, genre=None, duration=None, note=None):
        print("Je suis dans la fonction search_series")
        query = {}
        if name:
            query["title.0"] = {"$regex": name, "$options": "i"}
        if actors:
            query["cast.0"] = {"$regex": actors, "$options": "i"}
        if genre:
            query["genre.0"] = {"$regex": genre, "$options": "i"}
        if duration:
            query["total_duration"] = {"$lt": duration}
        if note:
            query["score"] = {"$gte": str(note)}
        return list(series_collection.find(query))

    # Search parameters
    name = st.text_input("Rechercher par nom:")
    actors = st.text_input("Rechercher par acteur(s):")
    genre = st.text_input("Rechercher par genre:")
    duration = st.slider("Rechercher par durée (en minutes):", min_value=0, max_value=300, step=5)
    note = st.slider("Rechercher par note (minimale):", min_value=0.0, max_value=10.0, step=0.1)

    # Search button
    if st.button("Rechercher"):
        if choix == "film":
            resultats = search_films(name, actors, genre, duration, note)
        else:
            resultats = search_series(name, actors, genre, duration, note)

        # Display search results
        if resultats:
            for resultat in resultats:
                # Afficher le résultat en fonction du type (film ou série)
                if choix == "film":
                    st.title(resultat["titre"][0])
                    st.subheader("Année: " + str(resultat["year"]))
                    st.write("Note: " + str(resultat["note"][0]))
                    st.write("Synopsis:", resultat["synopsis"][0])
                    st.write("Casting:", ", ".join(resultat["casting"]))
                    st.write("Pays:", resultat["pays"][0])
                    st.write("Public:", resultat["public"][0])
                    st.write("---")
                else:
                    st.title(resultat["title"][0])
                    st.subheader("Année: " + str(resultat["year"]))
                    st.write("Note: " + str(resultat["score"][0]))
                    st.write("Description:", resultat["description"][0])
                    st.write("Casting:", ", ".join(resultat["cast"]))
                    st.write("Pays:", ", ".join(resultat["country"]))
                    st.write("Langue:", ", ".join(resultat["language"]))
                    st.write("---")

# Page de réponse aux questions
def reponse():
    
    def film_plus_long():
        film_plus_long = db.Top_films.find_one(sort=[("duree", -1)])
        st.write("Le film le plus long est : ", film_plus_long["titre"][0])
        
    def films_mieux_notes():
        films_mieux_notes = db.Top_films.find().sort([("note", -1)]).limit(5)
        st.write("Les 5 films les mieux notés sont : ")
        for film in films_mieux_notes:
            st.write(film["titre"][0], "-", film["note"][0])
            
    def nb_films_joues():
        nb_films_morgan = db.Top_films.count_documents({"casting": {"$in": ["Morgan Freeman"]}})
        nb_films_tom = db.Top_films.count_documents({"casting": {"$in": ["Tom Cruise"]}})
        st.write("**Morgan Freeman** a joué dans", nb_films_morgan, "films")
        st.write("**Tom Cruise** a joué dans", nb_films_tom, "film")
        
    def meilleurs_films_genre():
        genres = db.Top_films.distinct("genre")
        genre_choice = st.selectbox("Sélectionner un genre", genres)
        films = db.Top_films.find({"genre": genre_choice}).sort("note", -1).limit(3)
        st.write(f"**Les 3 meilleurs films du genre {genre_choice}:**")
        for film in films:
            st.write(film["titre"][0], "-", film["note"][0])

    def pourcentage_films():
        films_mieux_notes_100 = list(db.Top_films.find().sort([("note", -1)]).limit(100))
        nb_films_americains = len([film for film in films_mieux_notes_100 if "United States" in film["pays"]])
        nb_films_francais = len([film for film in films_mieux_notes_100 if "France" in film["pays"]])
        pourcentage_americains = nb_films_americains / 100 * 100
        pourcentage_francais = nb_films_francais / 100 * 100
        st.write("Parmi les 100 films les mieux notés, {:.2f}% sont américains et {:.2f}% sont français.".format(pourcentage_americains, pourcentage_francais))
        
    def duree_moyenne_films():
        genres = db.Top_films.distinct("genre")
        selected_genre = st.selectbox("Sélectionner un genre", genres)
        if selected_genre:
            durees = []
            films_genre = db.Top_films.find({"genre": selected_genre})
            for film in films_genre:
                durees.append(film["duree"])
            duree_moyenne = sum(durees) / len(durees)
            st.write(f"La durée moyenne des films du genre {selected_genre} est de {duree_moyenne:.2f} minutes.")

    
    def main():
        st.title("Analyse des Top 250 films d'IMDb")
        st.write("Ce dashboard permet d'analyser les Top 250 films d'IMDb en utilisant la base de données MongoDB.")
        st.title("Réponses aux questions")
        
        question_menu = ["Film le plus long", "Films les mieux notés", "Nombre de films joués par des acteurs", "Meilleurs films par genre", "Pourcentage de films américains et français parmi les 100 meilleurs", "Durée moyenne des films par genre"]
        selected_question = st.selectbox("Sélectionner une question", question_menu)

        if selected_question == "Film le plus long":
            film_plus_long()
        elif selected_question == "Films les mieux notés":
            films_mieux_notes()
        elif selected_question == "Nombre de films joués par des acteurs":
            nb_films_joues()
        elif selected_question == "Meilleurs films par genre":
            meilleurs_films_genre()
        elif selected_question == "Pourcentage de films américains et français parmi les 100 meilleurs":
            pourcentage_films()
        elif selected_question == "Durée moyenne des films par genre":
            duree_moyenne_films()


    if __name__ == '__main__':
        main()
        
# Ajouter une barre de navigation
menu = ["Recherche de films/séries", "Réponses aux questions"]
choice = st.sidebar.selectbox("Menu", menu)

# Afficher la page sélectionnée
if choice == "Recherche de films/séries":
    recherche()
else:
    reponse()

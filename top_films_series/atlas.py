#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pymongo
from pymongo import MongoClient


# In[27]:


from dotenv import load_dotenv
import os
load_dotenv()
ATLAS_KEY= os.getenv('ATLAS_KEY')


# In[28]:


print(ATLAS_KEY)


# In[29]:


client = MongoClient(ATLAS_KEY)


# In[30]:


# sélectionner la base de données
db = client.Top250


# ## Quel est le film le plus long ?

# In[32]:


film_plus_long = db.Top_films.find_one(sort=[("duree", -1)])
print("Le film le plus long est : ", film_plus_long["titre"][0])


# ## Quels sont les 5 films les mieux notés ?

# In[33]:


films_mieux_notes = db.Top_films.find().sort([("note", -1)]).limit(5)
for film in films_mieux_notes:
    print(film["titre"][0], "-", film["note"][0])


# ## Dans combien de films a joué Morgan Freeman ? Tom Cruise ?

# In[37]:


nb_films_morgan = db.Top_films.count_documents({"casting": {"$in": ["Morgan Freeman"]}})
print("Morgan Freeman a joué dans", nb_films_morgan, "films")

nb_films_tom = db.Top_films.count_documents({"casting": {"$in": ["Tom Cruise"]}})
print("Tom Cruise a joué dans", nb_films_tom, "film")


# ## Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?

# In[41]:


films_horreur = db.Top_films.find({"genre": "Horror"}).sort([("note", -1)]).limit(3)
print("Les 3 meilleurs films d'horreur sont :")
for film in films_horreur:
    print(film["titre"][0], "-", film["note"][0])
print()

films_drame = db.Top_films.find({"genre": "Drama"}).sort([("note", -1)]).limit(3)
print("Les 3 meilleurs films dramatiques sont :")
for film in films_drame:
    print(film["titre"][0], "-", film["note"][0])
print()

films_comique = db.Top_films.find({"genre": "Comedy"}).sort([("note", -1)]).limit(3)
print("Les 3 meilleurs films comiques sont :")
for film in films_comique:
    print(film["titre"][0], "-", film["note"][0])


# ## Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?

# In[57]:


# Calcul du pourcentage de films américains et français parmi les 100 films les mieux notés
films_mieux_notes_100 = list(db.Top_films.find().sort([("note", -1)]).limit(100))
nb_films_americains = len([film for film in films_mieux_notes_100 if "United States" in film["pays"]])
nb_films_francais = len([film for film in films_mieux_notes_100 if "France" in film["pays"]])
pourcentage_americains = nb_films_americains / 100 * 100
pourcentage_francais = nb_films_francais / 100 * 100

print("Parmi les 100 films les mieux notés, {:.2f}% sont américains et {:.2f}% sont français.".format(pourcentage_americains, pourcentage_francais))


# ## Quel est la durée moyenne d’un film en fonction du genre ?

# In[63]:


# Obtenir la liste des genres uniques
genres = db.Top_films.distinct("genre")

# Boucler sur la liste des genres pour calculer la durée moyenne de chaque genre
for genre in genres:
    durees = []
    films_genre = db.Top_films.find({"genre": genre})
    for film in films_genre:
        durees.append(film["duree"])
    duree_moyenne = sum(durees) / len(durees)
    print(f"Durée moyenne des films de genre {genre}: {round(duree_moyenne)} minutes")


# ## En fonction du genre, afficher la liste des films les plus longs.

# In[64]:


genres = db.Top_films.distinct("genre")
for genre in genres:
    films = db.Top_films.find({"genre": genre}).sort("duree", -1).limit(3)
    print(f"Les 3 films les plus longs du genre {genre}:")
    for film in films:
        print(film["titre"][0], "-", film["duree"], "minutes")
    print()


# ## En fonction du genre, quel est le coût de tournage d’une minute de film ?
# 

# ## Quels sont les séries les mieux notés ?
# 

# In[69]:


series_mieux_notes = db.Top_series.find().sort([("score", -1)]).limit(5)
for serie in series_mieux_notes:
    print(serie["title"][0], "-", serie["score"])


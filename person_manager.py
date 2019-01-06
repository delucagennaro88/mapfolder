import imdb
import json
import os
import sys
import time

from json_manager import open_json, open_json_data, check_filmographies

actor_collection = {}

ia = imdb.IMDb()


def define_dates(actor_identifier):
    birth = ""
    death = ""

    for key, value in actor_identifier.items():
        if key == "birth date":
            birth = actor_identifier['birth date'][:4]
        elif key == "death date":
            death = actor_identifier['death date'][:4]
        else:
            pass

    if birth and death:
        dates = '(' + str(birth) + '-' + str(death) + ')'

    elif not birth:
        dates = '(' + '-' + str(death) + ')'

    elif not death:
        dates = '(' + str(birth) + '-' + ')'

    else:
        dates = "(-)"

    return dates


def search_filmography(filmography):
    actor_dictionary = {}
    for a in filmography:
        for key, value in a.items():
            key_index = str(key)  # qui va salvato l'indice della categoria
            if key_index == "director" or key_index == "writer" or key_index == "actor":
                actor_dictionary[key_index] = []
                time.sleep(5)
                for b in value:
                    print(b)
                    movie_film = ia.search_movie(str(b))
                    print(movie_film)
                    movie = movie_film[0]
                    print(movie)
                    movie_id = movie.movieID
                    title = movie.get('title')
                    movie_year = movie['year']
                    actor_dictionary[key_index].append(
                        {'Title': title, 'Year': movie_year, 'Id': movie_id, 'Original': str(b), 'Present': False})
                    time.sleep(5)
            else:
                pass
    return actor_dictionary


def check_presence(cinema_json, json_actor_dir):
    change = False
    cinema_file = open_json(cinema_json)
    attori_file = open_json_data(
        json_actor_dir)  # Occorre creare una funzione apposita per aprire il File. OPEN_JSOn non va bene!

    cinema_data = cinema_file.values()

    for z in attori_file.values():
        for w in z:
            # print(w['Name'])
            for y, (key, value) in enumerate(w['Filmography'].items()):
                for x in value:
                    for a in cinema_data:
                        for b in a:
                            if x['Id'] == b['Movie Id'] and x['Present'] == False:
                                print(x['Title'])
                                x['Present'] = True
                                change = True

    if change == True:
        print('Updated')
        with open(json_actor_dir, 'w') as outfile:
            json.dump(attori_file, outfile, indent=4, ensure_ascii=False)
    else:
        print("Non ci sono cambiamenti")
        return


def attori_amati(cinema_json, json_actor_dir, actor_name):
    # 1. Dato il nome di un attore, restituisce l'elenco di tutti i suoi film (solo titoli e date)
    # 2. L'elenco viene salvato in JSON
    # 3. Scorre l'elenco e verifica quali sono i film già posseduti e quali no.
    try:
        actors = ia.search_person(actor_name)
        actor = actors[0]
        actor_id = actor.personID
        actor_identifier = ia.get_person(actor_id)

        URL = ia.get_imdbURL(actor)

        dates = define_dates(actor_identifier)

        filmography = actor_identifier['filmography']
        filmography_box = search_filmography(filmography)

        actor_name_str = str(actor)

        if "'" in actor_name_str:
            # se c'è l'apostrofo
            new_actor_str = actor_name_str.replace("'", "")
            print(new_actor_str)
        else:
            # se non c'è l'apostrofo
            new_actor_str = actor_name_str

        actor_gif = "static/res/" + new_actor_str.lower().replace(" ", "") + ".gif"  # eliminiamo maiuscole e spazi e aggiungiamo l'estensione gif
        actor_poster = "res/" + new_actor_str.lower().replace(" ", "") + "_poster.jpg"

        actor_collection[actor_name_str] = []
        actor_collection[actor_name_str].append(
            {'Name': actor_name_str, 'Id': actor_id, 'Date': dates, 'Gif': actor_gif, 'Poster': actor_poster, 'Filmography': filmography_box, 'Url': URL})

        #UPDATE presences nei cast dei film
        check_filmographies(actor_id)

        # qui si verifica se il JSON esiste
        # se non esiste si crea e si scrive con W
        # se esiste si aggiorna col metodo inventato
        if not os.path.exists(json_actor_dir):
            with open(json_actor_dir, 'w') as outfile:
                json.dump(actor_collection, outfile, sort_keys=True, indent=4, ensure_ascii=False)
            print("Creato!")
            check_presence(cinema_json, json_actor_dir)
            print("Aggiornato con le presenze")
            return
        else:
            with open(json_actor_dir, 'r') as outfile:
                data = json.load(outfile)
            data_str = str(data)
            no_brackets = data_str[
                          data_str.find("{") + 1:data_str.rfind("}")]  # ora non è un dizionario, ma una stringa
            # facciamo lo stesso con collection
            collection_str = str(actor_collection)
            no_brackets_coll = collection_str[collection_str.find("{") + 1:collection_str.rfind("}")]
            # ora concateniamo le due stringhe
            new_str = '{' + no_brackets + ', ' + no_brackets_coll + '}'
            # qui ritorna dictionary
            dict1 = eval(new_str)
            with open(json_actor_dir, 'w') as outfile:
                json.dump(dict1, outfile, indent=4, ensure_ascii=False)
            print("Modificato!")
            check_presence(cinema_json, json_actor_dir)
            print("Aggiornato con le presenze")
    except imdb.IMDbError as e:
        print("Probably you're not connected to Internet.  Complete error report:")
        print(e)
        sys.exit(3)

    if not actor:
        print('It seems that there\'s no actor with "%s"' % actor)
        sys.exit(4)

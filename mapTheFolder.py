import os, time, sys
from bytes_converter import bytes_converter
from Movie import Movie
import imdb

directory = "C:\\Users\\Utente\\Desktop\\FILM"
collection = []
ia = imdb.IMDb()

def search_director(movie_identifier):
    directors = movie_identifier['director']
    director_container= {}
    for dir in directors:
        director_name = dir['name']
        director_id = dir.personID
        director_container.update({'DirectorName': director_name,'DirectorId': director_id})
        return director_container

def search_cast(movie_identifier):
    actors = movie_identifier['cast']
    for actor in actors:
        actor_name = actor['name']
        actor_id = actor.personID
        return actor_name, actor_id

def movie_name(i):
    try:
        movies = ia.search_movie(i)
        movie = movies[0]
        title = movie.get('title')
        imdbURL = ia.get_imdbURL(movie)
        movie_id = movie.movieID
        movie_year = movie['year']
        movie_identifier = ia.get_movie(movie_id)
        plot = movie_identifier.get('plot', [''])[0]
        plot = plot.split('::')[0]
        director_box = search_director(movie_identifier)
        actor_name, actor_id = search_cast(movie_identifier)

    except imdb.IMDbError as e:
        print("Probably you're not connected to Internet.  Complete error report:")
        print(e)
        sys.exit(3)

    if not movie:
        print('It seems that there\'s no movie with movie_id "%s"' % title)
        sys.exit(4)

    movie_container = {'Title': title, 'Url': imdbURL, 'Id': movie_id, 'Year': movie_year, 'Plot': plot, 'DirectorBox': director_box, 'ActorName': actor_name, 'ActorId': actor_id}

    return movie_container

def save_info(directory):
    if os.path.exists(directory):
        for i in os.listdir(directory):

            film = movie_name(i)

            dir = os.path.join(directory, i)

            if os.path.isfile(dir):
                ext = os.path.splitext(dir)[1]
                size = bytes_converter(os.path.getsize(dir))

            elif os.path.isdir(dir):
                ext = 'directory' #qui andrebbe messa una funzione che apre la cartella e analizza i file interni
                size = 0 #qui andrebbe messa una funzione che quantifica i file nella cartella

            else:
                ext = 'unknown'
                size = 0

            a = os.stat(os.path.join(directory, i))

            collection.append(Movie(directory, i, dir, time.ctime(a.st_atime), time.ctime(a.st_ctime), size, ext, film['Id'], film['Url'], film['Title'], film['Year'], film['Plot'], film['DirectorBox'], film['ActorName'], film['ActorId']))

        return collection

    else:
        print('Mi dispiace! La Directory non esiste...riprova')

# Qui comincia il programma

save_info(directory)

for i in collection:
    #print('\n')
    #print('Informazioni sul file' + '\n' + i.home_path + '\n' + i.name + '\n' + i.dir + '\n' + str(i.atime) + '\n' + str(i.ctime) + '\n' + str(i.size) + '\n' + i.ext + '\n\n\n')
    #print('Informazioni sul film' + '\n' + str(i.id) + '\n' + i.url + '\n' + i.title + '\n' + str(i.year) + '\n' + i.plot + '\n')

    for value in i.director_box.values():
        print(value)
    #for nome_attore, id_attore in i.actor_name, i.actor_id:
    #    print(nome_attore+ '\n' + str(id_attore) + '\n')
    print('\n\n\n')

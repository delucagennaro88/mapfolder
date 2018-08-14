import os, time, sys
from bytes_converter import bytes_converter
from Folder import Folder
import imdb

directory = "C:\\Users\\Utente\\Desktop\\FILM"
collection = []
ia = imdb.IMDb()

def search_director(movie_identifier):
    directors = movie_identifier['director']
    for dir in directors:
        director_name = dir['name']
        director_id = dir.personID
        print(director_name, director_id)

def search_cast(movie_identifier):
    actors = movie_identifier['cast']
    for actor in actors:
        actor_name = actor['name']
        actor_id = actor.personID
        print(actor_name, actor_id)

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
        print('Info on movies\n\n\n')
        print(title + '\n\n\n' + imdbURL + '\n\n\n' + str(movie_id) + '\n\n\n' + str(movie_year))
        search_director(movie_identifier)
        search_cast(movie_identifier)
        print(plot)

    except imdb.IMDbError as e:
        print("Probably you're not connected to Internet.  Complete error report:")
        print(e)
        sys.exit(3)

    if not movie:
        print('It seems that there\'s no movie with movie_id "%s"' % title)
        sys.exit(4)

def save_info(directory):
    if os.path.exists(directory):
        for i in os.listdir(directory):

            film = movie_name(i)

            dir = os.path.join(directory, i)

            if os.path.isfile(dir):
                print('è un file!')
                ext = os.path.splitext(dir)[1]
                size = bytes_converter(os.path.getsize(dir))

            elif os.path.isdir(dir):
                print('è una cartella')
                ext = 'directory' #qui andrebbe messa una funzione che apre la cartella e analizza i file interni
                size = 0 #qui andrebbe messa una funzione che quantifica i file nella cartella

            else:
                print('non è un file')
                ext = 'unknown'
                size = 0

            a = os.stat(os.path.join(directory, i))

            collection.append(Folder(directory, i, dir, time.ctime(a.st_atime), time.ctime(a.st_ctime), size, ext))

        return collection

    else:
        print('Mi dispiace! La Directory non esiste...riprova')

# Qui comincia il programma

save_info(directory)

for i in collection:
    print('Info on files\n\n\n')
    print(i.home_path+'\n\n\n'+i.name+'\n\n\n'+i.dir+'\n\n\n'+str(i.atime)+'\n\n\n'+str(i.ctime)+'\n\n\n'+str(i.size)+'\n\n\n'+i.ext)

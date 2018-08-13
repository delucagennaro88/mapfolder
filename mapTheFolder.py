import os, time
from bytes_converter import bytes_converter
from Folder import Folder
from imdb import IMDb

directory = "C:\\Users\\Utente\\Desktop\\FILM"
collection = []
ia = IMDb()

def movie_name(i):
    movies = ia.search_movie(i)
    movie = movies[0]
    title = movie.get('title')
    return title

def save_info(directory):
    if os.path.exists(directory):
        for i in os.listdir(directory):

            film = movie_name(i)
            print(film)

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
    print(i.home_path)
    print(i.name)
    print(i.dir)
    print(i.atime)
    print(i.ctime)
    print(i.size)
    print(i.ext)
    print('Bravo\n\n\n\n')

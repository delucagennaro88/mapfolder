import os, time
from movie_manager import movie_name
from bytes_converter import bytes_converter
from Movie import Movie

collection = []

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

            collection.append(Movie(directory, i, dir, time.ctime(a.st_atime), time.ctime(a.st_ctime), size, ext, film['Id'], film['Url'], film['Title'], film['Year'], film['Plot'], film['DirectorBox'], film['ActorBox']))

        return collection

    else:
        print('Mi dispiace! La Directory non esiste...riprova')
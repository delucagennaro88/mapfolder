import os, time
from movie_manager import movie_name
from bytes_converter import bytes_converter
from Movie import Movie

collection = {}


def save_info(directory):
    num = 0

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
            collection[num] = []
            collection[num].append({'Home Directory': directory, 'Id': i, 'File Name': dir, 'Atime': time.ctime(a.st_atime), 'Ctime': time.ctime(a.st_ctime), 'Size': size, 'Extension': ext, 'Movie Id': film['Id'], 'Movie Url': film['Url'], 'Movie Title': film['Title'], 'Movie Year': film['Year'], 'Movie plot': film['Plot'], 'Movie Director': film['DirectorBox'], 'Movie Actor': film['ActorBox']})
            num += 1

        return collection

    else:
        print('Mi dispiace! La Directory non esiste...riprova')